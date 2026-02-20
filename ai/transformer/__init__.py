"""
MathTransformer — Transformer autoregresiv de la zero pentru exerciții BAC.

Exporturi principale:
    MathTransformer         — modelul complet
    MathTransformerConfig   — configurația hiperparametrilor
    TransformerConfig       — alias pentru compatibilitate
"""

from .config import MathTransformerConfig, TransformerConfig
from .model import MathTransformer
