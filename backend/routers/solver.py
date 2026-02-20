"""
AI Solver Router - Solve exercises using trained models
"""

from fastapi import APIRouter, HTTPException
from schemas import SolveRequest, SolveResponse

router = APIRouter(prefix="/api/solver", tags=["solver"])

# Lazy-loaded model references
_transformer_model = None
_qwen_model = None


def _get_transformer():
    global _transformer_model
    if _transformer_model is not None:
        return _transformer_model

    try:
        import sys, os
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        sys.path.insert(0, project_root)

        import torch
        from ai.tokenizer.bpe import MathBPETokenizer
        from ai.transformer.model import MathTransformer

        tokenizer_path = os.path.join(project_root, "ai", "tokenizer", "math_bpe.json")
        checkpoint_path = os.path.join(project_root, "ai", "transformer", "checkpoints", "best_model.pt")

        if not os.path.exists(tokenizer_path) or not os.path.exists(checkpoint_path):
            return None

        tokenizer = MathBPETokenizer()
        tokenizer.load(tokenizer_path)

        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        model = MathTransformer.from_pretrained(checkpoint_path, device=str(device))

        _transformer_model = {"model": model, "tokenizer": tokenizer, "device": device}
    except Exception:
        _transformer_model = None

    return _transformer_model


def _get_qwen():
    global _qwen_model
    if _qwen_model is not None:
        return _qwen_model

    try:
        import sys, os
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        sys.path.insert(0, project_root)

        from ai.finetune.inference import solve_exercise as qwen_solve

        adapter_path = os.path.join(project_root, "ai", "finetune", "adapters")
        if not os.path.exists(adapter_path):
            adapter_path = None

        _qwen_model = {"solve_fn": qwen_solve, "adapter_path": adapter_path}
    except Exception:
        _qwen_model = None

    return _qwen_model


@router.post("/solve", response_model=SolveResponse)
def solve_exercise(req: SolveRequest):
    if req.model == "transformer":
        engine = _get_transformer()
        if not engine:
            raise HTTPException(
                status_code=503,
                detail="Modelul Transformer nu este disponibil. Antrenati-l mai intai.",
            )

        try:
            import torch
            from ai.tokenizer.bpe import MathBPETokenizer

            model = engine["model"]
            tokenizer = engine["tokenizer"]
            device = engine["device"]

            # Format autoregresiv: <BOS> question <SEP> → generează răspunsul
            bos = MathBPETokenizer.SPECIAL_TOKENS["<BOS>"]
            sep = MathBPETokenizer.SPECIAL_TOKENS["<SEP>"]
            eos = MathBPETokenizer.SPECIAL_TOKENS["<EOS>"]
            pad = MathBPETokenizer.SPECIAL_TOKENS["<PAD>"]

            prompt_ids = [bos] + tokenizer.encode(req.question) + [sep]
            input_tensor = torch.tensor([prompt_ids], dtype=torch.long).to(device)

            output = model.generate(input_tensor, max_new_tokens=200, temperature=0.5, top_k=30)

            # Decodăm doar partea generată
            gen_ids = output[0].tolist()[len(prompt_ids):]
            clean_ids = []
            for tid in gen_ids:
                if tid in (eos, pad):
                    break
                clean_ids.append(tid)

            decoded = tokenizer.decode(clean_ids)

            # Parse: răspunsul și pașii sunt separați cu <SEP>
            parts = decoded.split("<SEP>") if "<SEP>" in decoded else [decoded]
            answer = parts[0].strip()
            steps = [s.strip() for s in parts[1:] if s.strip()]

            return SolveResponse(
                answer=answer,
                steps=steps,
                model_used="transformer",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Eroare la rezolvare: {str(e)}")

    elif req.model == "qwen":
        qwen = _get_qwen()
        if not qwen:
            raise HTTPException(
                status_code=503,
                detail="Modelul Qwen+LoRA nu este disponibil. Antrenati-l mai intai.",
            )

        try:
            result = qwen["solve_fn"](req.question, adapter_path=qwen["adapter_path"])
            return SolveResponse(
                answer=result.get("answer", ""),
                steps=result.get("steps", []),
                model_used="qwen_lora",
                confidence=result.get("confidence"),
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Eroare la rezolvare: {str(e)}")


@router.get("/models")
def list_models():
    """List available AI models and their status."""
    transformer = _get_transformer()
    qwen = _get_qwen()

    return {
        "models": [
            {
                "id": "transformer",
                "name": "Math Transformer (custom, autoregresiv)",
                "status": "loaded" if transformer else "not_available",
                "description": "Transformer autoregresiv antrenat de la zero pe exercitii BAC",
            },
            {
                "id": "qwen",
                "name": "Qwen2.5-Math + LoRA",
                "status": "loaded" if qwen else "not_available",
                "description": "Qwen2.5-Math fine-tuned cu LoRA pe exercitii BAC",
            },
        ]
    }
