"""ADAPTI-GUARD adaptive defense baseline."""

from __future__ import annotations

from src.adapti_guard.baselines.regex_baseline import RegexDefenseBaseline
from src.adapti_guard.evaluation.real_llm_pipeline import RealLLMEvaluationPipeline


class AdaptiGuardBaseline:
    name = "adapti_guard"
    implemented = True

    def __init__(self, target_model, judge, *, defense_level: int = 1):
        self.pipeline = RealLLMEvaluationPipeline(
            target_model, judge, defense_level=defense_level
        )

    def run_sample(self, **kwargs):
        return self.pipeline.run_sample(
            sample_id=kwargs["sample_id"],
            prompt=kwargs["prompt"],
            label=kwargs["label"],
            category=kwargs.get("category", "unknown"),
            attack_type=kwargs.get("attack_type", kwargs.get("category", "unknown")),
        )
