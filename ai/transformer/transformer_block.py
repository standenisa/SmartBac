"""
Bloc Transformer cu Pre-Norm (stilul GPT-2).

Un bloc Transformer combină atenția multi-cap cu rețeaua feed-forward,
folosind conexiuni reziduale și LayerNorm.

Există două stiluri de LayerNorm:

    Post-Norm (stilul original, "Attention Is All You Need"):
        x = LayerNorm(x + Attention(x))
        x = LayerNorm(x + FFN(x))

    Pre-Norm (stilul GPT-2, mai stabil la antrenament):
        x = x + Attention(LayerNorm(x))     ← LayerNorm ÎNAINTE de attention
        x = x + FFN(LayerNorm(x))           ← LayerNorm ÎNAINTE de FFN

Noi folosim Pre-Norm pentru că:
    1. Gradienții trec DIRECT prin conexiunea reziduală (fără LayerNorm pe drum)
    2. Antrenamentul este mai stabil, mai ales cu multe straturi
    3. Nu necesită warmup atât de lung
    4. Este standardul în GPT-2, GPT-3, LLaMA, și majoritatea LLM-urilor moderne
"""

import torch
import torch.nn as nn

from .attention import MultiHeadSelfAttention
from .feed_forward import FeedForward


class TransformerBlock(nn.Module):
    """
    Un singur bloc Transformer Pre-Norm (decoder-only, autoregresiv).

    Structura internă:
        ┌──────────────────────────┐
        │         Input x          │
        ├──────────────────────────┤
        │      LayerNorm(x)        │  ← normalizare ÎNAINTE de atenție
        │           │              │
        │   MultiHeadSelfAttention │  ← atenție cauzală (vede doar trecutul)
        │           │              │
        │      Dropout             │
        │           │              │
        │      x + output          │  ← conexiune reziduală
        ├──────────────────────────┤
        │      LayerNorm(x)        │  ← normalizare ÎNAINTE de FFN
        │           │              │
        │      FeedForward         │  ← transformare neliniară per poziție
        │           │              │
        │      Dropout             │
        │           │              │
        │      x + output          │  ← conexiune reziduală
        └──────────────────────────┘

    Args:
        d_model: Dimensiunea modelului (ex: 256).
        n_heads: Numărul de capete de atenție (ex: 8).
        d_ff:    Dimensiunea FFN internă (ex: 1024).
        dropout: Probabilitate dropout.
    """

    def __init__(self, d_model: int, n_heads: int, d_ff: int, dropout: float = 0.1):
        super().__init__()

        # ── LayerNorm #1: aplicat ÎNAINTE de self-attention ──
        # Normalizează media la 0 și deviația standard la 1 pe dimensiunea d_model
        self.norm1 = nn.LayerNorm(d_model)

        # ── Multi-Head Self-Attention cu mască cauzală ──
        self.attention = MultiHeadSelfAttention(d_model, n_heads, dropout)

        # ── Dropout #1: pe ieșirea din attention (regularizare) ──
        self.dropout1 = nn.Dropout(p=dropout)

        # ── LayerNorm #2: aplicat ÎNAINTE de feed-forward ──
        self.norm2 = nn.LayerNorm(d_model)

        # ── Feed-Forward Network cu GELU ──
        self.ffn = FeedForward(d_model, d_ff, dropout)

        # ── Dropout #2: pe ieșirea din FFN (regularizare) ──
        self.dropout2 = nn.Dropout(p=dropout)

    def forward(self, x: torch.Tensor, causal_mask: torch.Tensor | None = None) -> torch.Tensor:
        """
        Forward pass printr-un bloc Transformer Pre-Norm.

        Args:
            x:           (batch, seq_len, d_model) — reprezentările tokenilor.
            causal_mask: (1, 1, seq_len, seq_len) — mască cauzală booleană.

        Returns:
            (batch, seq_len, d_model) — reprezentările actualizate.
        """
        # ── Sub-blocul 1: Self-Attention cu Pre-Norm ──
        # Salvăm input-ul pentru conexiunea reziduală
        residual = x

        # Normalizăm ÎNAINTE de attention (Pre-Norm)
        x_norm = self.norm1(x)

        # Aplicăm self-attention cu mască cauzală
        attn_output = self.attention(x_norm, causal_mask=causal_mask)

        # Conexiunea reziduală: adunăm input-ul original cu ieșirea atenției
        # Acest lucru permite gradienților să treacă direct, fără degradare
        x = residual + self.dropout1(attn_output)

        # ── Sub-blocul 2: Feed-Forward cu Pre-Norm ──
        # Salvăm din nou pentru conexiunea reziduală
        residual = x

        # Normalizăm ÎNAINTE de FFN (Pre-Norm)
        x_norm = self.norm2(x)

        # Aplicăm FFN: W₂ · GELU(W₁ · x + b₁) + b₂
        ffn_output = self.ffn(x_norm)

        # Conexiunea reziduală: adunăm input-ul cu ieșirea FFN
        x = residual + self.dropout2(ffn_output)

        return x
