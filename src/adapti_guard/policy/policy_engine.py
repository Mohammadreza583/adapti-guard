from dataclasses import dataclass

from src.adapti_guard.core.models import DefenseAction, RiskLevel
from src.adapti_guard.risk.risk_engine import RiskAssessment


@dataclass
class PolicyDecision:
    action: DefenseAction
    reason: str


class DefensePolicyEngine:
    """
    Utility-aware adaptive defense policy.

    Risk determines the baseline defense.

    Historical defense level provides additional protection
    only when the current risk justifies it.

    The policy avoids permanently blocking low-risk requests.
    """

    def decide(
        self,
        risk: RiskAssessment,
        tool_sensitive: bool = False,
        defense_level: int = 0,
    ) -> PolicyDecision:

        if defense_level < 0 or defense_level > 3:
            raise ValueError(
                f"Unsupported defense level: {defense_level}"
            )

        # -------------------------------------------------
        # Baseline policy from current risk
        # -------------------------------------------------

        if risk.level == RiskLevel.LOW:

            if tool_sensitive:
                baseline = DefenseAction.TOOL_RESTRICTION
                reason = "low_risk_tool_sensitive"
            else:
                baseline = DefenseAction.NO_INTERVENTION
                reason = "low_risk"

        elif risk.level == RiskLevel.MEDIUM:

            if tool_sensitive:
                baseline = DefenseAction.TOOL_RESTRICTION
                reason = "medium_risk_tool_sensitive"
            else:
                baseline = DefenseAction.SANITIZE
                reason = "medium_risk"

        elif risk.level == RiskLevel.HIGH:

            if tool_sensitive:
                baseline = DefenseAction.TOOL_RESTRICTION
                reason = "high_risk_tool_sensitive"
            else:
                baseline = DefenseAction.BLOCK
                reason = "high_risk"

        else:
            raise ValueError(
                f"Unsupported risk level: {risk.level}"
            )

        # -------------------------------------------------
        # Adaptive escalation
        # -------------------------------------------------

        strength = {
            DefenseAction.NO_INTERVENTION: 0,
            DefenseAction.SANITIZE: 1,
            DefenseAction.TOOL_RESTRICTION: 2,
            DefenseAction.BLOCK: 3,
        }

        adaptive_action = {
            0: DefenseAction.NO_INTERVENTION,
            1: DefenseAction.SANITIZE,
            2: DefenseAction.TOOL_RESTRICTION,
            3: DefenseAction.BLOCK,
        }[defense_level]

        # -------------------------------------------------
        # Important:
        #
        # Do NOT let a historical level permanently block
        # LOW-risk interactions.
        #
        # Level 1/2 can strengthen LOW/MEDIUM risk.
        # Level 3 only forces BLOCK for MEDIUM/HIGH.
        # -------------------------------------------------

        if risk.level == RiskLevel.LOW:

            if defense_level == 1:
                return PolicyDecision(
                    action=DefenseAction.SANITIZE,
                    reason="adaptive_low_risk_level_1",
                )

            if defense_level >= 2:
                return PolicyDecision(
                    action=DefenseAction.TOOL_RESTRICTION,
                    reason="adaptive_low_risk_level_2",
                )

            return PolicyDecision(
                action=baseline,
                reason=reason,
            )

        # MEDIUM risk

        if risk.level == RiskLevel.MEDIUM:

            if defense_level >= 3:
                return PolicyDecision(
                    action=DefenseAction.BLOCK,
                    reason="adaptive_medium_risk_level_3",
                )

            if defense_level >= 2:
                return PolicyDecision(
                    action=DefenseAction.TOOL_RESTRICTION,
                    reason="adaptive_medium_risk_level_2",
                )

            if defense_level >= 1:
                return PolicyDecision(
                    action=DefenseAction.SANITIZE,
                    reason="adaptive_medium_risk_level_1",
                )

            return PolicyDecision(
                action=baseline,
                reason=reason,
            )

        # HIGH risk

        return PolicyDecision(
            action=baseline,
            reason=reason,
        )
