#!/usr/bin/env python3
"""
Training script for the MathBPETokenizer.

Loads exercise data from the project's data directory, extracts all textual
content (questions, answers, solution steps, LaTeX fragments), trains a BPE
tokenizer, saves it to disk, and prints diagnostic statistics.
"""

import json
import os
import sys
import time

# ---------------------------------------------------------------------------
# Resolve project root so imports work when the script is executed directly.
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from ai.tokenizer.bpe import MathBPETokenizer

# ---------------------------------------------------------------------------
# Paths (relative to project root)
# ---------------------------------------------------------------------------
AUGMENTED_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "augmented_exercises.json")
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "exercises_bac.json")
TOKENIZER_SAVE_PATH = os.path.join(PROJECT_ROOT, "ai", "tokenizer", "math_bpe.json")


# ===================================================================
# Data loading helpers
# ===================================================================

def load_data() -> list[dict]:
    """Load exercise data, falling back from augmented to raw."""
    if os.path.isfile(AUGMENTED_DATA_PATH):
        print(f"[DATA] Loading augmented data from {AUGMENTED_DATA_PATH}")
        with open(AUGMENTED_DATA_PATH, "r", encoding="utf-8") as fh:
            return json.load(fh)

    if os.path.isfile(RAW_DATA_PATH):
        print(f"[DATA] Augmented data not found. Falling back to {RAW_DATA_PATH}")
        with open(RAW_DATA_PATH, "r", encoding="utf-8") as fh:
            return json.load(fh)

    print("[DATA] ERROR: No data files found. Looked in:")
    print(f"       - {AUGMENTED_DATA_PATH}")
    print(f"       - {RAW_DATA_PATH}")
    sys.exit(1)


def extract_texts(data: list[dict]) -> list[str]:
    """Recursively extract every string value from the exercise data."""
    texts: list[str] = []

    def _recurse(obj):
        if isinstance(obj, str):
            stripped = obj.strip()
            if stripped:
                texts.append(stripped)
        elif isinstance(obj, list):
            for item in obj:
                _recurse(item)
        elif isinstance(obj, dict):
            for value in obj.values():
                _recurse(value)

    _recurse(data)
    return texts


# ===================================================================
# Statistics
# ===================================================================

def print_vocab_stats(tokenizer: MathBPETokenizer) -> None:
    """Print informative statistics about the trained vocabulary."""
    total = len(tokenizer)

    # Count LaTeX tokens present in the vocabulary
    latex_in_vocab = [t for t in tokenizer.LATEX_TOKENS if t in tokenizer.vocab]

    # Count operator tokens present
    ops_in_vocab = [t for t in tokenizer.MATH_OPERATORS if t in tokenizer.vocab]

    # Count special tokens
    specials_in_vocab = [t for t in tokenizer.SPECIAL_TOKENS if t in tokenizer.vocab]

    # Merge-created tokens (everything else)
    reserved = (
        set(tokenizer.SPECIAL_TOKENS.keys())
        | set(tokenizer.LATEX_TOKENS)
        | set(tokenizer.MATH_OPERATORS)
    )
    merge_tokens = [t for t in tokenizer.vocab if t not in reserved and len(t) > 1]

    print("\n" + "=" * 60)
    print("  VOCABULARY STATISTICS")
    print("=" * 60)
    print(f"  Total tokens          : {total}")
    print(f"  Special tokens        : {len(specials_in_vocab)}")
    print(f"  LaTeX tokens          : {len(latex_in_vocab)} / {len(tokenizer.LATEX_TOKENS)}")
    print(f"  Operator tokens       : {len(ops_in_vocab)} / {len(tokenizer.MATH_OPERATORS)}")
    print(f"  Merge-created tokens  : {len(merge_tokens)}")
    print(f"  Total merge rules     : {len(tokenizer.merges)}")
    print("=" * 60)


def test_encode_decode(tokenizer: MathBPETokenizer) -> None:
    """Run a handful of sample encode/decode round-trips."""
    samples = [
        r"Rezolvati ecuatia: x^2 + 3x - 4 = 0",
        r"\frac{1}{2} + \frac{3}{4} = \frac{5}{4}",
        r"\int_0^1 x^2 dx = \frac{1}{3}",
        r"\lim_{x \rightarrow \infty} \frac{1}{x} = 0",
        r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}",
        r"\sqrt{a^2 + b^2}",
        r"Calculati \log_2 8 = 3",
        r"Daca f(x) = \sin x + \cos x, atunci f'(x) = \cos x - \sin x",
    ]

    print("\n" + "=" * 60)
    print("  ENCODE / DECODE SAMPLES")
    print("=" * 60)
    for text in samples:
        ids = tokenizer.encode(text)
        decoded = tokenizer.decode(ids)
        match = "OK" if decoded == text else "MISMATCH"
        print(f"\n  [{match}] Original : {text}")
        print(f"         Tokens   : {len(ids)} ids")
        print(f"         IDs      : {ids[:20]}{'...' if len(ids) > 20 else ''}")
        print(f"         Decoded  : {decoded}")
    print("=" * 60)


# ===================================================================
# Main
# ===================================================================

def main() -> None:
    print("=" * 60)
    print("  Math BPE Tokenizer -- Training Script")
    print("=" * 60)

    # 1. Load data -----------------------------------------------------------
    data = load_data()
    texts = extract_texts(data)
    print(f"[DATA] Extracted {len(texts)} text fragments from the dataset.")

    # 2. Create tokenizer ----------------------------------------------------
    tokenizer = MathBPETokenizer(vocab_size=8192)

    # 3. Train ---------------------------------------------------------------
    t0 = time.time()
    tokenizer.train(texts, verbose=True)
    elapsed = time.time() - t0
    print(f"[BPE] Training took {elapsed:.2f}s")

    # 4. Save ----------------------------------------------------------------
    os.makedirs(os.path.dirname(TOKENIZER_SAVE_PATH), exist_ok=True)
    tokenizer.save(TOKENIZER_SAVE_PATH)
    print(f"[BPE] Tokenizer saved to {TOKENIZER_SAVE_PATH}")

    # 5. Test ----------------------------------------------------------------
    test_encode_decode(tokenizer)

    # 6. Stats ---------------------------------------------------------------
    print_vocab_stats(tokenizer)

    # 7. Quick coverage estimate ---------------------------------------------
    #    Encode the entire corpus and count <UNK> tokens.
    total_tokens = 0
    unk_tokens = 0
    unk_id = tokenizer.SPECIAL_TOKENS["<UNK>"]
    for text in texts:
        ids = tokenizer.encode(text)
        total_tokens += len(ids)
        unk_tokens += ids.count(unk_id)

    if total_tokens > 0:
        coverage = (1.0 - unk_tokens / total_tokens) * 100
    else:
        coverage = 0.0
    print(f"\n  Corpus coverage : {coverage:.2f}%  "
          f"({unk_tokens} UNK out of {total_tokens} tokens)")


if __name__ == "__main__":
    main()
