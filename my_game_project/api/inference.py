# api/inference.py
from dataclasses import dataclass
from services.gemma import GemmaService

@dataclass(frozen=True)
class NormalizedInference:
    """
    Decision Layerによって正規化され、不変（Immutable）となった
    型安全な推論結果オブジェクト
    """
    report: str
    confidence_score: float  # 後で名前を変えたくなってもここ1箇所の変更で済む！
    suspicion: str
    contradiction: str
    severity_score: int

class InferenceNormalizer:
    """
    Decision Layer
    
    Gemmaの生の出力を、シミュレーション世界が安全に消費できる
    'NormalizedInference' 型へと検証・正規化する責務を持つ。
    """
    def __init__(self):
        self.gemma_service = GemmaService()

    def normalize_node_analysis(self, sector: str, evidence: str, force_fallacy: bool = False) -> NormalizedInference:
        """LLMの生JSONをパースし、厳密な型に当てはめてDecision Layerから出力する"""
        # TODO: 生のGemma出力をパースするロジック
        return NormalizedInference(
            report="Normalized analytical deduction text.",
            confidence_score=0.85,  # 0.0 ~ 1.0 に正規化済み
            suspicion="HIGH",
            contradiction="Logical discrepancy found.",
            severity_score=4         # 1 ~ 5 の整数を保証
        )
