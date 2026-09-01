#!/usr/bin/env python3
"""Create stub result folders for EXP003-EXP008 (NOT_RUN until executed)."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
EXPS = [
    "EXP003_baseline_comparison",
    "EXP004_adaptive_controller",
    "EXP005_rag_security",
    "EXP006_agent_security",
    "EXP007_ablation",
    "EXP008_latency_cost",
]

for exp in EXPS:
    d = ROOT / "results" / exp
    d.mkdir(parents=True, exist_ok=True)
    (d / "config.json").write_text(json.dumps({"experiment": exp, "status": "NOT_RUN"}, indent=2) + "\n")
    (d / "metrics.json").write_text(json.dumps({"status": "NOT_RUN"}, indent=2) + "\n")
    (d / "README.md").write_text(f"# {exp}\n\nStatus: NOT_RUN\n", encoding="utf-8")

print("Created NOT_RUN stubs for EXP003-EXP008")
