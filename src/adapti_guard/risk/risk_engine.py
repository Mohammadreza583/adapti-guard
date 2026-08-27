from dataclasses import dataclass

from src.adapti_guard.core.models import RiskLevel
from src.adapti_guard.detector.prompt_injection_detector import DetectionResult


@dataclass
class RiskAssessment:
    score: float
    level: RiskLevel
    reasons: list[str]


class RiskAssessmentEngine:
    """
    Interpretable risk assessment engine for ADAPTI-GUARD MVP.
    """

    def __init__(
        self,
        low_threshold: float = 0.30,
        high_threshold: float = 0.70,
    ):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

    def assess(
        self,
        detection: DetectionResult,
        tool_sensitive: bool = False,
        contextual_risk: float = 0.0,
        historical_attack: float = 0.0,
    ) -> RiskAssessment:

        contextual_risk = max(0.0, min(1.0, contextual_risk))
        historical_attack = max(0.0, min(1.0, historical_attack))

        score = (
            0.60 * detection.score
            + 0.20 * float(tool_sensitive)
            + 0.15 * contextual_risk
            + 0.05 * historical_attack
        )

        # Injection presence creates a minimum risk floor.
        if detection.is_injection:
            score = max(score, 0.35)

        score = max(0.0, min(1.0, score))

        reasons = []

        if detection.is_injection:
            reasons.append("prompt_injection_detected")

        if tool_sensitive:
            reasons.append("sensitive_tool_context")

        if contextual_risk > 0:
            reasons.append("elevated_contextual_risk")

        if historical_attack > 0:
            reasons.append("historical_attack_evidence")

        if score < self.low_threshold:
            level = RiskLevel.LOW
        elif score < self.high_threshold:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.HIGH

        return RiskAssessment(
            score=round(score, 4),
            level=level,
            reasons=reasons,
        )
