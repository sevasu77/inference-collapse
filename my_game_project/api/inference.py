# api/inference.py
from models.inference import NormalizedInference

class InferenceNormalizer:
    """
    Decision Layer (判定層)

    Validates and normalizes raw inference data produced by
    any LLM (Gemma, GPT, Claude, etc.) into the system's
    canonical NormalizedInference model.
    """

    def normalize(self, raw_data: dict) -> NormalizedInference:
        """
        Validate a parsed inference payload and convert it into
    the canonical NormalizedInference model.
        """
        # TODO:
        # - Validate required fields
        # - Normalize confidence to a float in the range [0.0, 1.0]
        # - Clamp severity to an integer in the range [1, 5]
        # - Normalize contradiction into a consistent text format
        # - Apply safe defaults for missing or invalid values

        return NormalizedInference(
            report="Normalized text data extracted from raw input.",
            confidence=0.85,
            suspicion="HIGH",
            contradiction="Logical inconsistency detected.",
            severity=4,
        )
