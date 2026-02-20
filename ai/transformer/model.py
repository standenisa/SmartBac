"""
MathTransformer — model Transformer autoregresiv (decoder-only) scris de la zero.

Arhitectura (similară cu GPT-2, dar mai mică):

    Input token IDs
         │
         ▼
    Token Embedding  ×  √d_model   (scalare ca în paper-ul original)
         │
         ▼
    + Positional Encoding (sinusoidal, precalculat)
         │
         ▼
    ┌─────────────────────┐
    │  TransformerBlock #1 │  ← Pre-Norm: LN → Attention → +residual → LN → FFN → +residual
    │  TransformerBlock #2 │
    │        ...           │
    │  TransformerBlock #6 │
    └─────────────────────┘
         │
         ▼
    LayerNorm final
         │
         ▼
    Linear(d_model → vocab_size)   ← "LM head" — produce logits per token
         │
         ▼
    Logits (batch, seq_len, vocab_size)

Generarea (inferență):
    Pornind de la un prompt (ex: "<BOS> Rezolvă ecuația: 2x + 3 = 7 <SEP>"),
    modelul generează câte un token pe rând folosind top-k sampling cu temperatură.
    Se oprește la <EOS> sau la limita de tokeni.

Număr parametri cu config implicit (vocab=1347, d_model=256, n_layers=6):
    ~5.4M parametri antrenabili.
"""

import os
import sys
import math
import torch
import torch.nn as nn

from .config import MathTransformerConfig, TransformerConfig
from .positional_encoding import SinusoidalPositionalEncoding
from .transformer_block import TransformerBlock
from .attention import create_causal_mask


class MathTransformer(nn.Module):
    """
    Transformer autoregresiv (decoder-only) pentru rezolvarea exercițiilor
    de matematică BAC.

    Modelul primește o secvență de tokeni și prezice URMĂTORUL token la
    fiecare poziție. La antrenament se folosește teacher forcing (toate
    pozițiile deodată). La inferență se generează câte un token pe rând.

    Args:
        config: MathTransformerConfig cu toți hiperparametrii.
    """

    def __init__(self, config: MathTransformerConfig):
        super().__init__()

        # Salvăm configurația pentru serializare / reconstrucție
        self.config = config

        # ── Token Embedding ──
        # Transformă indicii de tokeni (ints) în vectori denși de dimensiune d_model
        # padding_idx=pad_idx face ca embedding-ul pentru <PAD> să fie mereu zero
        self.token_embedding = nn.Embedding(
            num_embeddings=config.vocab_size,
            embedding_dim=config.d_model,
            padding_idx=config.pad_idx,
        )

        # ── Positional Encoding (sinusoidal, NU se antrenează) ──
        self.positional_encoding = SinusoidalPositionalEncoding(
            d_model=config.d_model,
            max_len=config.max_seq_len,
            dropout=config.dropout,
        )

        # ── Stiva de blocuri Transformer ──
        # Fiecare bloc: Pre-Norm → Self-Attention → +residual → Pre-Norm → FFN → +residual
        self.blocks = nn.ModuleList([
            TransformerBlock(
                d_model=config.d_model,
                n_heads=config.n_heads,
                d_ff=config.d_ff,
                dropout=config.dropout,
            )
            for _ in range(config.n_layers)
        ])

        # ── LayerNorm final (necesar pentru Pre-Norm) ──
        # În arhitectura Pre-Norm, ultimul bloc nu are LayerNorm "după",
        # deci adăugăm unul explicit înainte de proiecția finală
        self.final_norm = nn.LayerNorm(config.d_model)

        # ── LM Head: proiecție liniară d_model → vocab_size ──
        # Produce logits (scoruri nenormalizate) pentru fiecare token din vocabular
        # Softmax-ul se aplică EXTERN (în CrossEntropyLoss sau la sampling)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

        # ── Inițializarea greutăților ──
        self._init_weights()

        # ── Printăm informații despre model ──
        n_params = sum(p.numel() for p in self.parameters())
        n_trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        print(f"[MathTransformer] Parametri totali:      {n_params:,}")
        print(f"[MathTransformer] Parametri antrenabili:  {n_trainable:,}")
        print(f"[MathTransformer] Vocab size:             {config.vocab_size}")
        print(f"[MathTransformer] d_model={config.d_model}, n_heads={config.n_heads}, "
              f"n_layers={config.n_layers}, d_ff={config.d_ff}")

    def _init_weights(self):
        """
        Inițializarea greutăților modelului.

        Folosim inițializare normală cu deviație standard mică (0.02) pentru
        straturile liniare și embedding-uri — standard în GPT-2 și modele similare.
        Bias-urile sunt inițializate la zero.
        """
        for module in self.modules():
            if isinstance(module, nn.Linear):
                # Inițializare normală cu σ = 0.02 (standard GPT-2)
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.Embedding):
                # Embedding-urile se inițializează la fel
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
                # Asigurăm că padding-ul rămâne zero
                if module.padding_idx is not None:
                    with torch.no_grad():
                        module.weight[module.padding_idx].fill_(0)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        """
        Forward pass: primește tokeni, returnează logits.

        Args:
            input_ids: (batch, seq_len) — indicii tokenilor de intrare.

        Returns:
            logits: (batch, seq_len, vocab_size) — scoruri pentru fiecare token
                    din vocabular, la fiecare poziție.

        La antrenament:
            input  = sequence[:-1]   (tot minus ultimul token)
            labels = sequence[1:]    (tot minus primul token)
            loss = CrossEntropyLoss(logits.view(-1, vocab), labels.view(-1))
        """
        batch_size, seq_len = input_ids.shape
        device = input_ids.device

        # Pas 1: Token embedding + scalare cu √d_model (ca în paper-ul original)
        # Scalarea compensează faptul că embedding-urile sunt mici inițial
        x = self.token_embedding(input_ids) * math.sqrt(self.config.d_model)

        # Pas 2: Adaugă codificarea pozițională sinusoidală
        x = self.positional_encoding(x)

        # Pas 3: Creăm masca cauzală (triunghiulară superioară)
        # Previne fiecare token să "vadă" tokenii viitori
        causal_mask = create_causal_mask(seq_len, device)

        # Pas 4: Trecem prin stiva de blocuri Transformer
        for block in self.blocks:
            x = block(x, causal_mask=causal_mask)

        # Pas 5: LayerNorm final (necesar pentru Pre-Norm architecture)
        x = self.final_norm(x)

        # Pas 6: Proiecția LM head → logits
        logits = self.lm_head(x)

        return logits

    @torch.no_grad()
    def generate(
        self,
        input_ids: torch.Tensor,
        max_new_tokens: int = 200,
        temperature: float = 0.7,
        top_k: int = 50,
        eos_idx: int | None = None,
    ) -> torch.Tensor:
        """
        Generare autoregresivă cu top-k sampling și temperatură.

        Algoritmul:
            1. Pornește cu prompt-ul (input_ids)
            2. La fiecare pas:
               a. Trece secvența curentă prin model → logits
               b. Ia logits-urile de la ULTIMA poziție
               c. Aplică temperatura (scalare)
               d. Selectează top-k cele mai probabile tokeni
               e. Eșantionează din distribuția normalizată (sampling)
               f. Adaugă tokenul generat la secvență
            3. Se oprește la <EOS> sau la limita de tokeni

        De ce top-k sampling (nu greedy)?
            Greedy (argmax) produce text repetitiv și "sigur" dar plictisitor.
            Top-k sampling permite diversitate controlată: modelul alege
            din cele mai probabile k opțiuni, proporțional cu probabilitatea lor.
            Temperatura controlează "creativitatea":
                T < 1.0 → mai conservator (preferă tokenul cel mai probabil)
                T = 1.0 → fără modificare
                T > 1.0 → mai creativ (distribuție mai uniformă)

        Args:
            input_ids:      (batch, seq_len) — prompt-ul tokenizat.
            max_new_tokens: Numărul maxim de tokeni noi de generat.
            temperature:    Temperatura de sampling (0.7 = ușor conservator).
            top_k:          Câți tokeni candidați păstrăm la fiecare pas.
            eos_idx:        Indexul tokenului <EOS>. Dacă None, folosim config.

        Returns:
            (batch, seq_len + generated_len) — secvența completă cu tokenii generați.
        """
        self.eval()

        if eos_idx is None:
            eos_idx = self.config.eos_idx

        # Copiem input_ids pentru a nu modifica tensorul original
        generated = input_ids.clone()

        # Ținem evidența secvențelor care au generat deja <EOS>
        batch_size = input_ids.size(0)
        finished = torch.zeros(batch_size, dtype=torch.bool, device=input_ids.device)

        for _ in range(max_new_tokens):
            # Tăiem secvența dacă depășește max_seq_len
            # (păstrăm ultimii max_seq_len tokeni ca context)
            if generated.size(1) > self.config.max_seq_len:
                context = generated[:, -self.config.max_seq_len:]
            else:
                context = generated

            # Forward pass → logits de formă (batch, seq_len, vocab_size)
            logits = self.forward(context)

            # Luăm logits-urile doar de la ULTIMA poziție
            # (predicția pentru următorul token)
            next_logits = logits[:, -1, :]  # (batch, vocab_size)

            # Aplicăm temperatura: scalăm logits-urile
            if temperature != 1.0:
                next_logits = next_logits / temperature

            # Top-k filtering: păstrăm doar cele mai probabile k tokeni
            if top_k > 0:
                # Găsim al k-lea cel mai mare logit (prag)
                top_k_values, _ = torch.topk(next_logits, min(top_k, next_logits.size(-1)))
                threshold = top_k_values[:, -1].unsqueeze(-1)  # (batch, 1)

                # Mascăm toate tokenele sub prag cu -inf
                next_logits = next_logits.masked_fill(next_logits < threshold, float("-inf"))

            # Convertim logits în probabilități cu softmax
            probs = torch.softmax(next_logits, dim=-1)

            # Eșantionăm UN token din distribuția de probabilitate
            next_token = torch.multinomial(probs, num_samples=1)  # (batch, 1)

            # Pentru secvențele terminate, înlocuim cu PAD
            next_token = next_token.masked_fill(finished.unsqueeze(1), self.config.pad_idx)

            # Adăugăm tokenul generat la secvență
            generated = torch.cat([generated, next_token], dim=1)

            # Verificăm dacă am generat <EOS>
            finished = finished | (next_token.squeeze(1) == eos_idx)

            # Dacă TOATE secvențele au terminat, ne oprim devreme
            if finished.all():
                break

        return generated

    @classmethod
    def from_config(cls, config: MathTransformerConfig) -> "MathTransformer":
        """Construiește un MathTransformer dintr-un obiect de configurație."""
        return cls(config)

    @classmethod
    def from_pretrained(cls, checkpoint_path: str, device: str = "cpu") -> "MathTransformer":
        """
        Încarcă un model antrenat dintr-un checkpoint salvat.

        Args:
            checkpoint_path: Calea către fișierul .pt cu checkpoint-ul.
            device:          Device-ul pe care se încarcă ('cpu', 'mps', 'cuda').

        Returns:
            Model MathTransformer cu greutățile încărcate, în modul eval().
        """
        checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
        config = checkpoint["config"]
        model = cls(config)
        model.load_state_dict(checkpoint["model_state_dict"])
        model.to(device)
        model.eval()
        return model
