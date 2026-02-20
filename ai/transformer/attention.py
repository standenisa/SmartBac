"""
Multi-Head Self-Attention scris manual, de la zero.

NU folosește torch.nn.MultiheadAttention — totul e implementat explicit:

1. Proiecții liniare separate pentru Query, Key, Value:
       Q = W_q · x,  K = W_k · x,  V = W_v · x

2. Împărțire pe n_heads capete (split heads):
       (batch, seq, d_model) → (batch, n_heads, seq, d_k)
       unde d_k = d_model / n_heads

3. Scaled Dot-Product Attention:
       Attention(Q, K, V) = softmax(Q · K^T / √d_k) · V

4. Causal mask (mască triunghiulară) pentru generare autoregresivă:
       Fiecare token poate "vedea" doar tokenii anteriori (inclusiv pe sine).
       Pozițiile viitoare sunt mascate cu -inf înainte de softmax.

5. Concatenare capete + proiecție de ieșire:
       output = W_o · Concat(head_1, ..., head_h)
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class MultiHeadSelfAttention(nn.Module):
    """
    Multi-Head Self-Attention implementat manual.

    Atenția multi-cap permite modelului să "privească" secvența din
    mai multe perspective simultan. Fiecare cap învață un alt tip de
    relație între tokeni (ex: un cap pentru relații sintactice,
    altul pentru relații matematice).

    Args:
        d_model:  Dimensiunea totală a modelului (ex: 256).
        n_heads:  Numărul de capete de atenție (ex: 8).
                  d_model trebuie să fie divisibil cu n_heads.
        dropout:  Probabilitate dropout pe scorurile de atenție.
    """

    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.1):
        super().__init__()

        # Verificăm că d_model se divide exact la n_heads
        assert d_model % n_heads == 0, (
            f"d_model ({d_model}) trebuie să fie divisibil cu n_heads ({n_heads})"
        )

        self.d_model = d_model          # Dimensiunea totală (ex: 256)
        self.n_heads = n_heads           # Număr capete (ex: 8)
        self.d_k = d_model // n_heads    # Dimensiunea per cap (ex: 32)

        # ── Proiecții liniare W_q, W_k, W_v, W_o ──
        # Fiecare proiectează din d_model în d_model (toate capetele deodată)
        self.W_q = nn.Linear(d_model, d_model)  # Proiecție Query
        self.W_k = nn.Linear(d_model, d_model)  # Proiecție Key
        self.W_v = nn.Linear(d_model, d_model)  # Proiecție Value
        self.W_o = nn.Linear(d_model, d_model)  # Proiecție de ieșire (după concat)

        # Dropout pe scorurile de atenție (înainte de înmulțirea cu V)
        self.attn_dropout = nn.Dropout(p=dropout)

        # Dropout pe ieșirea finală (după proiecția W_o)
        self.output_dropout = nn.Dropout(p=dropout)

    def forward(
        self,
        x: torch.Tensor,
        causal_mask: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """
        Forward pass pentru self-attention.

        Args:
            x:           (batch, seq_len, d_model) — reprezentările tokenilor.
            causal_mask: (1, 1, seq_len, seq_len) — mască booleană unde
                         True = poziție mascată (token viitor, nu poate fi văzut).
                         Dacă None, nu se aplică nicio mască.

        Returns:
            output: (batch, seq_len, d_model) — reprezentările actualizate.
        """
        batch_size, seq_len, _ = x.shape

        # ── Pas 1: Calculăm Q, K, V prin proiecțiile liniare ──
        # Forma: (batch, seq_len, d_model)
        Q = self.W_q(x)
        K = self.W_k(x)
        V = self.W_v(x)

        # ── Pas 2: Împărțim pe capete (split heads) ──
        # (batch, seq_len, d_model) → (batch, seq_len, n_heads, d_k)
        # → transpose → (batch, n_heads, seq_len, d_k)
        Q = Q.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)

        # ── Pas 3: Scaled Dot-Product Attention ──
        # Scoruri: Q · K^T, formă (batch, n_heads, seq_len, seq_len)
        # Scalăm cu √d_k pentru a evita gradienți prea mici din softmax
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        # ── Pas 4: Aplicăm masca cauzală (dacă există) ──
        # Masca pune -inf pe pozițiile viitoare → softmax le face ~0
        if causal_mask is not None:
            scores = scores.masked_fill(causal_mask, float("-inf"))

        # ── Pas 5: Softmax pe ultima dimensiune (seq_len a lui K) ──
        # Rezultat: ponderi de atenție, sumă = 1 pe fiecare rând
        attn_weights = F.softmax(scores, dim=-1)

        # Aplicăm dropout pe ponderile de atenție (regularizare)
        attn_weights = self.attn_dropout(attn_weights)

        # ── Pas 6: Înmulțim ponderile cu V ──
        # (batch, n_heads, seq_len, seq_len) @ (batch, n_heads, seq_len, d_k)
        # → (batch, n_heads, seq_len, d_k)
        attn_output = torch.matmul(attn_weights, V)

        # ── Pas 7: Concatenăm capetele (merge heads) ──
        # (batch, n_heads, seq_len, d_k) → transpose → (batch, seq_len, n_heads, d_k)
        # → reshape → (batch, seq_len, d_model)
        attn_output = (
            attn_output
            .transpose(1, 2)                                # (batch, seq, n_heads, d_k)
            .contiguous()                                    # asigurăm memorie contiguă
            .view(batch_size, seq_len, self.d_model)         # (batch, seq, d_model)
        )

        # ── Pas 8: Proiecția de ieșire W_o ──
        output = self.W_o(attn_output)
        output = self.output_dropout(output)

        return output


def create_causal_mask(seq_len: int, device: torch.device) -> torch.Tensor:
    """
    Creează masca cauzală (triunghiulară superioară) pentru atenție autoregresivă.

    Masca este un tensor boolean de formă (1, 1, seq_len, seq_len) unde:
        - True  = poziție MASCATĂ (token viitor, nu poate fi văzut)
        - False = poziție VIZIBILĂ (token curent sau anterior)

    Exemplu pentru seq_len=4:
        [[False,  True,  True,  True],    ← tokenul 0 vede doar tokenul 0
         [False, False,  True,  True],    ← tokenul 1 vede tokenii 0, 1
         [False, False, False,  True],    ← tokenul 2 vede tokenii 0, 1, 2
         [False, False, False, False]]    ← tokenul 3 vede toți tokenii

    Args:
        seq_len: Lungimea secvenței.
        device:  Device-ul pe care se creează tensorul.

    Returns:
        Tensor boolean de formă (1, 1, seq_len, seq_len).
    """
    # torch.triu cu diagonal=1 returnează matricea triunghiulară superioară
    # cu 1 deasupra diagonalei principale (exclusiv diagonala)
    mask = torch.triu(
        torch.ones(seq_len, seq_len, device=device, dtype=torch.bool),
        diagonal=1,  # 1 = deasupra diagonalei (exclude diagonala)
    )

    # Adăugăm dimensiunile batch și heads: (1, 1, seq_len, seq_len)
    # Broadcasting-ul le va extinde automat la (batch, n_heads, seq, seq)
    return mask.unsqueeze(0).unsqueeze(0)
