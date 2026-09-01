#!/usr/bin/env python3
"""EXP001 — Dataset analysis for benchmark_v3."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.adapti_guard.evaluation.experiment_logging import ExperimentRunContext, update_registry_row

EXPERIMENT_ID = "EXP001"


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts/build_benchmark_v3.py")], check=True)
    stats_path = ROOT / "datasets/benchmark_v3/statistics.json"
    stats = json.loads(stats_path.read_text(encoding="utf-8"))

    status = "DONE" if stats.get("publication_ready") else "PARTIAL"

    with ExperimentRunContext.create(EXPERIMENT_ID, config={"experiment": "dataset_analysis"}) as ctx:
        ctx.write_metrics({"status": status, **stats})
        ctx.write_dataset_manifest(stats)
        ctx.write_summary(f"# EXP001 Dataset Analysis\n\nStatus: **{status}**\n")
        update_registry_row(
            ROOT / "experiments/registry.csv",
            {
                "experiment_id": EXPERIMENT_ID,
                "run_id": ctx.run_id,
                "status": status,
                "dataset": "benchmark_v3",
                "n_samples": str(stats.get("total", 0)),
                "run_dir": str(ctx.run_dir),
            },
        )

    # Also write experiment folder layout per spec
    out = ROOT / "results/EXP001_dataset_analysis"
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps({"status": status, **stats}, indent=2), encoding="utf-8")
    (out / "config.json").write_text(json.dumps({"experiment": EXPERIMENT_ID}, indent=2), encoding="utf-8")
    (out / "README.md").write_text(f"# EXP001\n\nStatus: {status}\n", encoding="utf-8")

    print(json.dumps({"status": status, "total": stats.get("total")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
