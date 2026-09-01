#!/usr/bin/env python3
"""EXP003 — Baseline comparison with shared dataset, target, and judge."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv()

from src.adapti_guard.baselines.comparison_runner import run_comparison
from src.adapti_guard.evaluation.experiment_logging import ExperimentRunContext, update_registry_row

EXPERIMENT_ID = "EXP003"
MAX_SAMPLES = int(os.getenv("EXP003_MAX_SAMPLES", "5"))


def main() -> int:
    out = ROOT / "results" / "EXP003_baseline_comparison"
    out.mkdir(parents=True, exist_ok=True)
    benchmark = ROOT / "datasets" / "benchmark_v4"
    csv_path = ROOT / "results" / "baseline_comparison.csv"

    result = run_comparison(
        benchmark_dir=benchmark,
        output_csv=csv_path,
        max_samples=MAX_SAMPLES,
        experiment_id=EXPERIMENT_ID,
    )

    (out / "metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (out / "config.json").write_text(json.dumps({
        "experiment": EXPERIMENT_ID,
        "max_samples": MAX_SAMPLES,
        "benchmark": str(benchmark),
        "output_csv": str(csv_path),
    }, indent=2), encoding="utf-8")

    status = result.get("status", "BLOCKED")
    with ExperimentRunContext.create(EXPERIMENT_ID, config=result) as ctx:
        ctx.write_metrics(result)
        update_registry_row(ROOT / "experiments/registry.csv", {
            "experiment_id": EXPERIMENT_ID,
            "run_id": ctx.run_id,
            "status": status,
        })

    print(json.dumps(result, indent=2))
    return 0 if status == "DONE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
