import csv
import re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(".")
DET = ROOT / "src/adapti_guard/detector"
OUT = ROOT / "experiments"
RUNS = OUT / "runs"
REGISTRY = OUT / "registry.csv"
HISTORY = OUT / "experiment_history.md"

OUT.mkdir(exist_ok=True)
RUNS.mkdir(exist_ok=True)

# ------------------------------------------------------------
# Recover versions ONLY from filenames.
# Do not infer version from comments inside files.
# ------------------------------------------------------------

version_files = {}

# Current implementation is the latest source state.
current = DET / "prompt_injection_detector.py"
if current.exists():
    version_files[17] = [str(current)]

for path in sorted(DET.glob("prompt_injection_detector.py.v*")):
    m = re.search(r"\.v(\d+)(?:_|$)", path.name)
    if not m:
        continue

    version = int(m.group(1))
    version_files.setdefault(version, []).append(str(path))

# ------------------------------------------------------------
# Known verified experiment result
# ------------------------------------------------------------

known_results = {
    16: {
        "dataset": "NotInject",
        "split": "smoke",
        "samples": 1000,
        "tp": 306,
        "tn": 510,
        "fp": 64,
        "fn": 120,
        "precision": 0.8270,
        "recall": 0.7183,
        "f1": 0.7688,
        "balanced_accuracy": 0.8034,
        "fpr": 0.1115,
        "fnr": 0.2817,
        "change": "Behavioral signal patch",
        "status": "VERIFIED"
    }
}

# ------------------------------------------------------------
# Build complete history V1 -> V17
# ------------------------------------------------------------

rows = []

for version in range(1, 18):

    files = version_files.get(version, [])
    result = known_results.get(version, {})

    if version in known_results:
        status = result["status"]
    elif files:
        status = "HISTORICAL_ARTIFACT"
    else:
        status = "UNRECOVERED"

    change = result.get("change", "")

    if not change and files:
        # Keep this deliberately conservative.
        change = "Historical detector version; change not reconstructed"

    rows.append([
        f"EXP-{version:03d}",
        datetime.now(timezone.utc).isoformat(),
        f"V{version}",
        "detector",
        change,
        result.get("dataset", ""),
        result.get("split", ""),
        result.get("samples", ""),
        result.get("tp", ""),
        result.get("tn", ""),
        result.get("fp", ""),
        result.get("fn", ""),
        result.get("precision", ""),
        result.get("recall", ""),
        result.get("f1", ""),
        result.get("balanced_accuracy", ""),
        result.get("fpr", ""),
        result.get("fnr", ""),
        status,
        " | ".join(files),
    ])

    run_dir = RUNS / f"EXP-{version:03d}_V{version}"
    run_dir.mkdir(exist_ok=True)

    config = {
        "experiment_id": f"EXP-{version:03d}",
        "version": f"V{version}",
        "status": status,
        "component": "detector",
        "change": change,
        "source_files": files,
        "verified_metrics": result
    }

    (run_dir / "config.json").write_text(
        __import__("json").dumps(
            config,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

# ------------------------------------------------------------
# Registry
# ------------------------------------------------------------

with open(REGISTRY, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "experiment_id",
        "date",
        "version",
        "component",
        "change",
        "dataset",
        "split",
        "samples",
        "tp",
        "tn",
        "fp",
        "fn",
        "precision",
        "recall",
        "f1",
        "balanced_accuracy",
        "fpr",
        "fnr",
        "status",
        "source_files"
    ])

    writer.writerows(rows)

# ------------------------------------------------------------
# Markdown history
# ------------------------------------------------------------

lines = [
    "# ADAPTI-GUARD Experiment History",
    "",
    f"Generated: {datetime.now(timezone.utc).isoformat()}",
    "",
    "Historical versions are reconstructed only from available project artifacts.",
    "Unknown results are intentionally not fabricated.",
    ""
]

for version in range(1, 18):

    files = version_files.get(version, [])
    result = known_results.get(version, {})

    if version in known_results:
        status = "VERIFIED"
    elif files:
        status = "HISTORICAL_ARTIFACT"
    else:
        status = "UNRECOVERED"

    lines.append(f"## V{version}")
    lines.append("")
    lines.append(f"**Status:** `{status}`")
    lines.append("")

    if result:
        lines.extend([
            "**Verified result:**",
            "",
            f"- Dataset: {result['dataset']}",
            f"- Split: {result['split']}",
            f"- Samples: {result['samples']}",
            f"- TP: {result['tp']}",
            f"- TN: {result['tn']}",
            f"- FP: {result['fp']}",
            f"- FN: {result['fn']}",
            f"- Precision: {result['precision']}",
            f"- Recall: {result['recall']}",
            f"- F1: {result['f1']}",
            f"- Balanced Accuracy: {result['balanced_accuracy']}",
            f"- FPR: {result['fpr']}",
            f"- FNR: {result['fnr']}",
            ""
        ])

    if files:
        lines.append("**Artifact files:**")
        lines.append("")
        for file in files:
            lines.append(f"- `{file}`")
        lines.append("")

    if not result and not files:
        lines.append(
            "No recoverable artifact/result is currently available."
        )
        lines.append("")

HISTORY.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print("=" * 80)
print("CORRECTED EXPERIMENT HISTORY")
print("=" * 80)

for version in range(1, 18):
    files = version_files.get(version, [])

    if version in known_results:
        status = "VERIFIED"
    elif files:
        status = "HISTORICAL_ARTIFACT"
    else:
        status = "UNRECOVERED"

    print(f"V{version:<2} -> {status}")

print()
print(f"Registry: {REGISTRY}")
print(f"History:  {HISTORY}")
