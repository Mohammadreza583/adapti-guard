from dataclasses import dataclass

from src.adapti_guard.core.models import (
    DefenseAction,
    RiskAssessment,
    RiskLevel,
)


@dataclass
class PolicyDecision:
    action: DefenseAction
    reason: str


class DefensePolicyEngine:

    def decide(
        self,
        risk: RiskAssessment,
        tool_sensitive: bool = False,
        defense_level: int = 0,
    ) -> PolicyDecision:

        if defense_level not in (0, 1, 2, 3):
            raise ValueError(
                f"Unsupported defense level: {defense_level}"
            )

        # High risk with a sensitive tool uses tool restriction
        # to preserve security while maintaining utility.
        if risk.level == RiskLevel.HIGH:

            if tool_sensitive:
                return PolicyDecision(
                    action=DefenseAction.TOOL_RESTRICTION,
                    reason="high_risk_sensitive_tool",
                )

            return PolicyDecision(
                action=DefenseAction.BLOCK,
                reason="high_risk_block",
            )

        # Adaptive escalation for LOW risk.
        if risk.level == RiskLevel.LOW:

            if defense_level >= 3:
                return PolicyDecision(
                    action=DefenseAction.BLOCK,
                    reason="adaptive_low_risk_level_3",
                )

            if defense_level == 2:
                return PolicyDecision(
                    action=DefenseAction.TOOL_RESTRICTION,
                    reason="adaptive_low_risk_level_2",
                )

            if defense_level == 1:
                return PolicyDecision(
                    action=DefenseAction.SANITIZE,
                    reason="adaptive_low_risk_level_1",
                )

            if tool_sensitive:
                return PolicyDecision(
                    action=DefenseAction.TOOL_RESTRICTION,
                    reason="low_risk_tool_sensitive",
                )

            return PolicyDecision(
                action=DefenseAction.NO_INTERVENTION,
                reason="low_risk",
            )

        # Adaptive escalation for MEDIUM risk.
        if risk.level == RiskLevel.MEDIUM:

            if defense_level >= 3:
                return PolicyDecision(
                    action=DefenseAction.BLOCK,
                    reason="adaptive_medium_risk_level_3",
                )

            if defense_level >= 2 or tool_sensitive:
                return PolicyDecision(
                    action=DefenseAction.TOOL_RESTRICTION,
                    reason="adaptive_medium_risk_level_2",
                )

            return PolicyDecision(
                action=DefenseAction.SANITIZE,
                reason="medium_risk",
            )

        raise ValueError(
            f"Unsupported risk level: {risk.level}"
        )
