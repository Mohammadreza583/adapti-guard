"""Hybrid detector: Final Risk = Regex + ML + LLM (weighted sum, normalized)."""

from __future__ import annotations

from dataclasses import dataclass

from src.adapti_guard.core.models import DetectionResult
from src.adapti_guard.detectors.llm_detector import LLMDetector
from src.adapti_guard.detectors.ml_detector import MLDetector
from src.adapti_guard.detectors.regex_detector import Detector, RegexDetector


@dataclass
class HybridWeights:
    regex: float = 0.4
    ml: float = 0.35
    llm: float = 0.25

    def normalized(self) -> tuple[float, float, float]:
        total = self.regex + self.ml + self.llm
        if total <= 0:
            return 1.0, 0.0, 0.0
        return self.regex / total, self.ml / total, self.llm / total


class HybridDetector(Detector):
    """
    Combines regex, ML, and optional LLM safety scores:

        Final Risk = w_r * RegexScore + w_m * MLScore + w_l * LLMScore
    """

    def __init__(
        self,
        *,
        regex_detector: Detector | None = None,
        ml_detector: MLDetector | None = None,
        llm_detector: LLMDetector | None = None,
        weights: HybridWeights | None = None,
        use_llm: bool = False,
        threshold: float = 0.5,
    ):
        self.regex_detector = regex_detector or RegexDetector()
        self.ml_detector = ml_detector or MLDetector()
        self.llm_detector = llm_detector
        self.use_llm = use_llm and llm_detector is not None
        self.weights = weights or HybridWeights()
        self.threshold = threshold

    @property
    def version(self) -> str:
        return "hybrid_v1"

    def detect(self, text: str) -> DetectionResult:
        regex_res = self.regex_detector.detect(text)
        ml_res = self.ml_detector.detect(text)
        llm_score = 0.0
        llm_meta: dict = {}
        if self.use_llm and self.llm_detector is not None:
            llm_res = self.llm_detector.detect(text)
            llm_score = llm_res.injection_probability
            llm_meta = llm_res.metadata or {}

        wr, wm, wl = self.weights.normalized()
        if not self.use_llm:
            # Redistribute LLM weight to regex+ML
            wr, wm = wr + wl * 0.6, wm + wl * 0.4
            wl = 0.0

        final_score = (
            wr * regex_res.injection_probability
            + wm * ml_res.injection_probability
            + wl * llm_score
        )
        patterns = list(regex_res.indicators or [])
        return DetectionResult(
            injection_probability=final_score,
            indicators=patterns + [f"hybrid:regex={regex_res.injection_probability:.3f}", f"hybrid:ml={ml_res.injection_probability:.3f}"],
        )
