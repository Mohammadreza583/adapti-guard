"""
Phase 8A statistical helpers.

95% CI uses the Student-t critical value for n=5 (df=4):

    mean ± t_(0.975, 4) * std / sqrt(n)

where std is the sample standard deviation (ddof=1).
"""

from __future__ import annotations

import math
from typing import Iterable, Sequence

# Two-sided 95% critical value, df = 4 (n = 5).
# Source: Student-t table; t_{0.975, 4} ≈ 2.7764451051977925
T_CRIT_95_DF4 = 2.7764451051977925

PRIMARY_METRICS = (
    "asr",
    "defense_rate",
    "utility",
    "defense_cost",
    "reward",
    "security_score",
)


def sample_mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("mean undefined for empty sample")
    return sum(values) / len(values)


def sample_std(values: Sequence[float]) -> float:
    """Sample standard deviation with ddof=1."""

    n = len(values)
    if n < 2:
        return 0.0
    mu = sample_mean(values)
    var = sum((x - mu) ** 2 for x in values) / (n - 1)
    std = math.sqrt(var)
    # Collapse pure floating-point noise; not real stochastic variance.
    if std < 1e-12:
        return 0.0
    return std


def ci95_t(values: Sequence[float]) -> tuple[float, float, float, float]:
    """
    Return (mean, std, ci_low, ci_high) using t-based 95% CI.

    For n != 5 the critical value is still looked up only for df=4
    because Phase 8A fixes n=5. Other n raises ValueError.
    """

    n = len(values)
    if n != 5:
        raise ValueError(
            f"Phase 8A CI requires n=5 seeds, got n={n}"
        )

    mu = sample_mean(values)
    std = sample_std(values)
    half = T_CRIT_95_DF4 * (std / math.sqrt(n))
    return mu, std, mu - half, mu + half


def aggregate_metric(values: Iterable[float]) -> dict[str, float | int]:
    vals = [float(v) for v in values]
    mu, std, lo, hi = ci95_t(vals)
    return {
        "mean": mu,
        "std": std,
        "ci95_low": lo,
        "ci95_high": hi,
        "n": len(vals),
    }
