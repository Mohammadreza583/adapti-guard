"""Meta Prompt Guard heuristic baseline."""

from __future__ import annotations

import re

from src.adapti_guard.baselines.no_defense import BaselineResult, NoDefenseBaseline
from src.adapti_guard.evaluation.llm_judge import JudgeVerdict

PROMPT_GUARD_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"system\s+override",
    r"you\s+are\s+now\s+dan",
    r"jailbreak",
    r"disregard\s+(all\s+)?rules",
]


class PromptGuardBaseline(NoDefenseBaseline):
    name = "prompt_guard"
    implemented = True

    def __init__(self, target_model, judge, *, threshold: int = 1):
        super().__init__(target_model, judge)
        self.patterns = [re.compile(p, re.IGNORECASE) for p in PROMPT_GUARD_PATTERNS]
        self.threshold = threshold

    def run_sample(self, **kwargs) -> BaselineResult:
        prompt = kwargs["prompt"]
        hits = sum(1 for p in self.patterns if p.search(prompt))
        if hits >= self.threshold:
            return BaselineResult(
                sample_id=kwargs["sample_id"],
                blocked=True,
                target_response="",
                judge_verdict=JudgeVerdict(
                    attack_success=False,
                    refusal=True,
                    harmful_compliance=False,
                    utility_success=False,
                    confidence=0.85,
                    reason="prompt_guard_blocked",
                ),
                latency_ms=0.0,
                defense_action="BLOCK",
            )
        return super().run_sample(**kwargs)
