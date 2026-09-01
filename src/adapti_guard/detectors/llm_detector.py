"""LLM-based moderation detector — NOT IMPLEMENTED."""

from src.adapti_guard.core.models import DetectionResult
from src.adapti_guard.detectors.regex_detector import Detector


class LLMDetector(Detector):
    def detect(self, text: str) -> DetectionResult:
        raise NotImplementedError(
            "LLMDetector is not implemented. Use RegexDetector or mark experiment BLOCKED."
        )

    @property
    def version(self) -> str:
        return "llm_not_implemented"
