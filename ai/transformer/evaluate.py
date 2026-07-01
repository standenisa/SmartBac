"""
Script de evaluare pentru MathTransformer autoregresiv.

Metrici:
    - Exact match accuracy (răspunsul generat == răspunsul corect)
    - Partial match accuracy (overlap tokeni >= 50%)
    - BLEU-4 score (implementat de la zero, fără dependențe externe)
    - Breakdown per tip de exercițiu

Utilizare:
    python -m ai.transformer.evaluate
    python -m ai.transformer.evaluate --checkpoint path/to/model.pt --data path/to/data.json
"""

import json
import math
import sys
import argparse
from pathlib import Path
from collections import Counter, defaultdict

import torch

# ── Importuri proiect ──
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from ai.tokenizer.bpe import MathBPETokenizer
from ai.transformer.model import MathTransformer
from ai.transformer.generate import pick_device


# ═══════════════════════════════════════════════════════════════════════
# BLEU-4 (implementat de la zero, cu smoothing)
# ═══════════════════════════════════════════════════════════════════════

def _count_ngrams(tokens: list[str], n: int) -> Counter:
    """Numără toate n-gramele dintr-o listă de tokeni."""
    return Counter(tuple(tokens[i: i + n]) for i in range(len(tokens) - n + 1))


def _brevity_penalty(ref_len: int, hyp_len: int) -> float:
    """Penalizare pentru ipoteze mai scurte decât referința."""
    if hyp_len == 0:
        return 0.0
    if hyp_len >= ref_len:
        return 1.0
    return math.exp(1 - ref_len / hyp_len)


def calculate_bleu(
    references: list[str],
    hypotheses: list[str],
    max_n: int = 4,
) -> float:
    """
    BLEU-N la nivel de corpus cu smoothing +1.

    Args:
        references:  Lista de referințe (texte corecte).
        hypotheses:  Lista de ipoteze (texte generate).
        max_n:       Ordinul maxim de n-grame (4 = BLEU-4).

    Returns:
        Scorul BLEU în [0, 1].
    """
    clipped = [0] * max_n
    total = [0] * max_n
    ref_len = 0
    hyp_len = 0

    for ref_str, hyp_str in zip(references, hypotheses):
        ref_tokens = ref_str.split()
        hyp_tokens = hyp_str.split()
        ref_len += len(ref_tokens)
        hyp_len += len(hyp_tokens)

        for n in range(1, max_n + 1):
            ref_ngrams = _count_ngrams(ref_tokens, n)
            hyp_ngrams = _count_ngrams(hyp_tokens, n)
            for ngram, count in hyp_ngrams.items():
                clipped[n - 1] += min(count, ref_ngrams.get(ngram, 0))
            total[n - 1] += max(len(hyp_tokens) - n + 1, 0)

    log_prec = 0.0
    for n in range(max_n):
        num = clipped[n] + (1 if n > 0 else 0)
        den = total[n] + (1 if n > 0 else 0)
        if den == 0 or num == 0:
            return 0.0
        log_prec += math.log(num / den)

    log_prec /= max_n
    bp = _brevity_penalty(ref_len, hyp_len)
    return bp * math.exp(log_prec)


# ═══════════════════════════════════════════════════════════════════════
# Evaluare
# ═══════════════════════════════════════════════════════════════════════

def evaluate_model(
    checkpoint_path: str,
    data_path: str,
    tokenizer_path: str,
) -> dict:
    """
    Evaluează un checkpoint pe un set de date.

    Procesul:
        1. Încarcă model + tokenizer
        2. Pentru fiecare exercițiu: generează răspunsul
        3. Compară cu ground truth
        4. Calculează metrici

    Returns:
        Dict cu exact_match, partial_match, bleu4, per_type.
    """
    # ── Device ──
    device = pick_device()
    print(f"[DEVICE] {device}")

    # ── Tokenizer ──
    tokenizer = MathBPETokenizer()
    tokenizer.load(tokenizer_path)
    print(f"[TOKENIZER] {len(tokenizer)} tokeni")

    # ── Model ──
    model = MathTransformer.from_pretrained(checkpoint_path, device=str(device))
    print(f"[MODEL] Încărcat din {checkpoint_path}")

    # ── Date ──
    with open(data_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    print(f"[DATE] {len(raw_data)} exerciții")

    # ── Generare + comparare ──
    bos_idx = MathBPETokenizer.SPECIAL_TOKENS["<BOS>"]
    sep_idx = MathBPETokenizer.SPECIAL_TOKENS["<SEP>"]
    eos_idx = MathBPETokenizer.SPECIAL_TOKENS["<EOS>"]
    pad_idx = MathBPETokenizer.SPECIAL_TOKENS["<PAD>"]

    references = []
    hypotheses = []
    exact = 0
    partial = 0
    type_stats = defaultdict(lambda: {"exact": 0, "partial": 0, "total": 0})

    print("[EVAL] Generare răspunsuri...")
    for i, item in enumerate(raw_data):
        question = item.get("question", "")
        answer = str(item.get("answer", ""))

        # Tokenizăm prompt-ul
        prompt_ids = [bos_idx] + tokenizer.encode(question) + [sep_idx]
        inp = torch.tensor([prompt_ids], dtype=torch.long).to(device)

        # Generăm
        out = model.generate(inp, max_new_tokens=100, temperature=0.3, top_k=20)
        gen_ids = out[0].tolist()[len(prompt_ids):]

        # Păstrăm doar răspunsul: ne oprim la primul separator
        # (modelul generează "răspuns <SEP> pas1 <SEP> ... <EOS>")
        clean = []
        for tid in gen_ids:
            if tid in (eos_idx, pad_idx, sep_idx):
                break
            clean.append(tid)

        hyp = tokenizer.decode(clean).strip()
        ref = answer.strip()

        references.append(ref)
        hypotheses.append(hyp)

        is_exact = ref == hyp
        ref_tokens = set(ref.split())
        hyp_tokens = set(hyp.split())
        is_partial = bool(ref_tokens) and len(ref_tokens & hyp_tokens) / len(ref_tokens) >= 0.5

        ex_type = item.get("type", "unknown")
        type_stats[ex_type]["total"] += 1
        if is_exact:
            exact += 1
            type_stats[ex_type]["exact"] += 1
        if is_partial:
            partial += 1
            type_stats[ex_type]["partial"] += 1

        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(raw_data)}...")

    total = len(raw_data)
    bleu = calculate_bleu(references, hypotheses)

    print(f"\n  Exact match:   {exact}/{total} ({exact/total:.1%})")
    print(f"  Partial match: {partial}/{total} ({partial/total:.1%})")
    print(f"  BLEU-4:        {bleu:.4f}")

    return {
        "exact_match": exact / max(total, 1),
        "partial_match": partial / max(total, 1),
        "bleu4": bleu,
        "total_samples": total,
        "per_type": {k: dict(v) for k, v in type_stats.items()},
    }


def main():
    project_root = _PROJECT_ROOT

    parser = argparse.ArgumentParser(description="Evaluare MathTransformer")
    parser.add_argument("--checkpoint", default=str(
        project_root / "ai" / "transformer" / "checkpoints" / "best_model.pt"
    ))
    parser.add_argument("--data", default=str(
        project_root / "data" / "raw" / "exercises_bac.json"
    ))
    parser.add_argument("--tokenizer", default=str(
        project_root / "ai" / "tokenizer" / "math_bpe.json"
    ))
    args = parser.parse_args()

    results = evaluate_model(args.checkpoint, args.data, args.tokenizer)

    results_path = project_root / "ai" / "transformer" / "checkpoints" / "eval_results.json"
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nRezultate salvate în {results_path}")


if __name__ == "__main__":
    main()
