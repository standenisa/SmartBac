"""
Generate train/val/test JSONL splits from merged exercises.
Output: data/splits/finetune/{train,val,test}.jsonl (ChatML format for Qwen LoRA)
Output: data/splits/transformer/{train,val,test}.json (raw format for custom Transformer)
"""

import json
import os
import random

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MERGED_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "exercises_merged.json")

SYSTEM_PROMPT = (
    "Ești un asistent de matematică specializat pe exerciții BAC. "
    "Rezolvă exercițiul pas cu pas, explicând fiecare etapă."
)


def format_chatml(ex):
    """Convert exercise to ChatML format for Qwen fine-tuning."""
    question = ex.get("question", "")
    answer = ex.get("answer", "")
    steps = ex.get("solution_steps", [])
    solution = ex.get("solution", "")

    if not question or not answer:
        return None

    if steps and any(s.strip() for s in steps):
        steps_text = "\n".join(f"Pasul {i+1}: {s}" for i, s in enumerate(steps) if s.strip())
        response = f"{steps_text}\n\nRăspuns: {answer}"
    elif solution:
        response = f"{solution}\n\nRăspuns: {answer}"
    else:
        response = f"Răspuns: {answer}"

    return (
        f"<|im_start|>system\n{SYSTEM_PROMPT}\n<|im_end|>\n"
        f"<|im_start|>user\n{question}\n<|im_end|>\n"
        f"<|im_start|>assistant\n{response}\n<|im_end|>"
    )


def main():
    with open(MERGED_PATH, "r", encoding="utf-8") as f:
        exercises = json.load(f)
    print(f"Loaded {len(exercises)} exercises from {MERGED_PATH}")

    random.seed(42)
    indices = list(range(len(exercises)))
    random.shuffle(indices)

    n = len(exercises)
    n_train = int(0.8 * n)
    n_val = int(0.1 * n)

    train_idx = indices[:n_train]
    val_idx = indices[n_train:n_train + n_val]
    test_idx = indices[n_train + n_val:]

    # --- Finetune splits (ChatML JSONL) ---
    ft_dir = os.path.join(PROJECT_ROOT, "data", "splits", "finetune")
    os.makedirs(ft_dir, exist_ok=True)

    for name, idx_list in [("train", train_idx), ("val", val_idx), ("test", test_idx)]:
        path = os.path.join(ft_dir, f"{name}.jsonl")
        count = 0
        with open(path, "w", encoding="utf-8") as f:
            for i in idx_list:
                text = format_chatml(exercises[i])
                if text:
                    json.dump({"text": text}, f, ensure_ascii=False)
                    f.write("\n")
                    count += 1
        print(f"  finetune/{name}.jsonl: {count} samples")

    # --- Transformer splits (raw JSON) ---
    tf_dir = os.path.join(PROJECT_ROOT, "data", "splits", "transformer")
    os.makedirs(tf_dir, exist_ok=True)

    for name, idx_list in [("train", train_idx), ("val", val_idx), ("test", test_idx)]:
        path = os.path.join(tf_dir, f"{name}.json")
        split_data = [exercises[i] for i in idx_list]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(split_data, f, ensure_ascii=False, indent=2)
        print(f"  transformer/{name}.json: {len(split_data)} samples")

    print(f"\nSplits: {len(train_idx)} train / {len(val_idx)} val / {len(test_idx)} test")


if __name__ == "__main__":
    main()
