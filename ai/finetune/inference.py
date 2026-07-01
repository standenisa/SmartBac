"""
Inference with LoRA fine-tuned Qwen2.5-Math
"""
import json
import re
import sys
import argparse
from pathlib import Path
from typing import Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ai.finetune.lora_config import LoRAConfig, InstructionTemplate

# ---------------------------------------------------------------------------
# MLX imports
# ---------------------------------------------------------------------------
try:
    import mlx.core as mx
    import mlx.nn as nn
    from mlx.utils import tree_unflatten
    MLX_AVAILABLE = True
except ImportError:
    MLX_AVAILABLE = False

try:
    from mlx_lm import load as mlx_load
    from mlx_lm import generate as mlx_generate
    from mlx_lm.tuner.lora import LoRALinear
    MLX_LM_AVAILABLE = True
except ImportError:
    MLX_LM_AVAILABLE = False


# ============================================================================
# Model loader
# ============================================================================

_MODEL_CACHE: dict = {}


def load_model(
    adapter_path: Optional[str] = None,
    config: Optional[LoRAConfig] = None,
):
    """Load the base model and optionally merge LoRA adapter weights.

    Parameters
    ----------
    adapter_path : str, optional
        Path to a directory containing ``adapters.safetensors`` and
        ``adapter_config.json``.  If *None*, the default
        ``<output_dir>/best_adapter`` (or ``final_adapter``) is used.
    config : LoRAConfig, optional
        Override the default configuration.

    Returns
    -------
    tuple
        ``(model, tokenizer)``
    """
    if not MLX_AVAILABLE or not MLX_LM_AVAILABLE:
        print(
            "\nMLX is not available. Install with:\n"
            "  pip install mlx mlx-lm\n"
        )
        sys.exit(1)

    config = config or LoRAConfig()

    # Resolve adapter path
    if adapter_path is None:
        base = Path(__file__).resolve().parent.parent.parent / config.output_dir
        if (base / "best_adapter" / "adapters.safetensors").exists():
            adapter_path = str(base / "best_adapter")
        elif (base / "final_adapter" / "adapters.safetensors").exists():
            adapter_path = str(base / "final_adapter")
        else:
            adapter_path = None  # No adapter -- use base model only

    cache_key = (config.model_name, adapter_path or "")
    if cache_key in _MODEL_CACHE:
        return _MODEL_CACHE[cache_key]

    print(f"[inference] Loading base model: {config.model_name}")
    model, tokenizer = mlx_load(config.model_name)

    if adapter_path is not None:
        adapter_file = Path(adapter_path) / "adapters.safetensors"
        if adapter_file.exists():
            print(f"[inference] Loading LoRA adapters from {adapter_path}")

            # Apply LoRA structure first (same target modules as training)
            for name, child in model.named_modules():
                short = name.split(".")[-1]
                if short in config.target_modules and isinstance(child, nn.Linear):
                    lora_layer = LoRALinear.from_linear(
                        child,
                        r=config.lora_rank,
                        alpha=config.lora_alpha,
                        dropout=0.0,  # No dropout at inference
                    )
                    parts = name.split(".")
                    parent = model
                    for p in parts[:-1]:
                        parent = parent[int(p)] if p.isdigit() else getattr(parent, p)
                    setattr(parent, parts[-1], lora_layer)

            # Load adapter weights (saved flat, with dotted keys)
            adapter_weights = mx.load(str(adapter_file))
            model.update(tree_unflatten(list(adapter_weights.items())))
            mx.eval(model.parameters())
            print(f"[inference] LoRA adapters loaded ({len(adapter_weights)} tensors)")
        else:
            print(f"[inference] WARNING: Adapter file not found at {adapter_file}")
            print("[inference] Running with base model only.")
    else:
        print("[inference] No adapter path provided. Running with base model only.")

    _MODEL_CACHE[cache_key] = (model, tokenizer)
    return model, tokenizer


# ============================================================================
# Response parsing
# ============================================================================

def _parse_response(raw: str) -> dict:
    """Parse the raw model output into structured fields.

    Returns
    -------
    dict
        ``{ "answer": str, "steps": list[str], "full_response": str }``
    """
    full_response = raw.strip()

    # Try to extract final answer
    answer = ""
    answer_match = re.search(r"Răspuns:\s*(.+?)(?:\n|$)", full_response)
    if answer_match:
        answer = answer_match.group(1).strip()

    # Extract numbered steps
    steps = []
    step_matches = re.findall(r"Pasul\s+\d+:\s*(.+?)(?:\n|$)", full_response)
    if step_matches:
        steps = [s.strip() for s in step_matches]

    # If no structured steps found, split by newlines as fallback
    if not steps:
        lines = [l.strip() for l in full_response.split("\n") if l.strip()]
        # Filter out the answer line
        steps = [l for l in lines if not l.startswith("Răspuns:")]

    return {
        "answer": answer,
        "steps": steps,
        "full_response": full_response,
    }


# ============================================================================
# Solve functions
# ============================================================================

def solve_exercise(
    question: str,
    max_tokens: int = 512,
    temperature: float = 0.1,
    adapter_path: Optional[str] = None,
    config: Optional[LoRAConfig] = None,
) -> dict:
    """Solve a single maths exercise.

    Parameters
    ----------
    question : str
        The exercise text (Romanian BAC format).
    max_tokens : int
        Maximum number of tokens to generate.
    temperature : float
        Sampling temperature. Lower = more deterministic.
    adapter_path : str, optional
        Path to LoRA adapter directory.
    config : LoRAConfig, optional
        Model / inference configuration.

    Returns
    -------
    dict
        ``{ "question": str, "answer": str, "steps": list[str],
            "full_response": str }``
        Suitable for direct JSON serialisation and FastAPI responses.
    """
    model, tokenizer = load_model(adapter_path=adapter_path, config=config)

    prompt = InstructionTemplate.format_prompt(question)

    # Generate
    response = mlx_generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=max_tokens,
        temp=temperature,
    )

    # Strip any trailing special tokens
    for stop in ["<|im_end|>", "<|endoftext|>"]:
        if stop in response:
            response = response[: response.index(stop)]

    parsed = _parse_response(response)
    parsed["question"] = question
    return parsed


def batch_solve(
    questions: list[str],
    max_tokens: int = 512,
    temperature: float = 0.1,
    adapter_path: Optional[str] = None,
    config: Optional[LoRAConfig] = None,
) -> list[dict]:
    """Solve multiple exercises sequentially.

    Parameters
    ----------
    questions : list[str]
        List of exercise texts.

    Returns
    -------
    list[dict]
        One result dict per question (same schema as ``solve_exercise``).
    """
    results = []
    for i, q in enumerate(questions, 1):
        print(f"[batch] Solving {i}/{len(questions)} ...")
        result = solve_exercise(
            q,
            max_tokens=max_tokens,
            temperature=temperature,
            adapter_path=adapter_path,
            config=config,
        )
        results.append(result)
    return results


# ============================================================================
# Interactive mode
# ============================================================================

def interactive_mode(adapter_path: Optional[str] = None, config: Optional[LoRAConfig] = None):
    """Read exercises from stdin, solve, and print results."""
    print("\n" + "=" * 60)
    print(" BAC Math Assistant -- Interactive Mode")
    print(" Type your exercise and press Enter.")
    print(" Type 'quit' or 'exit' to stop.")
    print("=" * 60 + "\n")

    # Pre-load model
    load_model(adapter_path=adapter_path, config=config)

    while True:
        try:
            question = input("Exercițiu> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nLa revedere!")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("La revedere!")
            break

        result = solve_exercise(question, adapter_path=adapter_path, config=config)
        print("\n--- Rezolvare ---")
        print(result["full_response"])
        print("-" * 40)
        if result["answer"]:
            print(f"Răspuns: {result['answer']}")
        print()


# ============================================================================
# API-compatible helpers (for FastAPI integration)
# ============================================================================

def get_api_response(question: str, adapter_path: Optional[str] = None) -> dict:
    """Return a response in the format expected by the FastAPI backend.

    This is a thin wrapper around ``solve_exercise`` that ensures the output
    matches the schema consumed by the ``/api/solve`` endpoint.

    Returns
    -------
    dict
        ``{ "question": str, "answer": str, "steps": list[str],
            "full_response": str, "model": str, "status": "success"|"error" }``
    """
    try:
        result = solve_exercise(question, adapter_path=adapter_path)
        result["model"] = LoRAConfig.model_name
        result["status"] = "success"
        return result
    except Exception as e:
        return {
            "question": question,
            "answer": "",
            "steps": [],
            "full_response": "",
            "model": LoRAConfig.model_name,
            "status": "error",
            "error": str(e),
        }


# ============================================================================
# CLI entry-point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Inference with LoRA fine-tuned Qwen2.5-Math"
    )
    parser.add_argument(
        "--adapter-path", type=str, default=None,
        help="Path to LoRA adapter directory (default: auto-detect)"
    )
    parser.add_argument(
        "--question", "-q", type=str, default=None,
        help="Single question to solve (non-interactive)"
    )
    parser.add_argument(
        "--batch-file", type=str, default=None,
        help="JSON file with a list of questions to solve"
    )
    parser.add_argument(
        "--max-tokens", type=int, default=512,
        help="Maximum tokens to generate"
    )
    parser.add_argument(
        "--temperature", type=float, default=0.1,
        help="Sampling temperature"
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Output JSON file for batch results"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true",
        help="Run in interactive mode"
    )

    args = parser.parse_args()

    # Single question mode
    if args.question:
        result = solve_exercise(
            args.question,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            adapter_path=args.adapter_path,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # Batch mode
    if args.batch_file:
        with open(args.batch_file, "r", encoding="utf-8") as f:
            questions = json.load(f)
        if isinstance(questions, dict):
            questions = questions.get("questions", [])

        results = batch_solve(
            questions,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            adapter_path=args.adapter_path,
        )

        output_json = json.dumps(results, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_json)
            print(f"[batch] Results saved to {args.output}")
        else:
            print(output_json)
        return

    # Default: interactive mode
    interactive_mode(adapter_path=args.adapter_path)


if __name__ == "__main__":
    main()
