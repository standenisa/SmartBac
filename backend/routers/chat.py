"""
Chat Router — AI-powered math assistant chat endpoint.

Tries models in order:
  1. Custom Transformer (if trained)
  2. Qwen+LoRA via MLX (if available)
  3. Rule-based fallback (always works)
"""

import re
import os
import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api", tags=["chat"])

# Add project root for AI imports
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


class ChatRequest(BaseModel):
    message: str
    user_id: int = 1
    model: Optional[str] = None  # "transformer", "qwen", or None (auto)


class ChatResponse(BaseModel):
    response: str
    latex: Optional[str] = None
    model_used: str = "rule_based"


# ── Lazy model loaders ──

_transformer_cache = None
_transformer_loaded = False


def _load_transformer():
    global _transformer_cache, _transformer_loaded
    if _transformer_loaded:
        return _transformer_cache
    _transformer_loaded = True

    try:
        import torch
        from ai.tokenizer.bpe import MathBPETokenizer
        from ai.transformer.model import MathTransformer

        tokenizer_path = os.path.join(_PROJECT_ROOT, "ai", "tokenizer", "math_bpe.json")
        checkpoint_path = os.path.join(_PROJECT_ROOT, "ai", "transformer", "checkpoints", "best_model.pt")

        if not os.path.exists(tokenizer_path) or not os.path.exists(checkpoint_path):
            return None

        tokenizer = MathBPETokenizer()
        tokenizer.load(tokenizer_path)

        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        model = MathTransformer.from_pretrained(checkpoint_path, device=str(device))

        _transformer_cache = {"model": model, "tokenizer": tokenizer, "device": device}
    except Exception:
        _transformer_cache = None

    return _transformer_cache


def _try_transformer(message: str) -> Optional[dict]:
    """Try solving with the custom Transformer."""
    engine = _load_transformer()
    if not engine:
        return None

    try:
        import torch
        from ai.tokenizer.bpe import MathBPETokenizer

        model = engine["model"]
        tokenizer = engine["tokenizer"]
        device = engine["device"]

        # Format autoregresiv: <BOS> message <SEP> → model generează răspunsul
        bos = MathBPETokenizer.SPECIAL_TOKENS["<BOS>"]
        sep = MathBPETokenizer.SPECIAL_TOKENS["<SEP>"]
        eos = MathBPETokenizer.SPECIAL_TOKENS["<EOS>"]
        pad = MathBPETokenizer.SPECIAL_TOKENS["<PAD>"]

        prompt_ids = [bos] + tokenizer.encode(message) + [sep]
        input_tensor = torch.tensor([prompt_ids], dtype=torch.long).to(device)

        output = model.generate(input_tensor, max_new_tokens=200, temperature=0.7, top_k=50)

        # Decodăm doar partea generată
        gen_ids = output[0].tolist()[len(prompt_ids):]
        clean_ids = []
        for tid in gen_ids:
            if tid in (eos, pad):
                break
            clean_ids.append(tid)

        answer = tokenizer.decode(clean_ids).strip()
        return {"response": answer, "model_used": "transformer"}
    except Exception:
        return None


def _try_qwen(message: str) -> Optional[dict]:
    """Try solving with Qwen+LoRA."""
    try:
        from ai.finetune.inference import solve_exercise

        adapter_path = os.path.join(_PROJECT_ROOT, "ai", "finetune", "adapters")
        if not os.path.exists(adapter_path):
            adapter_path = None

        result = solve_exercise(message, adapter_path=adapter_path)
        full = result.get("full_response", result.get("answer", ""))
        return {"response": full, "model_used": "qwen_lora"}
    except Exception:
        return None


# ── Rule-based fallback ──

_PATTERNS = [
    # Linear equations: ax + b = c
    (r"(\d*)x\s*([+-]\s*\d+)\s*=\s*([+-]?\d+)",
     lambda m: _solve_linear(m)),
    # Quadratic: x^2 - a = 0  or  x² - a = 0
    (r"x[\^²]2?\s*-\s*(\d+)\s*=\s*0",
     lambda m: f"x = ±sqrt({m.group(1)})"),
    # Simple: ax = b
    (r"(\d+)x\s*=\s*(\d+)",
     lambda m: f"x = {int(m.group(2))}/{m.group(1)} = {int(m.group(2))/int(m.group(1)):.4g}"),
]


def _solve_linear(m):
    coeff = int(m.group(1)) if m.group(1) else 1
    b = int(m.group(2).replace(" ", ""))
    c = int(m.group(3))
    x = (c - b) / coeff
    return f"x = ({c} - ({b})) / {coeff} = {x:.4g}"


def _rule_based(message: str) -> dict:
    """Simple pattern-matching fallback."""
    text = message.strip()

    for pattern, handler in _PATTERNS:
        match = re.search(pattern, text)
        if match:
            answer = handler(match)
            return {
                "response": f"Rezolvare:\n{answer}",
                "model_used": "rule_based",
            }

    return {
        "response": (
            "Momentan nu am un model AI incarcat pentru a rezolva aceasta problema. "
            "Te rog sa incerci un exercitiu de tip ecuatie liniara sau patrata.\n\n"
            "Exemple:\n"
            "- Rezolva ecuatia: 3x - 5 = 7\n"
            "- Rezolva: x^2 - 9 = 0\n"
            "- Calculeaza: 5x = 35"
        ),
        "model_used": "rule_based",
    }


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Mesajul nu poate fi gol.")

    # If a specific model is requested, try only that one
    if req.model == "transformer":
        result = _try_transformer(message)
        if result:
            return ChatResponse(**result)
        raise HTTPException(status_code=503, detail="Modelul Transformer nu este disponibil.")

    if req.model == "qwen":
        result = _try_qwen(message)
        if result:
            return ChatResponse(**result)
        raise HTTPException(status_code=503, detail="Modelul Qwen nu este disponibil.")

    # Auto mode: try models in order
    result = _try_transformer(message)
    if result:
        return ChatResponse(**result)

    result = _try_qwen(message)
    if result:
        return ChatResponse(**result)

    # Fallback to rule-based
    result = _rule_based(message)
    return ChatResponse(**result)
