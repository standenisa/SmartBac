"""
Tokenizer Service — lazy-loads MathBPETokenizer for the backend.
"""

import os
import sys

# Add project root so we can import ai.tokenizer
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from ai.tokenizer.bpe import MathBPETokenizer

_TOKENIZER_PATH = os.path.join(_PROJECT_ROOT, "ai", "tokenizer", "math_bpe.json")

_tokenizer: MathBPETokenizer | None = None
_loaded: bool = False


def _get_tokenizer() -> MathBPETokenizer | None:
    """Lazy-load the tokenizer from disk. Returns None if not trained yet."""
    global _tokenizer, _loaded
    if _loaded:
        return _tokenizer
    _loaded = True

    if not os.path.isfile(_TOKENIZER_PATH):
        return None

    _tokenizer = MathBPETokenizer()
    _tokenizer.load(_TOKENIZER_PATH)
    return _tokenizer


def _require_tokenizer() -> MathBPETokenizer:
    tok = _get_tokenizer()
    if tok is None:
        raise RuntimeError("Tokenizer not trained yet. Run ai/tokenizer/train_tokenizer.py first.")
    return tok


def encode(text: str) -> list[int]:
    """Encode text to token IDs."""
    return _require_tokenizer().encode(text)


def decode(ids: list[int]) -> str:
    """Decode token IDs back to text."""
    return _require_tokenizer().decode(ids)


def get_vocab_info() -> dict:
    """Return vocabulary metadata."""
    tok = _get_tokenizer()
    if tok is None:
        return {
            "status": "not_loaded",
            "vocab_size": 0,
            "special_tokens": list(MathBPETokenizer.SPECIAL_TOKENS.keys()),
            "num_merges": 0,
        }
    return {
        "status": "loaded",
        "vocab_size": len(tok),
        "special_tokens": list(tok.SPECIAL_TOKENS.keys()),
        "num_merges": len(tok.merges),
        "num_latex_tokens": len(tok.LATEX_TOKENS),
        "num_operator_tokens": len(tok.MATH_OPERATORS),
    }
