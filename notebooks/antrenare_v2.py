# ============================================================
# SmartBAC — Qwen2.5-Math-7B + QLoRA (Kaggle T4)
# Model mai mic = termină în ~4-6 ore garantat
# ============================================================

# CELULA 1 — Instalare
# !pip install -q transformers>=4.45.0 peft>=0.13.0 bitsandbytes>=0.44.0 accelerate>=1.0.0 datasets trl

# ============================================================
# CELULA 2 — Setup
# ============================================================

from kaggle_secrets import UserSecretsClient
from huggingface_hub import login

user_secrets = UserSecretsClient()
secret_hf_token = user_secrets.get_secret("HF_TOKEN")
login(secret_hf_token)

import torch
import json
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# MODEL MIC — termină în timp pe T4
MODEL_ID = "Qwen/Qwen2.5-Math-7B-Instruct"
HF_REPO = "denisastan/bac-math-qwen-lora"

print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

# ============================================================
# CELULA 3 — Dataset
# ============================================================

data_path = "/kaggle/input/smartbac-vlm-data/train.jsonl"

# Citim JSONL și extragem text
samples = []
with open(data_path, "r") as f:
    for line in f:
        item = json.loads(line.strip())
        convs = item.get("conversations", [])
        if len(convs) >= 2:
            question = convs[0]["content"].replace("<image>\n", "").strip()
            answer = convs[1]["content"].strip()
            if question and answer:
                samples.append({"question": question, "answer": answer})

print(f"Total samples: {len(samples)}")

# Formatare ChatML
SYSTEM_PROMPT = (
    "Ești SmartBAC, un asistent de matematică specializat pe exerciții de Bacalaureat. "
    "Gândește pas cu pas în blocul <think>, apoi dă răspunsul final. "
    "Răspunde în limba română."
)

def format_sample(ex):
    text = (
        f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n"
        f"<|im_start|>user\n{ex['question']}<|im_end|>\n"
        f"<|im_start|>assistant\n<think>\n{ex['answer']}\n</think>\n\nRăspuns: {ex['answer'].split('Răspuns:')[-1].strip() if 'Răspuns:' in ex['answer'] else ex['answer']}<|im_end|>"
    )
    return {"text": text}

from datasets import Dataset
dataset = Dataset.from_list(samples)
dataset = dataset.map(format_sample)
dataset = dataset.train_test_split(test_size=0.05, seed=42)

print(f"Train: {len(dataset['train'])}")
print(f"Test:  {len(dataset['test'])}")
print(f"\nExemplu:\n{dataset['train'][0]['text'][:500]}")

# ============================================================
# CELULA 4 — Model + LoRA
# ============================================================

print(f"\nLoading {MODEL_ID}...")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    attn_implementation="eager",
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)

peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                     "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# ============================================================
# CELULA 5 — Tokenizare
# ============================================================

def tokenize_fn(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=1024,
        padding="max_length",
    )

tokenized_train = dataset["train"].map(tokenize_fn, batched=True, remove_columns=dataset["train"].column_names)
tokenized_test = dataset["test"].map(tokenize_fn, batched=True, remove_columns=dataset["test"].column_names)

# Labels = input_ids (pentru causal LM)
def add_labels(examples):
    examples["labels"] = examples["input_ids"].copy()
    return examples

tokenized_train = tokenized_train.map(add_labels, batched=True)
tokenized_test = tokenized_test.map(add_labels, batched=True)

print(f"Tokenized train: {len(tokenized_train)}")
print(f"Tokenized test: {len(tokenized_test)}")

# ============================================================
# CELULA 6 — Training (3 epoci)
# ============================================================

training_args = TrainingArguments(
    output_dir="./rezultate_AI",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=8,
    gradient_checkpointing=True,
    learning_rate=5e-5,
    num_train_epochs=3,
    logging_steps=20,
    eval_strategy="steps",
    eval_steps=100,
    save_strategy="epoch",
    save_total_limit=2,
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    optim="paged_adamw_8bit",
    bf16=True,
    report_to="none",
    remove_unused_columns=False,
    dataloader_pin_memory=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
)

effective_batch = 2 * 8
total_steps = (len(tokenized_train) * 3) // effective_batch
print(f"\n{'='*50}")
print(f"  Training {MODEL_ID}")
print(f"  {len(tokenized_train)} train / {len(tokenized_test)} test")
print(f"  Effective batch: {effective_batch}")
print(f"  Total steps: ~{total_steps}")
print(f"  Epochs: 3")
print(f"{'='*50}\n")

trainer.train()

# ============================================================
# CELULA 7 — Save + Push
# ============================================================

model.save_pretrained("./rezultate_AI/final")
tokenizer.save_pretrained("./rezultate_AI/final")

model.push_to_hub(HF_REPO)
tokenizer.push_to_hub(HF_REPO)
print(f"\nModel salvat și publicat: https://huggingface.co/{HF_REPO}")

# ============================================================
# CELULA 8 — Grafice
# ============================================================

import matplotlib.pyplot as plt
import numpy as np

istoric = trainer.state.log_history
pasi_train, loss_train = [], []
pasi_eval, loss_eval = [], []

for log in istoric:
    if "loss" in log and "eval_loss" not in log:
        pasi_train.append(log["step"])
        loss_train.append(log["loss"])
    if "eval_loss" in log:
        pasi_eval.append(log["step"])
        loss_eval.append(log["eval_loss"])

plt.figure(figsize=(10, 5))
plt.plot(pasi_train, loss_train, label="Train Loss", color="teal", linewidth=2)
if pasi_eval:
    plt.plot(pasi_eval, loss_eval, label="Eval Loss", color="crimson", marker="o", linewidth=2)
plt.title("SmartBAC — Evoluția Loss (3 Epoci)", fontsize=14)
plt.xlabel("Pași")
plt.ylabel("Loss")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("loss_smartbac_v2.png", dpi=300)
plt.show()

if loss_train:
    print(f"Final train loss: {loss_train[-1]:.4f}")
if loss_eval:
    print(f"Final eval loss: {loss_eval[-1]:.4f}")

# ============================================================
# CELULA 9 — Test
# ============================================================

test_questions = [
    "Rezolvă ecuația: x² - 5x + 6 = 0",
    "Calculează derivata: f(x) = x³ + 2x",
    "Calculează C(10,3)",
]

model.eval()
for q in test_questions:
    prompt = f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n<|im_start|>user\n{q}<|im_end|>\n<|im_start|>assistant\n"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.3,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    print(f"\nQ: {q}")
    print(f"A: {response[:300]}")
    print("-" * 50)
