"""
Fine-tune Qwen2.5-Math with LoRA using MLX
Optimized for Apple Silicon (M4)
"""
import json
import sys
import time
import math
import argparse
import random
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ai.finetune.lora_config import LoRAConfig, InstructionTemplate

# ---------------------------------------------------------------------------
# MLX imports -- wrapped so the script can still be inspected / tested on
# machines where MLX is not installed.
# ---------------------------------------------------------------------------
try:
    import mlx.core as mx
    import mlx.nn as nn
    import mlx.optimizers as optim
    from mlx.utils import tree_flatten, tree_map
    MLX_AVAILABLE = True
except ImportError:
    MLX_AVAILABLE = False

try:
    from mlx_lm import load as mlx_load
    from mlx_lm.tuner.lora import LoRALinear
    MLX_LM_AVAILABLE = True
except ImportError:
    MLX_LM_AVAILABLE = False


# ============================================================================
# Dataset preparation
# ============================================================================

def _load_jsonl(path: Path) -> list[str]:
    samples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                samples.append(json.loads(line)["text"])
    return samples


def prepare_dataset(config: LoRAConfig) -> dict:
    """Load exercises, convert to instruction format, split and save.

    Dacă există split-uri pre-generate (data/splits/finetune/*.jsonl),
    le folosește direct. Altfel, încarcă JSON-ul complet și face split intern.

    Returns a dict with keys ``train``, ``val``, ``test`` each holding a list
    of formatted text strings ready for tokenisation.
    """
    project_root = Path(__file__).resolve().parent.parent.parent

    # ── Verificăm dacă există split-uri pre-generate ──
    splits_dir = Path(config.splits_dir)
    if not splits_dir.is_absolute():
        splits_dir = project_root / splits_dir

    presplit_train = splits_dir / "train.jsonl"
    if presplit_train.exists():
        print(f"[data] Folosesc split-uri pre-generate din {splits_dir}")
        splits = {}
        for split_name in ["train", "val", "test"]:
            jsonl_path = splits_dir / f"{split_name}.jsonl"
            samples = _load_jsonl(jsonl_path) if jsonl_path.exists() else []
            splits[split_name] = samples
            print(f"[data] {split_name}: {len(samples)} samples (pre-split)")
        total = sum(len(v) for v in splits.values())
        print(f"[data] Total: {total} samples")
        return splits

    # ── Fallback: încarcă JSON-ul complet și face split intern ──
    data_path = Path(config.data_path)
    if not data_path.is_absolute():
        data_path = project_root / data_path

    print(f"[data] Loading exercises from {data_path} ...")
    if not data_path.exists():
        print(f"[data] WARNING: {data_path} not found. Creating sample dataset for testing.")
        exercises = _create_sample_dataset()
    else:
        with open(data_path, "r", encoding="utf-8") as f:
            exercises = json.load(f)

    # Convert every exercise to the ChatML instruction format
    formatted: list[str] = []
    for ex in exercises:
        question = ex.get("question", ex.get("text", ""))
        answer = ex.get("answer", ex.get("solution", ""))
        steps = ex.get("steps", ex.get("solution_steps", []))
        if isinstance(steps, str):
            steps = [s.strip() for s in steps.split("\n") if s.strip()]
        if question and answer:
            formatted.append(
                InstructionTemplate.format_training(question, answer, steps)
            )

    random.seed(config.seed)
    random.shuffle(formatted)

    n = len(formatted)
    n_train = int(n * config.train_split)
    n_val = int(n * config.val_split)

    splits = {
        "train": formatted[:n_train],
        "val": formatted[n_train:n_train + n_val],
        "test": formatted[n_train + n_val:],
    }

    # Persist as JSONL for reproducibility / use by mlx-lm tooling
    out_dir = Path(config.output_dir)
    if not out_dir.is_absolute():
        out_dir = project_root / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    for split_name, samples in splits.items():
        jsonl_path = out_dir / f"{split_name}.jsonl"
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for sample in samples:
                json.dump({"text": sample}, f, ensure_ascii=False)
                f.write("\n")
        print(f"[data] {split_name}: {len(samples)} samples -> {jsonl_path}")

    print(f"[data] Total formatted samples: {n}")
    return splits


def _create_sample_dataset() -> list[dict]:
    """Return a tiny placeholder dataset so the pipeline can be tested end-to-end."""
    return [
        {
            "question": "Calculați limita: lim(x->inf) (x^2 + 3x) / (2x^2 - 1)",
            "answer": "1/2",
            "steps": [
                "Împărțim numărătorul și numitorul la x^2",
                "Obținem lim (1 + 3/x) / (2 - 1/x^2)",
                "Când x -> inf, termenii 3/x și 1/x^2 tind la 0",
                "Limita este 1/2",
            ],
        },
        {
            "question": "Determinați derivata funcției f(x) = x^3 - 6x^2 + 9x + 1",
            "answer": "f'(x) = 3x^2 - 12x + 9",
            "steps": [
                "Aplicăm regula de derivare pentru puteri: (x^n)' = n*x^(n-1)",
                "(x^3)' = 3x^2",
                "(-6x^2)' = -12x",
                "(9x)' = 9",
                "(1)' = 0",
                "f'(x) = 3x^2 - 12x + 9",
            ],
        },
        {
            "question": "Rezolvați ecuația: x^2 - 5x + 6 = 0",
            "answer": "x1 = 2, x2 = 3",
            "steps": [
                "Identificăm coeficienții: a=1, b=-5, c=6",
                "Calculăm discriminantul: Δ = b^2 - 4ac = 25 - 24 = 1",
                "x1 = (5-1)/2 = 2",
                "x2 = (5+1)/2 = 3",
            ],
        },
        {
            "question": "Calculați integrala: ∫(2x + 3)dx",
            "answer": "x^2 + 3x + C",
            "steps": [
                "Aplicăm liniaritatea integralei",
                "∫2x dx = x^2",
                "∫3 dx = 3x",
                "Adăugăm constanta de integrare C",
                "Rezultat: x^2 + 3x + C",
            ],
        },
    ]


# ============================================================================
# Model setup
# ============================================================================

def setup_model(config: LoRAConfig):
    """Load the base model, apply LoRA adapters, and return (model, tokenizer).

    Uses ``mlx_lm.load`` to fetch / cache the base weights and then patches
    the requested ``target_modules`` with LoRA linear layers.
    """
    if not MLX_AVAILABLE or not MLX_LM_AVAILABLE:
        _print_install_instructions()
        sys.exit(1)

    print(f"[model] Loading {config.model_name} ...")
    model, tokenizer = mlx_load(config.model_name)

    # ----- apply LoRA adapters -----
    # Freeze the base model first; the LoRA layers created below add fresh
    # (trainable) lora_a / lora_b parameters on top of the frozen weights.
    model.freeze()

    lora_layers = 0

    def _apply_lora(module):
        nonlocal lora_layers
        for name, child in module.named_modules():
            # Replace matching linear layers with LoRA variants
            short = name.split(".")[-1]
            if short in config.target_modules and isinstance(child, nn.Linear):
                lora_layer = LoRALinear.from_linear(
                    child,
                    r=config.lora_rank,
                    alpha=config.lora_alpha,
                    dropout=config.lora_dropout,
                )
                # Set on parent -- walk the attribute chain
                parts = name.split(".")
                parent = module
                for p in parts[:-1]:
                    parent = parent[int(p)] if p.isdigit() else getattr(parent, p)
                setattr(parent, parts[-1], lora_layer)
                lora_layers += 1

    _apply_lora(model)

    total_params = sum(v.size for _, v in tree_flatten(model.parameters()))
    trainable_params = sum(v.size for _, v in tree_flatten(model.trainable_parameters()))

    print(f"[model] LoRA adapters applied to {lora_layers} layers")
    print(f"[model] Total parameters:     {total_params:,}")
    print(f"[model] Trainable parameters:  {trainable_params:,}")
    if total_params > 0:
        print(f"[model] Trainable ratio:       {trainable_params / total_params:.4%}")

    return model, tokenizer


# ============================================================================
# Learning-rate schedule helpers
# ============================================================================

def _lr_schedule(step: int, total_steps: int, config: LoRAConfig) -> float:
    """Linear warmup followed by cosine decay."""
    warmup_steps = int(total_steps * config.warmup_ratio)
    if step < warmup_steps:
        return config.learning_rate * (step / max(1, warmup_steps))
    progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
    return config.learning_rate * 0.5 * (1.0 + math.cos(math.pi * progress))


# ============================================================================
# Training
# ============================================================================

def train(config: LoRAConfig):
    """Full training loop with logging, validation, and checkpoint saving."""
    if not MLX_AVAILABLE or not MLX_LM_AVAILABLE:
        _print_install_instructions()
        sys.exit(1)

    mx.random.seed(config.seed)

    # ---- paths -----------------------------------------------------------
    out_dir = Path(config.output_dir)
    if not out_dir.is_absolute():
        out_dir = Path(__file__).resolve().parent.parent.parent / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- load data -------------------------------------------------------
    # Prefer pre-generated splits, fallback to output_dir
    project_root = Path(__file__).resolve().parent.parent.parent
    splits_dir = Path(config.splits_dir)
    if not splits_dir.is_absolute():
        splits_dir = project_root / splits_dir

    if (splits_dir / "train.jsonl").exists():
        train_jsonl = splits_dir / "train.jsonl"
        val_jsonl = splits_dir / "val.jsonl"
        print(f"[train] Using pre-split data from {splits_dir}")
    else:
        train_jsonl = out_dir / "train.jsonl"
        val_jsonl = out_dir / "val.jsonl"

    if not train_jsonl.exists():
        print("[train] Training JSONL not found. Running prepare_dataset first ...")
        prepare_dataset(config)

    train_texts = _load_jsonl(train_jsonl)
    val_texts = _load_jsonl(val_jsonl) if val_jsonl.exists() else []

    print(f"[train] Training samples:   {len(train_texts)}")
    print(f"[train] Validation samples: {len(val_texts)}")

    if not train_texts:
        print("[train] ERROR: No training data. Aborting.")
        return

    # ---- model -----------------------------------------------------------
    model, tokenizer = setup_model(config)

    # ---- tokenise --------------------------------------------------------
    def tokenize(text: str):
        return tokenizer.encode(text, max_length=config.max_seq_length, truncation=True)

    train_tokens = [tokenize(t) for t in train_texts]
    val_tokens = [tokenize(t) for t in val_texts] if val_texts else []

    # ---- optimizer -------------------------------------------------------
    steps_per_epoch = max(1, len(train_tokens) // (config.batch_size * config.gradient_accumulation_steps))
    total_steps = steps_per_epoch * config.num_epochs

    optimizer = optim.AdamW(
        learning_rate=config.learning_rate,
        weight_decay=config.weight_decay,
    )

    # ---- loss function ---------------------------------------------------
    def loss_fn(model, tokens_batch):
        """Compute cross-entropy loss over a batch of token sequences."""
        total_loss = mx.array(0.0)
        count = 0
        for tokens in tokens_batch:
            x = mx.array(tokens[:-1])[None, :]   # (1, seq_len-1)
            y = mx.array(tokens[1:])              # (seq_len-1,)
            logits = model(x)                     # (1, seq_len-1, vocab)
            logits = logits.squeeze(0)            # (seq_len-1, vocab)
            ce = nn.losses.cross_entropy(logits, y, reduction="mean")
            total_loss = total_loss + ce
            count += 1
        return total_loss / max(count, 1)

    loss_and_grad = nn.value_and_grad(model, loss_fn)

    # ---- training loop ---------------------------------------------------
    print(f"\n{'='*60}")
    print(f" Starting LoRA fine-tuning")
    print(f" Steps/epoch: {steps_per_epoch}  |  Total steps: {total_steps}")
    print(f"{'='*60}\n")

    best_val_loss = float("inf")
    global_step = 0
    start_time = time.time()

    for epoch in range(1, config.num_epochs + 1):
        # Shuffle training data each epoch
        indices = list(range(len(train_tokens)))
        random.shuffle(indices)

        epoch_loss = 0.0
        epoch_steps = 0
        accum_loss = mx.array(0.0)
        accum_grads = None
        accum_count = 0

        for i in range(0, len(indices), config.batch_size):
            batch_indices = indices[i : i + config.batch_size]
            batch = [train_tokens[j] for j in batch_indices]

            if not batch:
                continue

            # Update learning rate
            lr = _lr_schedule(global_step, total_steps, config)
            optimizer.learning_rate = lr

            loss, grads = loss_and_grad(model, batch)
            accum_loss = accum_loss + loss
            accum_grads = grads if accum_grads is None else tree_map(
                lambda a, b: a + b, accum_grads, grads
            )
            accum_count += 1

            # Update on a full accumulation window, or flush the leftover
            # micro-batches at the end of the epoch.
            is_last_batch = i + config.batch_size >= len(indices)
            if accum_count >= config.gradient_accumulation_steps or is_last_batch:
                # Average accumulated gradients
                scale = 1.0 / accum_count
                grads = tree_map(lambda g: g * scale, accum_grads)
                optimizer.update(model, grads)
                mx.eval(model.parameters(), optimizer.state)

                avg_loss = (accum_loss / accum_count).item()
                epoch_loss += avg_loss
                epoch_steps += 1
                global_step += 1

                accum_loss = mx.array(0.0)
                accum_grads = None
                accum_count = 0

                # Log every 10 steps
                if global_step % 10 == 0:
                    elapsed = time.time() - start_time
                    print(
                        f"  [epoch {epoch}/{config.num_epochs}]  "
                        f"step {global_step}/{total_steps}  "
                        f"loss={avg_loss:.4f}  lr={lr:.2e}  "
                        f"time={elapsed:.1f}s"
                    )

                # Validate + checkpoint every save_every steps
                if global_step % config.save_every == 0:
                    val_loss = _evaluate(model, val_tokens, config) if val_tokens else None
                    val_str = f"{val_loss:.4f}" if val_loss is not None else "N/A"
                    print(f"  >> Validation loss: {val_str}")

                    # Save checkpoint
                    ckpt_path = out_dir / f"checkpoint-{global_step}"
                    ckpt_path.mkdir(parents=True, exist_ok=True)
                    _save_adapter(model, ckpt_path, config)
                    print(f"  >> Checkpoint saved to {ckpt_path}")

                    if val_loss is not None and val_loss < best_val_loss:
                        best_val_loss = val_loss
                        best_path = out_dir / "best_adapter"
                        best_path.mkdir(parents=True, exist_ok=True)
                        _save_adapter(model, best_path, config)
                        print(f"  >> Best model updated (val_loss={best_val_loss:.4f})")

        avg_epoch_loss = epoch_loss / max(epoch_steps, 1)
        print(f"\n  Epoch {epoch} complete  |  avg loss = {avg_epoch_loss:.4f}\n")

    # ---- final save ------------------------------------------------------
    final_path = out_dir / "final_adapter"
    final_path.mkdir(parents=True, exist_ok=True)
    _save_adapter(model, final_path, config)

    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f" Training complete!")
    print(f" Total time:      {elapsed:.1f}s")
    print(f" Best val loss:   {best_val_loss:.4f}")
    print(f" Final adapter:   {final_path}")
    print(f"{'='*60}\n")


# ============================================================================
# Evaluation helper
# ============================================================================

def _evaluate(model, val_tokens: list, config: LoRAConfig) -> float:
    """Compute average cross-entropy on the validation set."""
    total_loss = 0.0
    count = 0
    for tokens in val_tokens:
        x = mx.array(tokens[:-1])[None, :]
        y = mx.array(tokens[1:])
        logits = model(x).squeeze(0)
        ce = nn.losses.cross_entropy(logits, y, reduction="mean")
        total_loss += ce.item()
        count += 1
    return total_loss / max(count, 1)


# ============================================================================
# Adapter save / load
# ============================================================================

def _save_adapter(model, path: Path, config: LoRAConfig):
    """Save only the LoRA adapter weights to *path*."""
    adapter_weights = dict(tree_flatten(model.trainable_parameters()))
    mx.save_safetensors(str(path / "adapters.safetensors"), adapter_weights)

    # Also persist the config so we know which base model to load later
    meta = {
        "model_name": config.model_name,
        "lora_rank": config.lora_rank,
        "lora_alpha": config.lora_alpha,
    }
    with open(path / "adapter_config.json", "w") as f:
        json.dump(meta, f, indent=2)


# ============================================================================
# Utility
# ============================================================================

def _print_install_instructions():
    print(
        "\n"
        "=" * 60 + "\n"
        " MLX is not installed or not available on this machine.\n"
        " This training script requires Apple Silicon and the\n"
        " following packages:\n"
        "\n"
        "   pip install mlx mlx-lm\n"
        "\n"
        " Make sure you are running on macOS with an M-series chip.\n"
        "=" * 60 + "\n"
    )


# ============================================================================
# CLI entry-point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Fine-tune Qwen2.5-Math with LoRA on MLX"
    )
    parser.add_argument("--lora-rank", type=int, default=None, help="LoRA rank (default: 16)")
    parser.add_argument("--lora-alpha", type=float, default=None, help="LoRA alpha (default: 32)")
    parser.add_argument("--epochs", type=int, default=None, help="Number of training epochs")
    parser.add_argument("--lr", type=float, default=None, help="Learning rate")
    parser.add_argument("--batch-size", type=int, default=None, help="Batch size")
    parser.add_argument("--max-seq-length", type=int, default=None, help="Maximum sequence length")
    parser.add_argument("--data-path", type=str, default=None, help="Path to exercise JSON")
    parser.add_argument("--output-dir", type=str, default=None, help="Directory for adapters / checkpoints")
    parser.add_argument("--model", type=str, default=None, help="Base model name or path")
    parser.add_argument("--prepare-only", action="store_true", help="Only prepare dataset, skip training")

    args = parser.parse_args()
    config = LoRAConfig()

    # Apply CLI overrides
    if args.lora_rank is not None:
        config.lora_rank = args.lora_rank
    if args.lora_alpha is not None:
        config.lora_alpha = args.lora_alpha
    if args.epochs is not None:
        config.num_epochs = args.epochs
    if args.lr is not None:
        config.learning_rate = args.lr
    if args.batch_size is not None:
        config.batch_size = args.batch_size
    if args.max_seq_length is not None:
        config.max_seq_length = args.max_seq_length
    if args.data_path is not None:
        config.data_path = args.data_path
    if args.output_dir is not None:
        config.output_dir = args.output_dir
    if args.model is not None:
        config.model_name = args.model

    print("=" * 60)
    print(" LoRA Fine-tuning Configuration")
    print("=" * 60)
    print(f"  Model:          {config.model_name}")
    print(f"  LoRA rank:      {config.lora_rank}")
    print(f"  LoRA alpha:     {config.lora_alpha}")
    print(f"  Batch size:     {config.batch_size}")
    print(f"  Learning rate:  {config.learning_rate}")
    print(f"  Epochs:         {config.num_epochs}")
    print(f"  Max seq length: {config.max_seq_length}")
    print(f"  Data path:      {config.data_path}")
    print(f"  Output dir:     {config.output_dir}")
    print("=" * 60 + "\n")

    # Step 1 -- prepare data
    prepare_dataset(config)

    if args.prepare_only:
        print("[main] --prepare-only flag set. Exiting after dataset preparation.")
        return

    # Step 2 -- train
    if not MLX_AVAILABLE or not MLX_LM_AVAILABLE:
        _print_install_instructions()
        sys.exit(1)

    train(config)

    # Step 3 -- final stats
    print("\n[main] Fine-tuning pipeline finished successfully.")
    print(f"[main] Adapter weights saved to: {config.output_dir}")
    print("[main] Use ai/finetune/inference.py to run inference with the fine-tuned model.")


if __name__ == "__main__":
    main()
