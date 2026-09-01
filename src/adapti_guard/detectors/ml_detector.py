"""ML classifier detector — NOT IMPLEMENTED."""

from src.adapti_guard.core.models import DetectionResult
from src.adapti_guard.detectors.regex_detector import Detector


class MLDetector(Detector):
    def detect(self, text: str) -> DetectionResult:
        raise NotImplementedError(
            "MLDetector is not implemented. Use RegexDetector or mark experiment BLOCKED."
        )

    @property
    def version(self) -> str:
        return "ml_not_implemented"
