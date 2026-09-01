"""Detector package — pluggable detection backends."""

from src.adapti_guard.detectors.regex_detector import Detector, RegexDetector

__all__ = ["Detector", "RegexDetector"]
