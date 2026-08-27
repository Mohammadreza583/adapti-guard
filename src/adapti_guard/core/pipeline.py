from dataclasses import dataclass
from typing import Any

from src.adapti_guard.detector.prompt_injection_detector import (
    PromptInjectionDetector,
)
from src.adapti_guard.risk.risk_engine import RiskAssessmentEngine
from src.adapti_guard.policy.policy_engine import DefensePolicyEngine
from src.adapti_guard.defense.action_layer import DefenseActionLayer


@dataclass
class PipelineResult:
    input_text: str
    detection: Any
    risk: Any
    decision: Any
    defense: Any
    response: str


class DefensePipeline:
    """
    End-to-end ADAPTI-GUARD MVP defense pipeline.

    Detector -> Risk -> Policy -> Defense -> Agent
    """

    def __init__(self):
        self.detector = PromptInjectionDetector()
        self.risk_engine = RiskAssessmentEngine()
        self.policy_engine = DefensePolicyEngine()
        self.action_layer = DefenseActionLayer()

    def run(
        self,
        text: str,
        contextual_risk: float = 0.0,
        tool_sensitive: bool = False,
    ) -> PipelineResult:

        # 1. Detect prompt injection
        detection = self.detector.detect(text)

        # 2. Estimate risk
        risk = self.risk_engine.assess(
            detection,
            contextual_risk=contextual_risk,
        )

        # 3. Select defense action
        decision = self.policy_engine.decide(
            risk,
            tool_sensitive=tool_sensitive,
        )

        # 4. Execute defense
        defense = self.action_layer.execute(
            decision.action,
            text,
        )

        # 5. Simulated protected-agent response
        response = self._agent_response(
            defense.allowed,
            defense.content,
        )

        return PipelineResult(
            input_text=text,
            detection=detection,
            risk=risk,
            decision=decision,
            defense=defense,
            response=response,
        )

    def _agent_response(
        self,
        allowed: bool,
        content: str,
    ) -> str:

        if not allowed:
            return "REQUEST_BLOCKED"

        return f"AGENT_RESPONSE: {content}"
