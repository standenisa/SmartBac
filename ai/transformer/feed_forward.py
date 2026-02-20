"""
Rețea Feed-Forward position-wise (FFN).

Fiecare poziție din secvență trece independent prin aceleași două
straturi liniare cu o activare GELU între ele:

    FFN(x) = W₂ · GELU(W₁ · x + b₁) + b₂

unde:
    W₁ ∈ ℝ^(d_model × d_ff)    — expandează dimensiunea de 4×
    W₂ ∈ ℝ^(d_ff × d_model)    — comprimă înapoi la d_model

De ce GELU și nu ReLU?
    GELU (Gaussian Error Linear Unit) este activarea standard în
    modelele moderne (GPT-2, BERT, LLaMA). Spre deosebire de ReLU
    care taie brusc la 0, GELU are o tranziție netedă care permite
    gradienți mai buni la valori mici negative.

    GELU(x) = x · Φ(x), unde Φ este CDF-ul distribuției normale.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class FeedForward(nn.Module):
    """
    Position-wise Feed-Forward Network cu activare GELU.

    "Position-wise" înseamnă că aceleași greutăți W₁, W₂ sunt aplicate
    independent pe FIECARE poziție (token) din secvență. Nu există
    interacțiune între poziții — atenția se ocupă de asta.

    Rolul FFN: după ce atenția a "amestecat" informația între tokeni,
    FFN-ul aplică o transformare neliniară pe fiecare token individual,
    permițând modelului să învețe relații complexe.

    Args:
        d_model: Dimensiunea de intrare și ieșire (ex: 256).
        d_ff:    Dimensiunea stratului ascuns (ex: 1024 = 4 × d_model).
        dropout: Probabilitate dropout aplicată după activare.
    """

    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        super().__init__()

        # Primul strat liniar: expandează d_model → d_ff
        # Permite modelului să lucreze într-un spațiu cu mai multe dimensiuni
        self.W1 = nn.Linear(d_model, d_ff)

        # Al doilea strat liniar: comprimă d_ff → d_model
        # Readuce reprezentarea la dimensiunea originală
        self.W2 = nn.Linear(d_ff, d_model)

        # Dropout aplicat între cele două straturi (regularizare)
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass prin FFN.

        Calculul: output = W₂ · Dropout(GELU(W₁ · x + b₁)) + b₂

        Args:
            x: Tensor de formă (batch, seq_len, d_model).

        Returns:
            Tensor de formă (batch, seq_len, d_model).
        """
        # Pas 1: Proiecția liniară W₁ · x + b₁ → (batch, seq_len, d_ff)
        hidden = self.W1(x)

        # Pas 2: Activare GELU (Gaussian Error Linear Unit)
        # GELU(x) ≈ 0.5 * x * (1 + tanh(√(2/π) * (x + 0.044715 * x³)))
        hidden = F.gelu(hidden)

        # Pas 3: Dropout pe activări (regularizare)
        hidden = self.dropout(hidden)

        # Pas 4: Proiecția liniară W₂ · hidden + b₂ → (batch, seq_len, d_model)
        output = self.W2(hidden)

        return output
