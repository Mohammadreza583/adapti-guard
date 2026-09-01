"""Regex-only defense baseline."""

from __future__ import annotations

from src.adapti_guard.baselines.no_defense import BaselineResult, NoDefenseBaseline
from src.adapti_guard.defense.action_layer import DefenseActionLayer
from src.adapti_guard.detectors.regex_detector import RegexDetector
from src.adapti_guard.evaluation.llm_judge import JudgeInput, JudgeVerdict
from src.adapti_guard.evaluation.target_model import GenerationRequest
from src.adapti_guard.policy.policy_engine import DefensePolicyEngine
from src.adapti_guard.risk.risk_engine import RiskEngine


class RegexDefenseBaseline(NoDefenseBaseline):
    name = "regex_defense"
    implemented = True

    def __init__(self, target_model, judge, *, defense_level: int = 2):
        super().__init__(target_model, judge)
        self.detector = RegexDetector()
        self.risk_engine = RiskEngine()
        self.policy_engine = DefensePolicyEngine()
        self.action_layer = DefenseActionLayer()
        self.defense_level = defense_level

    def run_sample(self, **kwargs) -> BaselineResult:
        prompt = kwargs["prompt"]
        label = kwargs["label"]
        category = kwargs.get("category", "unknown")
        attack_type = kwargs.get("attack_type", category)
        sample_id = kwargs["sample_id"]
        system_prompt = kwargs.get("system_prompt", "You are a helpful assistant.")

        detection = self.detector.detect(prompt)
        risk = self.risk_engine.assess(
            detection, metadata={"attack_type": attack_type, "attack_category": category}
        )
        decision = self.policy_engine.decide(risk=risk, defense_level=self.defense_level)
        defense = self.action_layer.execute(decision.action, prompt)

        if not defense.allowed:
            verdict = JudgeVerdict(
                attack_success=False,
                refusal=True,
                harmful_compliance=False,
                utility_success=False,
                confidence=1.0,
                reason="blocked_by_regex_defense",
            )
            return BaselineResult(
                sample_id=sample_id,
                blocked=True,
                target_response="",
                judge_verdict=verdict,
                latency_ms=0.0,
                defense_action=defense.action.value,
            )

        return super().run_sample(
            sample_id=sample_id,
            prompt=prompt,
            label=label,
            category=category,
            attack_type=attack_type,
            system_prompt=system_prompt,
        )
