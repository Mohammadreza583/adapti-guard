"""Baseline defense implementations for fair comparison."""

from src.adapti_guard.baselines.adapti_guard_baseline import AdaptiGuardBaseline
from src.adapti_guard.baselines.comparison_framework import BaselineType, BASELINE_REGISTRY
from src.adapti_guard.baselines.no_defense import NoDefenseBaseline
from src.adapti_guard.baselines.regex_baseline import RegexDefenseBaseline

__all__ = [
    "BaselineType",
    "BASELINE_REGISTRY",
    "NoDefenseBaseline",
    "RegexDefenseBaseline",
    "AdaptiGuardBaseline",
]
