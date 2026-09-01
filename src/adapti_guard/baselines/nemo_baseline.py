"""NeMo Guardrails baseline — requires NeMo installation."""

from __future__ import annotations

from src.adapti_guard.baselines.no_defense import BaselineResult
from src.adapti_guard.evaluation.llm_judge import JudgeVerdict


class NeMoGuardrailsBaseline:
    name = "nemo_guardrails"
    implemented = False

    def __init__(self, *args, **kwargs):
        self._nemo_available = self._check_nemo()

    def _check_nemo(self) -> bool:
        try:
            import nemoguardrails  # noqa: F401

            return True
        except ImportError:
            return False

    def run_sample(self, **kwargs) -> BaselineResult:
        if not self._nemo_available:
            return BaselineResult(
                sample_id=kwargs["sample_id"],
                blocked=False,
                target_response="",
                judge_verdict=JudgeVerdict(
                    attack_success=False,
                    refusal=False,
                    harmful_compliance=False,
                    utility_success=False,
                    confidence=0.0,
                    reason="nemo_not_installed",
                ),
                latency_ms=0.0,
                error="NeMo Guardrails not installed",
            )
        raise NotImplementedError("NeMo Guardrails integration pending full config")
