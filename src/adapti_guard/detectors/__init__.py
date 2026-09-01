"""Detector package — pluggable detection backends."""

from src.adapti_guard.detectors.hybrid_detector import HybridDetector, HybridWeights
from src.adapti_guard.detectors.llm_detector import LLMDetector
from src.adapti_guard.detectors.ml_detector import MLDetector, train_ml_detector_from_benchmark
from src.adapti_guard.detectors.regex_detector import Detector, RegexDetector

__all__ = [
    "Detector",
    "RegexDetector",
    "MLDetector",
    "LLMDetector",
    "HybridDetector",
    "HybridWeights",
    "train_ml_detector_from_benchmark",
]
