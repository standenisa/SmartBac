"""
Codificare pozițională sinusoidală (Sinusoidal Positional Encoding).

Implementează formulele din "Attention Is All You Need" (Vaswani et al., 2017):

    PE(pos, 2i)     = sin(pos / 10000^(2i / d_model))
    PE(pos, 2i + 1) = cos(pos / 10000^(2i / d_model))

unde:
    pos = poziția tokenului în secvență (0, 1, 2, ...)
    i   = indexul dimensiunii (0, 1, ..., d_model/2 - 1)

Matricea PE este precalculată o singură dată la construcție și stocată
ca buffer PyTorch (NU se antrenează, dar se mută automat pe device-ul
corect și face parte din state_dict).
"""

import math
import torch
import torch.nn as nn


class SinusoidalPositionalEncoding(nn.Module):
    """
    Adaugă informație despre poziția fiecărui token în secvență.

    Fără acest modul, Transformer-ul nu ar avea nicio noțiune de ordine —
    atenția operează pe mulțimi, nu pe secvențe. Codificarea sinusoidală
    rezolvă asta fără parametri antrenabili.

    Args:
        d_model:  Dimensiunea embedding-ului (trebuie să fie par).
        max_len:  Lungimea maximă a secvenței pe care o suportăm.
        dropout:  Probabilitate dropout aplicată DUPĂ adunarea PE.
    """

    def __init__(self, d_model: int, max_len: int = 2048, dropout: float = 0.1):
        super().__init__()

        # Stratul de dropout aplicat după adunarea embedding + PE
        self.dropout = nn.Dropout(p=dropout)

        # ── Precalculăm matricea de codificare pozițională ──
        # Formă: (max_len, d_model) — o linie per poziție
        pe = torch.zeros(max_len, d_model)

        # Vector de poziții: [0, 1, 2, ..., max_len-1] cu formă (max_len, 1)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)

        # Termenul de scalare exponențială: e^(-(2i / d_model) * ln(10000))
        # Echivalent cu 1 / 10000^(2i / d_model), dar stabil numeric
        # Calculăm pentru indicii pari: 0, 2, 4, ..., d_model-2
        div_term = torch.exp(
            torch.arange(0, d_model, 2, dtype=torch.float)
            * (-math.log(10000.0) / d_model)
        )

        # Dimensiunile pare: sin(pos * div_term)
        pe[:, 0::2] = torch.sin(position * div_term)

        # Dimensiunile impare: cos(pos * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        # Adăugăm dimensiunea batch: (1, max_len, d_model)
        # Astfel se poate aduna direct peste orice batch size
        pe = pe.unsqueeze(0)

        # Înregistrăm ca buffer: NU este parametru antrenabil,
        # dar face parte din state_dict și se mută pe device cu .to()
        self.register_buffer("pe", pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Adaugă codificarea pozițională la embedding-urile de intrare.

        Args:
            x: Tensor de formă (batch, seq_len, d_model) — embedding-urile tokenilor.

        Returns:
            Tensor de formă (batch, seq_len, d_model) cu PE adunată și dropout aplicat.
        """
        # Luăm doar primele seq_len poziții din buffer-ul precalculat
        # self.pe are forma (1, max_len, d_model), x are (batch, seq_len, d_model)
        # Broadcasting-ul pe dimensiunea batch se face automat
        seq_len = x.size(1)
        x = x + self.pe[:, :seq_len, :]

        # Aplicăm dropout (dezactivat automat în model.eval())
        return self.dropout(x)
