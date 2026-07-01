# ============================================================
# SmartBAC VLM — Qwen2.5-VL-3B + LoRA Fine-tuning
# Kaggle Notebook (GPU T4)
# ============================================================
# Celula 1: Instalare dependințe
# ============================================================

# !pip install -q transformers>=4.45.0 trl>=0.12.0 peft>=0.13.0 \
#     bitsandbytes>=0.44.0 accelerate>=1.0.0 qwen-vl-utils Pillow datasets

# ============================================================
# Celula 2: Imports + Config
# ============================================================

import os
import json
import torch
from pathlib import Path
from PIL import Image
from datasets import Dataset
from transformers import (
    Qwen2_5_VLForConditionalGeneration,
    AutoProcessor,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig

# ── Paths ──
DATA_DIR = Path("/kaggle/input/smartbac-vlm-data")
OUTPUT_DIR = Path("/kaggle/working/vlm-lora")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"
HF_REPO = "denisastan/smartbac-vlm-lora"  # schimbă dacă vrei alt nume

print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB")

# ============================================================
# Celula 3: Load Dataset
# ============================================================

def load_jsonl(path):
    samples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                # Fix image path pt Kaggle
                item["image"] = str(DATA_DIR / item["image"])
                samples.append(item)
    return Dataset.from_list(samples)

train_ds = load_jsonl(DATA_DIR / "train.jsonl")
val_ds = load_jsonl(DATA_DIR / "val.jsonl")

print(f"Train: {len(train_ds)} samples")
print(f"Val:   {len(val_ds)} samples")

# Quick sanity check
sample = train_ds[0]
img = Image.open(sample["image"])
print(f"Sample image: {img.size}, conversations: {len(sample['conversations'])}")

# ============================================================
# Celula 4: Load Model + LoRA
# ============================================================

QUANT_CONFIG = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

print(f"Loading {MODEL_ID}...")
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    MODEL_ID,
    quantization_config=QUANT_CONFIG,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)

processor = AutoProcessor.from_pretrained(MODEL_ID)
if processor.tokenizer.pad_token is None:
    processor.tokenizer.pad_token = processor.tokenizer.eos_token

# Freeze vision encoder (antrenăm doar LLM-ul)
for name, param in model.named_parameters():
    if "visual" in name:
        param.requires_grad = False

# LoRA config
model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                     "gate_proj", "up_proj", "down_proj"],
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# ============================================================
# Celula 5: Collate Function
# ============================================================

SYSTEM_PROMPT = (
    "Ești SmartBAC, un tutore expert de matematică pentru Bacalaureatul din România. "
    "Citești exercițiul din imagine și îl rezolvi pas cu pas. "
    "Răspunde DOAR în limba română. "
    "Format: Pasul 1: ... Pasul 2: ... Răspuns: ..."
)

def build_messages(sample):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in sample["conversations"]:
        if turn["role"] == "user":
            parts = []
            if "<image>" in turn["content"]:
                parts.append({"type": "image", "image": sample["image"]})
                text = turn["content"].replace("<image>", "").strip()
            else:
                text = turn["content"]
            if text:
                parts.append({"type": "text", "text": text})
            messages.append({"role": "user", "content": parts})
        else:
            messages.append({"role": "assistant", "content": turn["content"]})
    return messages

def collate_fn(batch):
    all_messages, all_images = [], []
    for sample in batch:
        try:
            img = Image.open(sample["image"]).convert("RGB")
        except Exception as e:
            print(f"[SKIP] {sample['image']}: {e}")
            continue
        all_messages.append(build_messages(sample))
        all_images.append(img)

    if not all_messages:
        return None

    texts = [
        processor.apply_chat_template(m, tokenize=False, add_generation_prompt=False)
        for m in all_messages
    ]
    inputs = processor(
        text=texts, images=all_images,
        padding=True, truncation=True, max_length=2048,
        return_tensors="pt",
    )
    labels = inputs["input_ids"].clone()
    labels[labels == processor.tokenizer.pad_token_id] = -100
    inputs["labels"] = labels
    return inputs

# ============================================================
# Celula 6: Training
# ============================================================

EPOCHS = 2
BATCH_SIZE = 2
GRAD_ACCUM = 8
LR = 1e-4

effective_batch = BATCH_SIZE * GRAD_ACCUM
total_steps = (len(train_ds) * EPOCHS) // effective_batch
warmup_steps = max(1, int(total_steps * 0.03))

print(f"Effective batch: {effective_batch}")
print(f"Total steps: ~{total_steps}")
print(f"Warmup: {warmup_steps}")

training_args = SFTConfig(
    output_dir=str(OUTPUT_DIR),
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=GRAD_ACCUM,
    gradient_checkpointing=True,
    learning_rate=LR,
    lr_scheduler_type="cosine",
    warmup_steps=warmup_steps,
    weight_decay=0.01,
    bf16=True,
    logging_steps=10,
    save_strategy="epoch",
    eval_strategy="epoch",
    save_total_limit=2,
    remove_unused_columns=False,
    dataloader_pin_memory=False,
    report_to="none",
    max_seq_length=2048,
    dataset_text_field="",
    dataset_kwargs={"skip_prepare_dataset": True},
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    processing_class=processor.tokenizer,
    data_collator=collate_fn,
)

print(f"\n{'='*50}")
print(f"  Training Qwen2.5-VL-3B + LoRA")
print(f"  {len(train_ds)} train / {len(val_ds)} val")
print(f"  ~{total_steps} steps, {EPOCHS} epochs")
print(f"{'='*50}\n")

trainer.train()

# ============================================================
# Celula 7: Save + Push to Hub
# ============================================================

model.save_pretrained(str(OUTPUT_DIR))
processor.save_pretrained(str(OUTPUT_DIR))
print(f"Saved to {OUTPUT_DIR}")

# Training curves
if trainer.state.log_history:
    train_losses = [l for l in trainer.state.log_history if "loss" in l and "eval" not in str(l.keys())]
    eval_losses = [l for l in trainer.state.log_history if "eval_loss" in l]
    if train_losses:
        print(f"Final train loss: {train_losses[-1].get('loss', 'N/A')}")
    if eval_losses:
        print(f"Final eval loss:  {eval_losses[-1]['eval_loss']:.4f}")

# ============================================================
# Celula 8: Push to HuggingFace Hub (opțional)
# ============================================================

# Decomentează și adaugă token-ul tău HF:
# from huggingface_hub import login
# login(token="hf_YOUR_TOKEN_HERE")
# model.push_to_hub(HF_REPO)
# processor.push_to_hub(HF_REPO)
# print(f"Pushed to https://huggingface.co/{HF_REPO}")

# ============================================================
# Celula 9: Test rapid pe o imagine
# ============================================================

test_sample = val_ds[0]
test_img = Image.open(test_sample["image"]).convert("RGB")

test_messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": [
        {"type": "image", "image": test_img},
        {"type": "text", "text": "Rezolvă exercițiul din imagine."},
    ]},
]

text_prompt = processor.apply_chat_template(test_messages, tokenize=False, add_generation_prompt=True)
inputs = processor(text=[text_prompt], images=[test_img], return_tensors="pt", padding=True)
inputs = {k: v.to(model.device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}

with torch.no_grad():
    output_ids = model.generate(**inputs, max_new_tokens=512, temperature=0.3, do_sample=True, top_p=0.9)

input_len = inputs["input_ids"].shape[1]
response = processor.tokenizer.decode(output_ids[0][input_len:], skip_special_tokens=True)

print("=" * 50)
print("EXPECTED:")
print(test_sample["conversations"][1]["content"][:300])
print("\nMODEL OUTPUT:")
print(response[:300])
print("=" * 50)
