"""Statistical validation helpers."""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np


def bootstrap_ci(
    values: Sequence[float],
    *,
    n_bootstrap: int = 5000,
    ci: float = 0.95,
    seed: int = 42,
    stat: Callable[[np.ndarray], float] = np.mean,
) -> tuple[float, float, float]:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return 0.0, 0.0, 0.0
    point = float(stat(arr))
    rng = np.random.default_rng(seed)
    boots = [float(stat(rng.choice(arr, size=arr.size, replace=True))) for _ in range(n_bootstrap)]
    alpha = (1.0 - ci) / 2.0
    lower, upper = np.quantile(boots, [alpha, 1.0 - alpha])
    return point, float(lower), float(upper)


def mcnemar_test(a_success: Sequence[bool], b_success: Sequence[bool]) -> dict[str, float | int | str]:
    if len(a_success) != len(b_success):
        raise ValueError("paired sequences must have equal length")
    b01 = sum(1 for x, y in zip(a_success, b_success) if (not x) and y)
    b10 = sum(1 for x, y in zip(a_success, b_success) if x and (not y))
    from scipy import stats

    if b01 + b10 == 0:
        return {"b01": b01, "b10": b10, "statistic": 0.0, "p_value": 1.0, "method": "mcnemar_exact"}
    result = stats.binomtest(b01, n=b01 + b10, p=0.5, alternative="two-sided")
    return {
        "b01": b01,
        "b10": b10,
        "statistic": float(result.statistic),
        "p_value": float(result.pvalue),
        "method": "mcnemar_exact",
    }


def wilcoxon_signed_rank(a: Sequence[float], b: Sequence[float]) -> dict[str, float | str]:
    from scipy import stats

    diff = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    if diff.size == 0:
        return {"statistic": 0.0, "p_value": 1.0, "method": "wilcoxon"}
    if np.allclose(diff, 0):
        return {"statistic": 0.0, "p_value": 1.0, "method": "wilcoxon"}
    stat = stats.wilcoxon(diff, alternative="two-sided")
    return {"statistic": float(stat.statistic), "p_value": float(stat.pvalue), "method": "wilcoxon"}


def cohens_h(p1: float, p2: float) -> float:
    """Effect size for difference in proportions."""
    from math import asin, sqrt

    return 2 * (asin(sqrt(p1)) - asin(sqrt(p2)))
