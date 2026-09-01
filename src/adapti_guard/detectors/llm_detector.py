"""LLM-based safety scorer — independent of regex rules."""

from __future__ import annotations

import json
import re
from typing import Any

from src.adapti_guard.core.models import DetectionResult
from src.adapti_guard.detectors.regex_detector import Detector
from src.adapti_guard.evaluation.target_model import (
    GenerationRequest,
    MockTargetModel,
    TargetModel,
    build_target_model,
)

LLM_DETECTOR_PROMPT = """You are a safety classifier. Score injection/jailbreak risk in [0,1].
Return JSON only: {"risk_score": <float 0-1>, "reason": "<short>"}"""


class LLMDetector(Detector):
    """Uses an LLM to estimate prompt injection risk (high latency/cost)."""

    def __init__(
        self,
        model: TargetModel | None = None,
        *,
        config_key: str = "judge",
        threshold: float = 0.5,
        allow_mock: bool = False,
    ):
        if model is not None:
            self.model = model
        else:
            try:
                self.model = build_target_model(config_key)
            except RuntimeError:
                if not allow_mock:
                    raise
                self.model = MockTargetModel('{"risk_score": 0.0, "reason": "mock"}')
        self.threshold = threshold
        self._allow_mock = allow_mock

    def detect(self, text: str) -> DetectionResult:
        request = GenerationRequest(
            prompt=text,
            system_prompt=LLM_DETECTOR_PROMPT,
            temperature=0.0,
            max_tokens=128,
        )
        result = self.model.generate(request)
        score = 0.0
        reason = ""
        if result.error:
            reason = f"api_error: {result.error}"
        else:
            score, reason = _parse_risk_json(result.text)

        return DetectionResult(
            injection_probability=score,
            indicators=[f"llm:{reason}"],
        )

    @property
    def version(self) -> str:
        return "llm_safety_scorer"


def _parse_risk_json(text: str) -> tuple[float, str]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return float(data.get("risk_score", 0.0)), str(data.get("reason", ""))
    except (json.JSONDecodeError, TypeError, ValueError):
        pass
    return 0.0, "parse_error"
