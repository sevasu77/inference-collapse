# models/inference.py
from dataclasses import dataclass

@dataclass(frozen=True)
class NormalizedInference:
    """Decision Layerによって正規化され、不変となった型安全な推論結果モデル"""
    report: str
    confidence_score: float
    suspicion: str
    contradiction: str
    severity_score: int
