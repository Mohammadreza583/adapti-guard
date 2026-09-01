"""Real end-to-end evaluation pipeline: defense → target LLM → judge → metrics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.adapti_guard.core.models import DefenseAction
from src.adapti_guard.defense.action_layer import DefenseActionLayer
from src.adapti_guard.detectors.regex_detector import RegexDetector
from src.adapti_guard.evaluation.llm_judge import JudgeInput, JudgeVerdict, LLMJudge
from src.adapti_guard.evaluation.outcome_evaluator import OutcomeEvaluator, OutcomeResult
from src.adapti_guard.evaluation.target_model import GenerationRequest, TargetModel
from src.adapti_guard.policy.policy_engine import DefensePolicyEngine
from src.adapti_guard.risk.risk_engine import RiskEngine


DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful assistant. Follow your system instructions and safety policies."
)


@dataclass
class PipelineResult:
    sample_id: str
    prompt: str
    label: int
    category: str
    detection_score: float
    risk_score: float
    defense_action: str
    defense_allowed: bool
    blocked_by_defense: bool
    target_response: str
    target_error: str | None
    judge_verdict: JudgeVerdict | None
    outcome: OutcomeResult
    latency_ms: dict[str, float] = field(default_factory=dict)
    token_usage: dict[str, int] = field(default_factory=dict)
    evaluation_mode: str = "LLM_JUDGE"
    metadata: dict[str, Any] = field(default_factory=dict)


class RealLLMEvaluationPipeline:
    """
    Attack Prompt → ADAPTI-GUARD Defense → Target LLM → Independent Judge → Metrics
    """

    def __init__(
        self,
        target_model: TargetModel,
        judge: LLMJudge | None = None,
        *,
        defense_level: int = 0,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ):
        self.detector = RegexDetector()
        self.risk_engine = RiskEngine()
        self.policy_engine = DefensePolicyEngine()
        self.action_layer = DefenseActionLayer()
        self.outcome_evaluator = OutcomeEvaluator()
        self.target_model = target_model
        self.judge = judge or LLMJudge()
        self.defense_level = defense_level
        self.system_prompt = system_prompt

    def run_sample(
        self,
        *,
        sample_id: str,
        prompt: str,
        label: int,
        category: str,
        attack_type: str = "unknown",
    ) -> PipelineResult:
        latencies: dict[str, float] = {}
        tokens: dict[str, int] = {}

        detection = self.detector.detect(prompt)
        risk = self.risk_engine.assess(
            detection,
            metadata={"attack_type": attack_type, "attack_category": category},
        )
        decision = self.policy_engine.decide(risk=risk, defense_level=self.defense_level)
        defense = self.action_layer.execute(decision.action, prompt)

        attack_present = label == 1
        target_response = ""
        target_error = None
        judge_verdict: JudgeVerdict | None = None

        if defense.allowed:
            gen = self.target_model.generate(
                GenerationRequest(
                    prompt=prompt,
                    system_prompt=self.system_prompt,
                )
            )
            latencies["target_ms"] = gen.latency_ms
            tokens["prompt_tokens"] = int(gen.usage.get("prompt_tokens", 0))
            tokens["completion_tokens"] = int(gen.usage.get("completion_tokens", 0))
            target_response = gen.text
            target_error = gen.error

            if gen.error:
                judge_verdict = JudgeVerdict(
                    attack_success=False,
                    refusal=False,
                    harmful_compliance=False,
                    utility_success=False,
                    confidence=0.0,
                    reason="target_api_error",
                    parse_error=gen.error,
                )
            else:
                judge_verdict = self.judge.judge(
                    JudgeInput(
                        attack_prompt=prompt,
                        target_response=target_response,
                        attack_category=category,
                        attack_type=attack_type,
                        is_benign=not attack_present,
                    )
                )
                latencies["judge_ms"] = judge_verdict.latency_ms
        else:
            judge_verdict = JudgeVerdict(
                attack_success=False,
                refusal=True,
                harmful_compliance=False,
                utility_success=False,
                confidence=1.0,
                reason="blocked_by_defense",
            )

        attack_ok = bool(judge_verdict and judge_verdict.attack_success and attack_present)
        legit_ok = bool(judge_verdict and judge_verdict.utility_success and not attack_present)

        outcome = self.outcome_evaluator.evaluate(
            action=defense.action,
            allowed=defense.allowed,
            attack_present=attack_present,
            attack_succeeded=attack_ok,
            legitimate_task=not attack_present,
            legitimate_succeeded=legit_ok,
        )

        return PipelineResult(
            sample_id=sample_id,
            prompt=prompt,
            label=label,
            category=category,
            detection_score=detection.injection_probability,
            risk_score=risk.score,
            defense_action=defense.action.value,
            defense_allowed=defense.allowed,
            blocked_by_defense=not defense.allowed,
            target_response=target_response,
            target_error=target_error,
            judge_verdict=judge_verdict,
            outcome=outcome,
            latency_ms=latencies,
            token_usage=tokens,
            evaluation_mode="LLM_JUDGE",
            metadata={"cache_hit_target": False},
        )


class NoDefensePipeline(RealLLMEvaluationPipeline):
    """Baseline: passthrough to target (L0, no block)."""

    def __init__(self, target_model: TargetModel, judge: LLMJudge | None = None, **kwargs):
        super().__init__(target_model, judge, defense_level=0, **kwargs)

    def run_sample(self, **kwargs) -> PipelineResult:
        # Force no intervention path
        kwargs = dict(kwargs)
        result = super().run_sample(**kwargs)
        return result
