"""No-defense baseline — passthrough to target LLM."""

from __future__ import annotations

from dataclasses import dataclass

from src.adapti_guard.core.models import DefenseAction
from src.adapti_guard.evaluation.llm_judge import JudgeInput, JudgeVerdict, LLMJudge
from src.adapti_guard.evaluation.target_model import GenerationRequest, TargetModel


@dataclass
class BaselineResult:
    sample_id: str
    blocked: bool
    target_response: str
    judge_verdict: JudgeVerdict | None
    latency_ms: float
    defense_action: str = "ALLOW"
    error: str | None = None


class NoDefenseBaseline:
    name = "no_defense"
    implemented = True

    def __init__(self, target_model: TargetModel, judge: LLMJudge):
        self.target_model = target_model
        self.judge = judge

    def run_sample(
        self,
        *,
        sample_id: str,
        prompt: str,
        label: int,
        category: str,
        attack_type: str = "unknown",
        system_prompt: str = "You are a helpful assistant.",
    ) -> BaselineResult:
        gen = self.target_model.generate(
            GenerationRequest(prompt=prompt, system_prompt=system_prompt)
        )
        if gen.error:
            verdict = JudgeVerdict(
                attack_success=False,
                refusal=False,
                harmful_compliance=False,
                utility_success=False,
                confidence=0.0,
                reason="target_api_error",
                parse_error=gen.error,
            )
            return BaselineResult(
                sample_id=sample_id,
                blocked=False,
                target_response="",
                judge_verdict=verdict,
                latency_ms=gen.latency_ms,
                error=gen.error,
            )

        verdict = self.judge.judge(
            JudgeInput(
                attack_prompt=prompt,
                target_response=gen.text,
                attack_category=category,
                attack_type=attack_type,
                is_benign=label == 0,
            )
        )
        return BaselineResult(
            sample_id=sample_id,
            blocked=False,
            target_response=gen.text,
            judge_verdict=verdict,
            latency_ms=gen.latency_ms + verdict.latency_ms,
        )
