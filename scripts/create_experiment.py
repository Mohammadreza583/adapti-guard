import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

if len(sys.argv) < 4:
    print(
        "Usage: python scripts/create_experiment.py "
        "<experiment_id> <version> <component> [change]"
    )
    raise SystemExit(1)

experiment_id = sys.argv[1]
version = sys.argv[2]
component = sys.argv[3]
change = sys.argv[4] if len(sys.argv) > 4 else ""

root = Path("experiments")
run_dir = root / "runs" / f"{experiment_id}_{version}"

if run_dir.exists():
    raise SystemExit(f"ERROR: {run_dir} already exists")

run_dir.mkdir(parents=True)

now = datetime.now(timezone.utc).isoformat()

config = {
    "experiment_id": experiment_id,
    "version": version,
    "date": now,
    "component": component,
    "change": change,
    "dataset": {
        "name": None,
        "path": None,
        "split": None,
        "samples": None,
        "sha256": None
    },
    "model": {
        "type": None,
        "name": None
    },
    "evaluation": {
        "threshold": None,
        "metrics": []
    },
    "reproducibility": {
        "seed": None
    }
}

metrics = {
    "experiment_id": experiment_id,
    "version": version,
    "status": "pending",
    "tp": None,
    "tn": None,
    "fp": None,
    "fn": None,
    "precision": None,
    "recall": None,
    "f1": None,
    "macro_f1": None,
    "balanced_accuracy": None,
    "fpr": None,
    "fnr": None,
    "asr": None,
    "defense_rate": None,
    "utility": None,
    "latency_ms": None
}

notes = f"""# {experiment_id} — {version}

## Objective

## Problem

## Hypothesis

## Change
{change}

## Dataset

## Configuration

## Results

## Comparison

## Decision

## Next Action
"""

for name, obj in [
    ("config.json", config),
    ("metrics.json", metrics),
]:
    with open(run_dir / name, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

(run_dir / "notes.md").write_text(notes, encoding="utf-8")
(run_dir / "stdout.log").touch()
(run_dir / "errors.json").write_text("[]\n", encoding="utf-8")

registry = root / "registry.csv"

with open(registry, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        experiment_id,
        now,
        version,
        component,
        change,
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "created",
        ""
    ])

print("=" * 70)
print("EXPERIMENT CREATED")
print("=" * 70)
print(f"ID:       {experiment_id}")
print(f"Version:  {version}")
print(f"Path:     {run_dir}")
print("=" * 70)
