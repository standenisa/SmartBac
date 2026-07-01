"""
LoRA Configuration for Qwen2.5-Math Fine-tuning
Optimized for Apple Silicon M4 with MLX
"""
from dataclasses import dataclass, field
from typing import List


SYSTEM_PROMPT = (
    "Ești un asistent de matematică specializat pe exerciții BAC. "
    "Rezolvă exercițiul pas cu pas, explicând fiecare etapă."
)


@dataclass
class LoRAConfig:
    """LoRA adapter configuration"""
    # Model
    model_name: str = "Qwen/Qwen2.5-Math-1.5B"

    # LoRA parameters
    lora_rank: int = 16              # LoRA rank (16-64)
    lora_alpha: float = 32.0         # Scaling factor (typically 2x rank)
    lora_dropout: float = 0.05       # Dropout for LoRA layers
    target_modules: List[str] = field(default_factory=lambda: [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ])

    # Training
    batch_size: int = 4
    learning_rate: float = 1e-4
    num_epochs: int = 3
    warmup_ratio: float = 0.1
    weight_decay: float = 0.01
    max_seq_length: int = 512
    gradient_accumulation_steps: int = 4

    # Data — folosește split-urile pre-generate dacă există
    data_path: str = "data/processed/exercises_merged.json"
    splits_dir: str = "data/splits/finetune"  # train.jsonl, val.jsonl, test.jsonl
    train_split: float = 0.80
    val_split: float = 0.10  # restul (0.10) merge în test

    # Output
    output_dir: str = "ai/finetune/adapters"
    save_every: int = 100  # Save checkpoint every N steps

    seed: int = 42


@dataclass
class InstructionTemplate:
    """Template for instruction tuning format"""
    system_prompt: str = SYSTEM_PROMPT

    @staticmethod
    def format_prompt(question: str) -> str:
        return (
            f"<|im_start|>system\n"
            f"{SYSTEM_PROMPT}\n"
            f"<|im_end|>\n"
            f"<|im_start|>user\n"
            f"{question}\n"
            f"<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

    @staticmethod
    def format_training(question: str, answer: str, steps: list) -> str:
        steps_text = "\n".join(f"Pasul {i+1}: {s}" for i, s in enumerate(steps))
        response = f"{steps_text}\n\nRăspuns: {answer}"
        return (
            f"<|im_start|>system\n"
            f"{SYSTEM_PROMPT}\n"
            f"<|im_end|>\n"
            f"<|im_start|>user\n"
            f"{question}\n"
            f"<|im_end|>\n"
            f"<|im_start|>assistant\n"
            f"{response}\n"
            f"<|im_end|>"
        )
