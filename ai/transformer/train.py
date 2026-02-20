"""
Script de antrenament pentru MathTransformer (autoregresiv, decoder-only).

Pipeline-ul de antrenament:
    1. Încarcă exercițiile din data/raw/exercises_bac.json
    2. Tokenizează cu MathBPETokenizer din ai/tokenizer/bpe.py
    3. Creează MathDataset pentru next-token prediction cu teacher forcing
    4. Antrenează cu AdamW + warmup liniar + cosine decay
    5. Salvează cel mai bun model (după validation loss) în checkpoints/
    6. La final, generează un exemplu demonstrativ

Formatul secvenței de antrenament:
    <BOS> [întrebare] <SEP> [răspuns] <SEP> [pas 1] <SEP> [pas 2] ... <EOS>

    Modelul învață să prezică fiecare token din secvență bazându-se pe
    tokenii anteriori (next-token prediction). La inferență, primește
    întrebarea și generează răspunsul + pașii de rezolvare.

Hiperparametri:
    - Batch size: 8  (mic, avem doar ~242 exerciții)
    - Max seq len: 256 (suficient pentru exerciții BAC)
    - Epochs: 50
    - Optimizer: AdamW (lr=3e-4, weight_decay=0.01)
    - Scheduler: Warmup liniar 10% din steps + cosine decay
    - Gradient clipping: max_norm=1.0
    - Device: MPS (Apple Silicon) dacă disponibil, altfel CPU
"""

import json
import math
import os
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# ── Adăugăm project root la sys.path pentru importuri ──
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from ai.tokenizer.bpe import MathBPETokenizer
from ai.transformer.config import MathTransformerConfig
from ai.transformer.model import MathTransformer


# ═══════════════════════════════════════════════════════════════════════
# Dataset pentru next-token prediction
# ═══════════════════════════════════════════════════════════════════════

class MathDataset(Dataset):
    """
    Dataset PyTorch pentru antrenament autoregresiv (next-token prediction).

    Fiecare exercițiu devine O SINGURĂ secvență:
        <BOS> întrebare <SEP> răspuns <SEP> pas1 <SEP> pas2 ... <EOS>

    La antrenament, modelul primește secvența[:-1] ca input și prezice
    secvența[1:] ca target (teacher forcing).

    Args:
        data_path:  Calea către fișierul JSON cu exerciții.
        tokenizer:  Instanță MathBPETokenizer cu metodele encode/decode.
        max_len:    Lungimea maximă a secvenței (se trunchiază dacă depășește).
    """

    # ID-urile tokenilor speciali (din MathBPETokenizer.SPECIAL_TOKENS)
    BOS_ID = 2   # <BOS> — Beginning Of Sequence
    EOS_ID = 3   # <EOS> — End Of Sequence
    SEP_ID = 4   # <SEP> — Separator între părțile secvenței

    def __init__(self, data_path: str, tokenizer: MathBPETokenizer, max_len: int = 256):
        super().__init__()

        # Încărcăm datele din JSON
        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.tokenizer = tokenizer
        self.max_len = max_len

        # Pre-tokenizăm toate exercițiile (cache pentru viteză)
        self.sequences = []
        for item in self.data:
            seq = self._build_sequence(item)
            self.sequences.append(seq)

    def _build_sequence(self, item: dict) -> list[int]:
        """
        Construiește secvența de tokeni pentru un exercițiu.

        Format:
            <BOS> encode(întrebare) <SEP> encode(răspuns) <SEP> encode(pas1) ... <EOS>

        Args:
            item: Dicționar cu câmpurile 'question', 'answer', 'steps' (opțional).

        Returns:
            Lista de token IDs, trunchiată la max_len.
        """
        question = item.get("question", "")
        answer = str(item.get("answer", ""))
        steps = item.get("steps", [])

        # Tokenizăm fiecare parte separat
        question_ids = self.tokenizer.encode(question)
        answer_ids = self.tokenizer.encode(answer)

        # Construim secvența: <BOS> question <SEP> answer
        seq = [self.BOS_ID] + question_ids + [self.SEP_ID] + answer_ids

        # Adăugăm pașii de rezolvare (dacă există): <SEP> pas1 <SEP> pas2 ...
        for step in steps:
            step_ids = self.tokenizer.encode(str(step))
            seq += [self.SEP_ID] + step_ids

        # Adăugăm <EOS> la final
        seq.append(self.EOS_ID)

        # Trunchiăm la max_len dacă secvența e prea lungă
        seq = seq[:self.max_len]

        # Asigurăm că ultimul token este <EOS> (dacă am trunchiat)
        if seq[-1] != self.EOS_ID:
            seq[-1] = self.EOS_ID

        return seq

    def __len__(self) -> int:
        return len(self.sequences)

    def __getitem__(self, idx: int) -> torch.Tensor:
        """Returnează secvența de tokeni ca tensor PyTorch."""
        return torch.tensor(self.sequences[idx], dtype=torch.long)


# ═══════════════════════════════════════════════════════════════════════
# Collate function: padding dinamic la lungimea maximă din batch
# ═══════════════════════════════════════════════════════════════════════

def collate_fn(batch: list[torch.Tensor], pad_idx: int = 0) -> torch.Tensor:
    """
    Padding dinamic: toate secvențele din batch devin egale ca lungime.

    Secvențele mai scurte sunt completate cu <PAD> (index 0) la dreapta.
    Acest lucru e necesar pentru a crea un tensor rectangular (batch, max_len).

    Args:
        batch:   Lista de tensori cu lungimi diferite.
        pad_idx: Indexul tokenului de padding.

    Returns:
        Tensor de formă (batch_size, max_len_in_batch).
    """
    # nn.utils.rnn.pad_sequence adaugă padding automat
    return nn.utils.rnn.pad_sequence(batch, batch_first=True, padding_value=pad_idx)


# ═══════════════════════════════════════════════════════════════════════
# Learning Rate Scheduler: Warmup liniar + Cosine Decay
# ═══════════════════════════════════════════════════════════════════════

class WarmupCosineScheduler:
    """
    Scheduler de learning rate cu warmup liniar urmat de cosine decay.

    Faza 1 (warmup): LR crește liniar de la 0 la lr_max
        - Durează warmup_steps pași
        - Previne actualizări prea mari la început când greutățile sunt random

    Faza 2 (cosine decay): LR scade gradual urmând o curbă cosinus
        - De la lr_max la ~0
        - Mai "blândă" decât decăderea exponențială
        - Permite modelului să facă ajustări fine la final

    Grafic:
        LR │     ╱‾‾‾‾‾‾‾‾‾╲
           │    ╱              ╲
           │   ╱                 ╲
           │  ╱                    ╲
           │ ╱                       ╲
           │╱                          ╲___
           └─────────────────────────────── step
           0   warmup     total_steps

    Args:
        optimizer:     Optimizer-ul PyTorch.
        warmup_steps:  Numărul de pași de warmup.
        total_steps:   Numărul total de pași de antrenament.
        lr_max:        Learning rate-ul maxim (atins la sfârșitul warmup-ului).
    """

    def __init__(self, optimizer, warmup_steps: int, total_steps: int, lr_max: float = 3e-4):
        self.optimizer = optimizer
        self.warmup_steps = warmup_steps
        self.total_steps = total_steps
        self.lr_max = lr_max
        self._step = 0

    def step(self):
        """Actualizează learning rate-ul la fiecare pas de antrenament."""
        self._step += 1
        lr = self._compute_lr()
        for param_group in self.optimizer.param_groups:
            param_group["lr"] = lr

    def _compute_lr(self) -> float:
        """Calculează learning rate-ul curent."""
        if self._step <= self.warmup_steps:
            # Faza 1: Warmup liniar — LR crește de la 0 la lr_max
            return self.lr_max * (self._step / max(self.warmup_steps, 1))
        else:
            # Faza 2: Cosine decay — LR scade de la lr_max spre 0
            # Progresul în faza de decay: 0.0 (început) → 1.0 (final)
            progress = (self._step - self.warmup_steps) / max(
                self.total_steps - self.warmup_steps, 1
            )
            # cos(0) = 1, cos(π) = -1 → (1 + cos(π·progress)) / 2 scade de la 1 la 0
            return self.lr_max * 0.5 * (1.0 + math.cos(math.pi * progress))

    def get_last_lr(self) -> float:
        """Returnează ultimul learning rate calculat."""
        return self._compute_lr()


# ═══════════════════════════════════════════════════════════════════════
# Bucla de antrenament pentru o epocă
# ═══════════════════════════════════════════════════════════════════════

def train_epoch(
    model: MathTransformer,
    dataloader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
    scheduler: WarmupCosineScheduler | None = None,
    grad_clip: float = 1.0,
) -> float:
    """
    Antrenează modelul pentru o epocă completă.

    La fiecare batch:
        1. Input = secvența[:-1] (tot minus ultimul token)
        2. Labels = secvența[1:] (tot minus primul token)
        3. Forward pass → logits
        4. Calculează loss (CrossEntropy, ignorând <PAD>)
        5. Backward pass + gradient clipping + optimizer step

    Args:
        model:      Modelul MathTransformer.
        dataloader: DataLoader-ul de antrenament.
        optimizer:  Optimizer-ul (AdamW).
        criterion:  Funcția de loss (CrossEntropyLoss).
        device:     Device-ul (cpu/mps/cuda).
        scheduler:  Scheduler-ul de learning rate (opțional).
        grad_clip:  Norma maximă a gradientului (pentru clipping).

    Returns:
        Loss-ul mediu pe întreaga epocă.
    """
    model.train()
    total_loss = 0.0
    n_batches = 0

    for batch in dataloader:
        # Mutăm batch-ul pe device (MPS/CPU)
        batch = batch.to(device)

        # ── Teacher forcing ──
        # Input: toate tokenurile MINUS ultimul (modelul prezice următorul)
        input_ids = batch[:, :-1]
        # Labels: toate tokenurile MINUS primul (ce trebuie prezis)
        labels = batch[:, 1:]

        # Resetăm gradienții din iterația anterioară
        optimizer.zero_grad()

        # Forward pass: model(input) → logits (batch, seq_len-1, vocab_size)
        logits = model(input_ids)

        # Aplatizăm pentru CrossEntropyLoss:
        #   logits: (batch * seq_len, vocab_size)
        #   labels: (batch * seq_len,)
        loss = criterion(
            logits.reshape(-1, logits.size(-1)),
            labels.reshape(-1),
        )

        # Backward pass: calculează gradienții
        loss.backward()

        # Gradient clipping: previne explodarea gradienților
        # Normalizează gradienții dacă norma lor depășește grad_clip
        nn.utils.clip_grad_norm_(model.parameters(), grad_clip)

        # Actualizează greutățile
        optimizer.step()

        # Actualizează learning rate-ul
        if scheduler is not None:
            scheduler.step()

        total_loss += loss.item()
        n_batches += 1

    return total_loss / max(n_batches, 1)


# ═══════════════════════════════════════════════════════════════════════
# Bucla de evaluare
# ═══════════════════════════════════════════════════════════════════════

@torch.no_grad()
def evaluate_epoch(
    model: MathTransformer,
    dataloader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> float:
    """
    Evaluează modelul pe un set de date (fără backward pass).

    Args:
        model:      Modelul MathTransformer.
        dataloader: DataLoader-ul de evaluare.
        criterion:  Funcția de loss.
        device:     Device-ul.

    Returns:
        Loss-ul mediu pe setul de evaluare.
    """
    model.eval()
    total_loss = 0.0
    n_batches = 0

    for batch in dataloader:
        batch = batch.to(device)
        input_ids = batch[:, :-1]
        labels = batch[:, 1:]

        logits = model(input_ids)
        loss = criterion(
            logits.reshape(-1, logits.size(-1)),
            labels.reshape(-1),
        )

        total_loss += loss.item()
        n_batches += 1

    return total_loss / max(n_batches, 1)


# ═══════════════════════════════════════════════════════════════════════
# Funcția principală de antrenament
# ═══════════════════════════════════════════════════════════════════════

def main():
    """
    Rutina principală de antrenament.

    Pașii:
        1. Detectează device-ul (MPS / CUDA / CPU)
        2. Încarcă tokenizer-ul BPE antrenat
        3. Încarcă datele din JSON și creează dataset-ul
        4. Configurează modelul, optimizer-ul și scheduler-ul
        5. Antrenează 50 de epoci cu salvare automată a celui mai bun model
        6. Generează un exemplu demonstrativ la final
    """
    print("=" * 65)
    print("  MathTransformer — Antrenament Autoregresiv")
    print("=" * 65)

    # ── Căi fișiere ──
    project_root = _PROJECT_ROOT
    data_path = project_root / "data" / "raw" / "exercises_bac.json"
    tokenizer_path = project_root / "ai" / "tokenizer" / "math_bpe.json"
    checkpoint_dir = project_root / "ai" / "transformer" / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    best_model_path = checkpoint_dir / "best_model.pt"
    history_path = checkpoint_dir / "training_history.json"

    # ── Device ──
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print(f"[DEVICE] MPS (Apple Silicon GPU)")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"[DEVICE] CUDA ({torch.cuda.get_device_name(0)})")
    else:
        device = torch.device("cpu")
        print(f"[DEVICE] CPU")

    # ── Încarcă tokenizer-ul ──
    if not tokenizer_path.exists():
        print(f"[EROARE] Tokenizer-ul nu a fost găsit la: {tokenizer_path}")
        print("  Rulează mai întâi: python -m ai.tokenizer.train_tokenizer")
        sys.exit(1)

    tokenizer = MathBPETokenizer()
    tokenizer.load(str(tokenizer_path))
    vocab_size = len(tokenizer)
    print(f"[TOKENIZER] Încărcat: {vocab_size} tokeni din {tokenizer_path}")

    # ── Verifică datele ──
    if not data_path.exists():
        print(f"[EROARE] Datele nu au fost găsite la: {data_path}")
        print("  Rulează mai întâi: python scripts/collect_data.py")
        sys.exit(1)

    # ── Hiperparametri ──
    BATCH_SIZE = 8        # Mic: avem doar ~242 exerciții
    MAX_SEQ_LEN = 256     # Suficient pentru exerciții BAC
    NUM_EPOCHS = 50       # Epoci de antrenament
    LR_MAX = 3e-4         # Learning rate maxim (AdamW)
    GRAD_CLIP = 1.0       # Gradient clipping max norm

    # ── Configurația modelului ──
    config = MathTransformerConfig(
        vocab_size=vocab_size,   # Din tokenizer (ex: 1347)
        d_model=256,
        n_heads=8,
        n_layers=6,
        d_ff=1024,
        max_seq_len=MAX_SEQ_LEN,
        dropout=0.1,
    )

    # ── Dataset ──
    print(f"\n[DATE] Încarcă exercițiile din {data_path}...")
    full_dataset = MathDataset(str(data_path), tokenizer, max_len=MAX_SEQ_LEN)
    n_total = len(full_dataset)

    # Split: 80% antrenament, 10% validare, 10% test
    n_train = int(0.8 * n_total)
    n_val = int(0.1 * n_total)
    n_test = n_total - n_train - n_val

    train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
        full_dataset,
        [n_train, n_val, n_test],
        generator=torch.Generator().manual_seed(42),
    )

    print(f"[DATE] Total: {n_total} | Train: {n_train} | Val: {n_val} | Test: {n_test}")

    # Lungimea medie a secvențelor (pentru informare)
    avg_len = sum(len(s) for s in full_dataset.sequences) / len(full_dataset.sequences)
    print(f"[DATE] Lungime medie secvență: {avg_len:.1f} tokeni")

    # ── DataLoaders ──
    pad_idx = config.pad_idx
    _collate = lambda batch: collate_fn(batch, pad_idx=pad_idx)

    train_loader = DataLoader(
        train_dataset, batch_size=BATCH_SIZE, shuffle=True,
        collate_fn=_collate, num_workers=0, drop_last=False,
    )
    val_loader = DataLoader(
        val_dataset, batch_size=BATCH_SIZE * 2, shuffle=False,
        collate_fn=_collate, num_workers=0,
    )
    test_loader = DataLoader(
        test_dataset, batch_size=BATCH_SIZE * 2, shuffle=False,
        collate_fn=_collate, num_workers=0,
    )

    # ── Model ──
    print(f"\n[MODEL] Creez MathTransformer...")
    model = MathTransformer(config).to(device)

    # ── Optimizer: AdamW ──
    # AdamW = Adam cu weight decay decuplat (regularizare L2 corectă)
    # betas=(0.9, 0.95) — standard pentru LLM-uri (LLaMA folosește aceleași valori)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LR_MAX,
        betas=(0.9, 0.95),
        weight_decay=0.01,
    )

    # ── Scheduler: Warmup 10% + Cosine Decay ──
    total_steps = NUM_EPOCHS * len(train_loader)
    warmup_steps = int(0.10 * total_steps)  # 10% warmup
    scheduler = WarmupCosineScheduler(optimizer, warmup_steps, total_steps, lr_max=LR_MAX)
    print(f"[SCHEDULER] Total steps: {total_steps} | Warmup: {warmup_steps}")

    # ── Loss: CrossEntropyLoss cu ignorare <PAD> ──
    criterion = nn.CrossEntropyLoss(ignore_index=pad_idx)

    # ═══════════════════════════════════════════════════════════════════
    # Bucla de antrenament
    # ═══════════════════════════════════════════════════════════════════

    best_val_loss = float("inf")
    history: list[dict] = []

    print(f"\n{'=' * 65}")
    print(f"  Încep antrenamentul: {NUM_EPOCHS} epoci")
    print(f"{'=' * 65}\n")

    for epoch in range(1, NUM_EPOCHS + 1):
        t0 = time.time()

        # Antrenament pe o epocă
        train_loss = train_epoch(
            model, train_loader, optimizer, criterion, device, scheduler, GRAD_CLIP
        )

        # Evaluare pe setul de validare
        val_loss = evaluate_epoch(model, val_loader, criterion, device)

        elapsed = time.time() - t0
        lr = scheduler.get_last_lr()

        # Loghează rezultatele
        print(
            f"  Epoca {epoch:3d}/{NUM_EPOCHS} │ "
            f"train_loss={train_loss:.4f} │ val_loss={val_loss:.4f} │ "
            f"lr={lr:.2e} │ {elapsed:.1f}s"
        )

        history.append({
            "epoch": epoch,
            "train_loss": round(train_loss, 6),
            "val_loss": round(val_loss, 6),
            "lr": round(lr, 8),
            "time_s": round(elapsed, 2),
        })

        # Salvează cel mai bun model (cel cu cel mai mic val_loss)
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "config": config,
                    "val_loss": val_loss,
                    "vocab_size": vocab_size,
                },
                best_model_path,
            )
            print(f"    ✓ Salvat best model (val_loss={val_loss:.4f})")

    # ═══════════════════════════════════════════════════════════════════
    # Evaluare finală pe setul de test
    # ═══════════════════════════════════════════════════════════════════

    print(f"\n{'=' * 65}")
    test_loss = evaluate_epoch(model, test_loader, criterion, device)
    print(f"  Test loss: {test_loss:.4f}")

    # ── Salvează istoricul antrenamentului ──
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print(f"  Istoric salvat în {history_path}")

    # ═══════════════════════════════════════════════════════════════════
    # Generare demonstrativă
    # ═══════════════════════════════════════════════════════════════════

    print(f"\n{'=' * 65}")
    print("  Generare demonstrativă")
    print(f"{'=' * 65}")

    demo_prompt = "Rezolvă ecuația: 2x + 3 = 7"
    print(f"\n  Prompt: {demo_prompt}")

    # Tokenizăm prompt-ul: <BOS> + encode(prompt) + <SEP>
    prompt_ids = [config.bos_idx] + tokenizer.encode(demo_prompt) + [config.sep_idx]
    input_tensor = torch.tensor([prompt_ids], dtype=torch.long).to(device)

    # Generăm cu temperature=0.7 și top_k=50
    output = model.generate(
        input_tensor,
        max_new_tokens=100,
        temperature=0.7,
        top_k=50,
    )

    # Decodăm rezultatul (sărind tokenii speciali)
    output_ids = output[0].tolist()
    # Găsim primul <SEP> (marchează începutul răspunsului)
    decoded = tokenizer.decode(output_ids)
    print(f"  Output complet: {decoded}")

    # Extragem doar partea generată (după prompt)
    generated_ids = output_ids[len(prompt_ids):]
    generated_text = tokenizer.decode(generated_ids)
    print(f"  Generat: {generated_text}")

    print(f"\n{'=' * 65}")
    print("  Antrenament complet!")
    print(f"  Best model: {best_model_path}")
    print(f"  Best val_loss: {best_val_loss:.4f}")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    main()
