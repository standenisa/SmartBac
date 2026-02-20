"""
Configurația modelului Transformer autoregresiv.

Conține toți hiperparametrii într-un singur dataclass, ușor de serializat
și de reconstruit la încărcarea unui checkpoint.

Parametri impliciți:
    vocab_size = 8192   (va fi suprascris din tokenizer la runtime)
    d_model    = 256    (dimensiunea embedding-ului și a reprezentărilor interne)
    n_heads    = 8      (capete de atenție; d_k = d_model / n_heads = 32)
    n_layers   = 6      (blocuri Transformer stivuite)
    d_ff       = 1024   (dimensiunea stratului feed-forward, 4× d_model)
    max_seq_len = 512   (lungimea maximă a secvenței de intrare)
    dropout    = 0.1    (probabilitate dropout peste tot în model)
"""

from dataclasses import dataclass, field


@dataclass
class MathTransformerConfig:
    """Toți hiperparametrii pentru Transformer-ul autoregresiv de matematică."""

    # ── Vocabular ──
    # Dimensiunea vocabularului; se încarcă din tokenizer (math_bpe.json)
    vocab_size: int = 8192

    # ── Arhitectură ──
    # Dimensiunea modelului (embedding + toate straturile interne)
    d_model: int = 256

    # Numărul de capete (heads) în multi-head attention
    # Fiecare cap operează pe d_k = d_model / n_heads = 32 dimensiuni
    n_heads: int = 8

    # Numărul de blocuri Transformer stivuite
    n_layers: int = 6

    # Dimensiunea stratului feed-forward intern (de obicei 4× d_model)
    d_ff: int = 1024

    # Lungimea maximă a secvenței (include și tokeniii speciali BOS/EOS)
    max_seq_len: int = 512

    # ── Regularizare ──
    # Probabilitate dropout aplicată uniform în model
    dropout: float = 0.1

    # ── Tokeni speciali ──
    # Indexul tokenului de padding (ignorat la calculul loss-ului)
    pad_idx: int = 0

    # Index BOS (Beginning Of Sequence)
    bos_idx: int = 2

    # Index EOS (End Of Sequence)
    eos_idx: int = 3

    # Index SEP (separator între întrebare și răspuns)
    sep_idx: int = 4


# ── Alias pentru compatibilitate cu codul existent ──
# Backend-ul și evaluate.py importă "TransformerConfig" din model.py
TransformerConfig = MathTransformerConfig
