"""
Train Qwen2.5-VL-3B cu LoRA pe exerciții BAC (imagini).

Design pt Kaggle T4 (16GB VRAM):
  - Qwen2.5-VL-3B-Instruct cu 4-bit quantization
  - LoRA rank=16 DOAR pe LLM layers (vision encoder înghețat)
  - Gradient checkpointing + accumulation
  - bf16 mixed precision

Usage pe Kaggle:
    !pip install transformers trl peft bitsandbytes accelerate qwen-vl-utils pillow
    !python train_vlm.py --data_dir /kaggle/input/bac-vision --output_dir /kaggle/working/vlm-lora

Usage local (testing):
    python ai/finetune/train_vlm.py --data_dir data/vision --output_dir ai/finetune/adapters/vlm-lora --max_steps 10
"""

import json
import argparse
from pathlib import Path

import torch
from PIL import Image
from datasets import Dataset

from transformers import (
    Qwen2_5_VLForConditionalGeneration,
    AutoProcessor,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig


# ─── Config defaults ───

MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"

LORA_CONFIG = dict(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    task_type="CAUSAL_LM",
)

QUANT_CONFIG = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)


def load_dataset_from_jsonl(jsonl_path: str) -> Dataset:
    """Load vision dataset from JSONL file."""
    samples = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            samples.append(item)
    return Dataset.from_list(samples)


def build_messages(sample: dict) -> list[dict]:
    """Convert dataset sample to Qwen2.5-VL message format."""
    messages = [
        {
            "role": "system",
            # Must stay in sync with SYSTEM_PROMPT in ai/finetune/inference_vlm.py
            # (duplicated so this script can run standalone on Kaggle).
            "content": (
                "Ești SmartBAC, un tutore expert de matematică pentru Bacalaureatul din România. "
                "Citești exercițiul din imagine și îl rezolvi pas cu pas. "
                "Răspunde DOAR în limba română. "
                "Format: Pasul 1: ... Pasul 2: ... Răspuns: ..."
            ),
        }
    ]

    for turn in sample["conversations"]:
        if turn["role"] == "user":
            content_parts = []
            if "<image>" in turn["content"]:
                content_parts.append({"type": "image", "image": sample["image"]})
                text = turn["content"].replace("<image>", "").strip()
            else:
                text = turn["content"]
            if text:
                content_parts.append({"type": "text", "text": text})
            messages.append({"role": "user", "content": content_parts})
        else:
            messages.append({
                "role": "assistant",
                "content": turn["content"]
            })

    return messages


def collate_fn(batch, processor):
    """Custom collate function for VLM training."""
    all_messages = []
    all_images = []

    for sample in batch:
        messages = build_messages(sample)

        # Load image
        img_path = sample["image"]
        try:
            img = Image.open(img_path).convert("RGB")
            all_images.append(img)
        except Exception as e:
            print(f"[WARN] Can't load {img_path}: {e}")
            continue

        all_messages.append(messages)

    if not all_messages:
        return None

    # Apply chat template
    texts = [
        processor.apply_chat_template(m, tokenize=False, add_generation_prompt=False)
        for m in all_messages
    ]

    # Process with Qwen2.5-VL processor
    inputs = processor(
        text=texts,
        images=all_images,
        padding=True,
        truncation=True,
        max_length=2048,
        return_tensors="pt",
    )

    # Labels = input_ids with padding tokens masked
    labels = inputs["input_ids"].clone()
    labels[labels == processor.tokenizer.pad_token_id] = -100

    inputs["labels"] = labels
    return inputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="data/vision")
    parser.add_argument("--output_dir", default="ai/finetune/adapters/vlm-lora")
    parser.add_argument("--model_id", default=MODEL_ID)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch_size", type=int, default=2)
    parser.add_argument("--grad_accum", type=int, default=8)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--max_steps", type=int, default=-1)
    parser.add_argument("--push_to_hub", type=str, default=None)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ─── Load model ───

    print(f"Loading {args.model_id} with 4-bit quantization...")
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        args.model_id,
        quantization_config=QUANT_CONFIG,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        attn_implementation="flash_attention_2" if torch.cuda.is_available() else "eager",
    )

    processor = AutoProcessor.from_pretrained(args.model_id)
    if processor.tokenizer.pad_token is None:
        processor.tokenizer.pad_token = processor.tokenizer.eos_token

    # ─── Freeze vision encoder ───

    for name, param in model.named_parameters():
        if "visual" in name:
            param.requires_grad = False

    # ─── LoRA ───

    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)
    lora_config = LoraConfig(**LORA_CONFIG)
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # ─── Datasets ───

    train_path = data_dir / "train.jsonl"
    val_path = data_dir / "val.jsonl"

    if not train_path.exists():
        raise FileNotFoundError(f"Train file not found: {train_path}")

    train_ds = load_dataset_from_jsonl(str(train_path))
    val_ds = load_dataset_from_jsonl(str(val_path)) if val_path.exists() else None

    print(f"Train: {len(train_ds)} samples")
    if val_ds:
        print(f"Val:   {len(val_ds)} samples")

    # ─── Training config ───

    effective_batch = args.batch_size * args.grad_accum
    total_steps = (len(train_ds) * args.epochs) // effective_batch if args.max_steps < 0 else args.max_steps
    warmup_steps = max(1, int(total_steps * 0.03))

    training_args = SFTConfig(
        output_dir=str(output_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=args.grad_accum,
        gradient_checkpointing=True,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_steps=warmup_steps,
        weight_decay=0.01,
        bf16=True,
        logging_steps=10,
        save_strategy="epoch",
        eval_strategy="epoch" if val_ds else "no",
        save_total_limit=2,
        max_steps=args.max_steps if args.max_steps > 0 else -1,
        remove_unused_columns=False,
        dataloader_pin_memory=False,
        report_to="none",
        max_seq_length=2048,
        dataset_text_field="",
        dataset_kwargs={"skip_prepare_dataset": True},
    )

    # ─── Trainer ───

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        processing_class=processor.tokenizer,
        data_collator=lambda batch: collate_fn(batch, processor),
    )

    # ─── Train ───

    print(f"\n{'='*50}")
    print(f"Training Qwen2.5-VL-3B + LoRA")
    print(f"  Effective batch: {effective_batch}")
    print(f"  Steps: ~{total_steps}")
    print(f"  Warmup: {warmup_steps}")
    print(f"  LR: {args.lr}")
    print(f"{'='*50}\n")

    trainer.train()

    # ─── Save ───

    model.save_pretrained(str(output_dir))
    processor.save_pretrained(str(output_dir))
    print(f"\nLoRA adapter saved to: {output_dir}")

    if args.push_to_hub:
        print(f"Pushing to Hub: {args.push_to_hub}")
        model.push_to_hub(args.push_to_hub)
        processor.push_to_hub(args.push_to_hub)
        print("Done!")

    # ─── Training stats ───

    if trainer.state.log_history:
        final = [l for l in trainer.state.log_history if "train_loss" in l]
        if final:
            print(f"\nFinal train loss: {final[-1]['train_loss']:.4f}")
        eval_logs = [l for l in trainer.state.log_history if "eval_loss" in l]
        if eval_logs:
            print(f"Final eval loss:  {eval_logs[-1]['eval_loss']:.4f}")


if __name__ == "__main__":
    main()
