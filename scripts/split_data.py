#!/usr/bin/env python3
"""
split_data.py — Creează split-uri train/val/test din datele augmentate.

Produce 3 formate:
  1. data/splits/*.json          — Format brut (pentru backend/MongoDB)
  2. data/splits/transformer/    — Format Transformer: <BOS>q<SEP>answer<SEP>steps<EOS>
  3. data/splits/finetune/       — Format Qwen LoRA: ChatML instruction tuning

Split: 80% train / 10% validation / 10% test
Stratificat pe 'type' pentru distribuție echilibrată.

Utilizare:
    python scripts/split_data.py
"""
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

random.seed(42)

ROOT = Path(__file__).resolve().parent.parent
DATA_SRC = ROOT / "data" / "augmented" / "exercises_augmented.json"
DATA_RAW = ROOT / "data" / "raw" / "exercises_bac.json"
OUT = ROOT / "data" / "splits"

# ─── Load ───

def load_exercises():
    """Load all exercises, prefer augmented, fallback to raw."""
    if DATA_SRC.exists():
        with open(DATA_SRC, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[LOAD] {DATA_SRC.name}: {len(data)} exerciții")
    elif DATA_RAW.exists():
        with open(DATA_RAW, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[LOAD] {DATA_RAW.name}: {len(data)} exerciții (fallback)")
    else:
        print("[EROARE] Nu există date! Rulează mai întâi scripts/augment_data.py")
        sys.exit(1)

    # Validate
    valid = []
    for ex in data:
        q = ex.get("question", "").strip()
        a = str(ex.get("answer", "")).strip()
        if q and a:
            valid.append(ex)
    print(f"[VALID] {len(valid)} exerciții cu question + answer")
    return valid


# ─── Stratified Split ───

def stratified_split(data, train=0.80, val=0.10):
    """Split stratificat pe câmpul 'type' pentru distribuție echilibrată."""
    by_type = defaultdict(list)
    for ex in data:
        by_type[ex.get("type", "unknown")].append(ex)

    train_set, val_set, test_set = [], [], []

    for typ, exs in by_type.items():
        random.shuffle(exs)
        n = len(exs)
        n_train = max(1, int(n * train))
        n_val = max(1, int(n * val))
        # Rest goes to test
        train_set.extend(exs[:n_train])
        val_set.extend(exs[n_train:n_train + n_val])
        test_set.extend(exs[n_train + n_val:])

    # Shuffle final
    random.shuffle(train_set)
    random.shuffle(val_set)
    random.shuffle(test_set)

    return train_set, val_set, test_set


# ─── Format: Raw JSON ───

def save_raw(train, val, test):
    """Salvează split-urile ca JSON simplu."""
    out = OUT
    out.mkdir(parents=True, exist_ok=True)
    for name, data in [("train", train), ("val", val), ("test", test)]:
        path = out / f"{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  {name}.json: {len(data)} exerciții")


# ─── Format: Transformer ───

def _get_steps(ex):
    """Normalizează câmpul 'steps' la listă (poate fi și string multilinie)."""
    steps = ex.get("steps", [])
    if isinstance(steps, str):
        steps = [s.strip() for s in steps.split("\n") if s.strip()]
    return [str(s) for s in steps]


def format_transformer_seq(ex):
    """
    Formatul Transformer autoregresiv:
    <BOS> question <SEP> answer <SEP> step1 <SEP> step2 ... <EOS>

    Returnează dict cu câmpurile necesare pentru MathDataset.
    """
    question = ex.get("question", "")
    answer = str(ex.get("answer", ""))
    steps = _get_steps(ex)

    # Text complet (pentru referință)
    parts = [question, answer] + [str(s) for s in steps]
    text = " <SEP> ".join(parts)

    return {
        "question": question,
        "answer": answer,
        "steps": steps,
        "type": ex.get("type", "unknown"),
        "difficulty": ex.get("difficulty", 1),
        "text": text,
    }


def save_transformer(train, val, test):
    """Salvează în format Transformer."""
    out = OUT / "transformer"
    out.mkdir(parents=True, exist_ok=True)
    for name, data in [("train", train), ("val", val), ("test", test)]:
        formatted = [format_transformer_seq(ex) for ex in data]
        path = out / f"{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(formatted, f, ensure_ascii=False, indent=2)
        print(f"  transformer/{name}.json: {len(formatted)} secvențe")


# ─── Format: Qwen LoRA (ChatML) ───

def format_chatml(ex):
    """
    Format ChatML pentru Qwen fine-tuning:
    <|im_start|>system ... <|im_end|>
    <|im_start|>user ... <|im_end|>
    <|im_start|>assistant ... <|im_end|>
    """
    question = ex.get("question", "")
    answer = str(ex.get("answer", ""))
    steps = _get_steps(ex)

    # Build response
    if steps:
        steps_text = "\n".join(
            f"Pasul {i}: " + re.sub(r"^(?:Step|Pasul)\s*\d+\s*:\s*", "", s)
            for i, s in enumerate(steps, 1)
        )
        response = f"{steps_text}\n\nRăspuns: {answer}"
    else:
        response = f"Răspuns: {answer}"

    text = (
        "<|im_start|>system\n"
        "Ești un asistent de matematică specializat pe exerciții BAC. "
        "Rezolvă exercițiul pas cu pas, explicând fiecare etapă.\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"{question}\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
        f"{response}\n"
        "<|im_end|>"
    )
    return {"text": text}


def save_finetune(train, val, test):
    """Salvează în format JSONL pentru Qwen LoRA fine-tuning."""
    out = OUT / "finetune"
    out.mkdir(parents=True, exist_ok=True)
    for name, data in [("train", train), ("val", val), ("test", test)]:
        path = out / f"{name}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for ex in data:
                json.dump(format_chatml(ex), f, ensure_ascii=False)
                f.write("\n")
        print(f"  finetune/{name}.jsonl: {len(data)} samples")


# ─── Stats ───

def print_stats(name, data):
    by_type = defaultdict(int)
    by_diff = defaultdict(int)
    for ex in data:
        by_type[ex.get("type", "?")] += 1
        by_diff[ex.get("difficulty", "?")] += 1
    print(f"\n  {name} ({len(data)} total):")
    print(f"    Per tip:  {dict(sorted(by_type.items(), key=lambda x: -x[1]))}")
    print(f"    Per diff: {dict(sorted(by_diff.items()))}")


# ─── Main ───

def main():
    print("=" * 60)
    print("  SPLIT DATE BAC PREP AI")
    print("  Train (80%) / Validation (10%) / Test (10%)")
    print("=" * 60)

    exercises = load_exercises()

    # Split stratificat
    train, val, test = stratified_split(exercises)

    print(f"\n[SPLIT] Train: {len(train)} | Val: {len(val)} | Test: {len(test)}")

    # Stats
    print_stats("Train", train)
    print_stats("Val", val)
    print_stats("Test", test)

    # 1. Raw JSON
    print(f"\n[1/3] Salvare JSON brut → {OUT}/")
    save_raw(train, val, test)

    # 2. Transformer format
    print(f"\n[2/3] Salvare format Transformer → {OUT}/transformer/")
    save_transformer(train, val, test)

    # 3. Qwen LoRA ChatML format
    print(f"\n[3/3] Salvare format Qwen LoRA → {OUT}/finetune/")
    save_finetune(train, val, test)

    print(f"\n{'=' * 60}")
    print(f"GATA! Structura finală:")
    print(f"  data/splits/")
    print(f"  ├── train.json          ({len(train)} ex, pt backend/MongoDB)")
    print(f"  ├── val.json            ({len(val)} ex)")
    print(f"  ├── test.json           ({len(test)} ex)")
    print(f"  ├── transformer/")
    print(f"  │   ├── train.json      ({len(train)} secvențe, pt ai/transformer/train.py)")
    print(f"  │   ├── val.json        ({len(val)} secvențe)")
    print(f"  │   └── test.json       ({len(test)} secvențe)")
    print(f"  └── finetune/")
    print(f"      ├── train.jsonl     ({len(train)} ChatML, pt ai/finetune/train_mlx.py)")
    print(f"      ├── val.jsonl       ({len(val)} ChatML)")
    print(f"      └── test.jsonl      ({len(test)} ChatML)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
