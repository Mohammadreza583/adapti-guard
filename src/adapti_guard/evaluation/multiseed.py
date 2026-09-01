"""Multi-seed experiment runner with mean/std/CI aggregation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np

from src.adapti_guard.evaluation.statistics import bootstrap_ci


@dataclass
class SeedResult:
    seed: int
    metrics: dict[str, float]
    status: str = "DONE"


@dataclass
class MultiSeedReport:
    seeds: list[int]
    per_seed: list[SeedResult] = field(default_factory=list)
    aggregated: dict[str, Any] = field(default_factory=dict)
    status: str = "DONE"

    def to_dict(self) -> dict[str, Any]:
        return {
            "seeds": self.seeds,
            "per_seed": [{"seed": r.seed, "metrics": r.metrics, "status": r.status} for r in self.per_seed],
            "aggregated": self.aggregated,
            "status": self.status,
        }


def run_multiseed(
    fn: Callable[[int], dict[str, float]],
    *,
    seeds: list[int] | None = None,
    min_seeds: int = 5,
) -> MultiSeedReport:
    """
    Run experiment function across seeds and aggregate mean, std, 95% CI.
    """
    seed_list = seeds or list(range(min_seeds))
    per_seed: list[SeedResult] = []
    metric_keys: set[str] = set()

    for seed in seed_list:
        try:
            metrics = fn(seed)
            per_seed.append(SeedResult(seed=seed, metrics=metrics))
            metric_keys.update(metrics.keys())
        except Exception as exc:
            per_seed.append(SeedResult(seed=seed, metrics={}, status=f"ERROR: {exc}"))

    aggregated: dict[str, Any] = {}
    for key in sorted(metric_keys):
        values = [r.metrics[key] for r in per_seed if key in r.metrics]
        if not values:
            continue
        arr = np.asarray(values, dtype=float)
        point, low, high = bootstrap_ci(arr, n_bootstrap=2000, seed=42)
        aggregated[key] = {
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
            "ci_95_lower": low,
            "ci_95_upper": high,
            "n_seeds": len(values),
        }

    return MultiSeedReport(seeds=seed_list, per_seed=per_seed, aggregated=aggregated)
