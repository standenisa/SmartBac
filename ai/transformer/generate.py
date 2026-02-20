"""
Script standalone de generare cu MathTransformer.

Încarcă un model antrenat și tokenizer-ul, primește un prompt (întrebare
de matematică) și generează răspunsul + pașii de rezolvare.

Utilizare:
    # Generare cu prompt din linia de comandă
    python -m ai.transformer.generate --prompt "Rezolvă ecuația: 3x - 5 = 7"

    # Cu parametri custom de sampling
    python -m ai.transformer.generate --prompt "Calculează derivata: f(x) = x^3" \\
        --max-tokens 200 --temperature 0.5 --top-k 30

    # Mod interactiv (prompt-uri repetate)
    python -m ai.transformer.generate --interactive

Parametri de sampling:
    --temperature  Controlează "creativitatea" (0.1 = conservator, 1.0 = normal)
    --top-k        Câți tokeni candidați la fiecare pas (50 = default)
    --max-tokens   Numărul maxim de tokeni de generat (200 = default)
"""

import argparse
import os
import sys
from pathlib import Path

import torch

# ── Adăugăm project root pentru importuri ──
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from ai.tokenizer.bpe import MathBPETokenizer
from ai.transformer.model import MathTransformer
from ai.transformer.config import MathTransformerConfig


# ═══════════════════════════════════════════════════════════════════════
# Funcția principală de generare
# ═══════════════════════════════════════════════════════════════════════

def generate(
    prompt: str,
    model: MathTransformer,
    tokenizer: MathBPETokenizer,
    device: torch.device,
    max_new_tokens: int = 200,
    temperature: float = 0.7,
    top_k: int = 50,
) -> str:
    """
    Generează un răspuns pentru un prompt de matematică.

    Procesul:
        1. Tokenizează prompt-ul: <BOS> + encode(prompt) + <SEP>
        2. Trimite la model.generate() cu top-k sampling
        3. Decodează tokenii generați înapoi în text
        4. Returnează doar partea generată (fără prompt)

    Args:
        prompt:         Textul întrebării (ex: "Rezolvă ecuația: 2x + 3 = 7").
        model:          Modelul MathTransformer antrenat.
        tokenizer:      Tokenizer-ul BPE.
        device:         Device-ul pe care rulează modelul.
        max_new_tokens: Numărul maxim de tokeni de generat.
        temperature:    Temperatura de sampling.
        top_k:          Câți tokeni candidați la fiecare pas.

    Returns:
        Textul generat (răspuns + pași de rezolvare).
    """
    # ── Tokenizăm prompt-ul ──
    # Format: <BOS> prompt_tokens <SEP>
    # <SEP> marchează: "acum generează răspunsul"
    bos_idx = MathBPETokenizer.SPECIAL_TOKENS["<BOS>"]
    sep_idx = MathBPETokenizer.SPECIAL_TOKENS["<SEP>"]
    eos_idx = MathBPETokenizer.SPECIAL_TOKENS["<EOS>"]

    prompt_ids = [bos_idx] + tokenizer.encode(prompt) + [sep_idx]
    input_tensor = torch.tensor([prompt_ids], dtype=torch.long).to(device)

    # ── Generare autoregresivă ──
    output_tensor = model.generate(
        input_tensor,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        eos_idx=eos_idx,
    )

    # ── Decodăm doar partea generată (fără prompt) ──
    full_ids = output_tensor[0].tolist()
    generated_ids = full_ids[len(prompt_ids):]

    # Eliminăm tokenii speciali din output (<PAD>, <EOS>)
    pad_idx = MathBPETokenizer.SPECIAL_TOKENS["<PAD>"]
    clean_ids = []
    for tid in generated_ids:
        if tid == eos_idx:
            break  # Ne oprim la <EOS>
        if tid == pad_idx:
            continue  # Sărim <PAD>
        clean_ids.append(tid)

    # Decodăm token IDs → text
    generated_text = tokenizer.decode(clean_ids)

    return generated_text


# ═══════════════════════════════════════════════════════════════════════
# Funcții de încărcare
# ═══════════════════════════════════════════════════════════════════════

def load_model_and_tokenizer(
    checkpoint_path: str | None = None,
    tokenizer_path: str | None = None,
) -> tuple[MathTransformer, MathBPETokenizer, torch.device]:
    """
    Încarcă modelul antrenat și tokenizer-ul.

    Args:
        checkpoint_path: Calea către checkpoint-ul modelului (.pt).
                         Dacă None, folosește calea implicită.
        tokenizer_path:  Calea către tokenizer-ul salvat (.json).
                         Dacă None, folosește calea implicită.

    Returns:
        (model, tokenizer, device) — gata de utilizare.
    """
    # ── Căi implicite ──
    if checkpoint_path is None:
        checkpoint_path = str(
            _PROJECT_ROOT / "ai" / "transformer" / "checkpoints" / "best_model.pt"
        )
    if tokenizer_path is None:
        tokenizer_path = str(
            _PROJECT_ROOT / "ai" / "tokenizer" / "math_bpe.json"
        )

    # ── Verificăm existența fișierelor ──
    if not os.path.exists(checkpoint_path):
        print(f"[EROARE] Checkpoint-ul nu a fost găsit: {checkpoint_path}")
        print("  Antrenează mai întâi: python -m ai.transformer.train")
        sys.exit(1)

    if not os.path.exists(tokenizer_path):
        print(f"[EROARE] Tokenizer-ul nu a fost găsit: {tokenizer_path}")
        print("  Antrenează mai întâi: python -m ai.tokenizer.train_tokenizer")
        sys.exit(1)

    # ── Device ──
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    print(f"[DEVICE] {device}")

    # ── Tokenizer ──
    tokenizer = MathBPETokenizer()
    tokenizer.load(tokenizer_path)
    print(f"[TOKENIZER] Încărcat: {len(tokenizer)} tokeni")

    # ── Model ──
    model = MathTransformer.from_pretrained(checkpoint_path, device=str(device))
    print(f"[MODEL] Încărcat din {checkpoint_path}")

    return model, tokenizer, device


# ═══════════════════════════════════════════════════════════════════════
# Mod interactiv
# ═══════════════════════════════════════════════════════════════════════

def interactive_mode(
    model: MathTransformer,
    tokenizer: MathBPETokenizer,
    device: torch.device,
    max_new_tokens: int = 200,
    temperature: float = 0.7,
    top_k: int = 50,
):
    """
    Mod interactiv: primește prompt-uri de la utilizator și generează răspunsuri.

    Scrie 'quit' sau 'exit' pentru a ieși.
    """
    print("\n" + "=" * 60)
    print("  MathTransformer — Mod Interactiv")
    print("  Scrie un exercițiu și apasă Enter.")
    print("  'quit' sau 'exit' pentru a ieși.")
    print("=" * 60 + "\n")

    while True:
        try:
            prompt = input("Exercițiu> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nLa revedere!")
            break

        if not prompt:
            continue
        if prompt.lower() in ("quit", "exit", "q"):
            print("La revedere!")
            break

        # Generăm răspunsul
        result = generate(
            prompt, model, tokenizer, device,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_k=top_k,
        )

        print(f"\n--- Răspuns ---")
        print(result)
        print("-" * 40 + "\n")


# ═══════════════════════════════════════════════════════════════════════
# CLI entry-point
# ═══════════════════════════════════════════════════════════════════════

def main():
    """Punct de intrare CLI pentru generare."""
    parser = argparse.ArgumentParser(
        description="Generare cu MathTransformer autoregresiv"
    )
    parser.add_argument(
        "--prompt", "-p", type=str, default=None,
        help="Prompt-ul (exercițiul) de rezolvat"
    )
    parser.add_argument(
        "--checkpoint", type=str, default=None,
        help="Calea către checkpoint-ul modelului (.pt)"
    )
    parser.add_argument(
        "--tokenizer", type=str, default=None,
        help="Calea către tokenizer-ul BPE (.json)"
    )
    parser.add_argument(
        "--max-tokens", type=int, default=200,
        help="Numărul maxim de tokeni de generat (default: 200)"
    )
    parser.add_argument(
        "--temperature", type=float, default=0.7,
        help="Temperatura de sampling (default: 0.7)"
    )
    parser.add_argument(
        "--top-k", type=int, default=50,
        help="Câți tokeni candidați la fiecare pas (default: 50)"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true",
        help="Rulează în mod interactiv"
    )

    args = parser.parse_args()

    # Încarcă model + tokenizer
    model, tokenizer, device = load_model_and_tokenizer(
        checkpoint_path=args.checkpoint,
        tokenizer_path=args.tokenizer,
    )

    # Mod interactiv
    if args.interactive:
        interactive_mode(
            model, tokenizer, device,
            max_new_tokens=args.max_tokens,
            temperature=args.temperature,
            top_k=args.top_k,
        )
        return

    # Mod single-prompt
    if args.prompt:
        result = generate(
            args.prompt, model, tokenizer, device,
            max_new_tokens=args.max_tokens,
            temperature=args.temperature,
            top_k=args.top_k,
        )
        print(f"\nPrompt: {args.prompt}")
        print(f"Răspuns: {result}")
        return

    # Dacă nu s-a specificat nimic, prompt implicit
    default_prompt = "Rezolvă ecuația: 2x + 3 = 7"
    print(f"\nNiciun prompt specificat. Folosesc: \"{default_prompt}\"")
    result = generate(
        default_prompt, model, tokenizer, device,
        max_new_tokens=args.max_tokens,
        temperature=args.temperature,
        top_k=args.top_k,
    )
    print(f"Răspuns: {result}")


if __name__ == "__main__":
    main()
