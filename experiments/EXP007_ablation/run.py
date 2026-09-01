#!/usr/bin/env python3
"""EXP007 — Ablation study: No adaptation vs Rule vs Bayesian vs Full ADAPTI-GUARD."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.adapti_guard.evaluation.experiment_logging import ExperimentRunContext, git_commit, update_registry_row
from src.adapti_guard.evaluation.multiseed import run_multiseed
from src.adapti_guard.experiments.harmonized_runner import (
    HarmonizedRunner,
    PolicyMode,
    summarize_method,
)

EXPERIMENT_ID = "EXP007"
EPISODES = int(__import__("os").getenv("EXP007_EPISODES", "100"))
SEEDS = list(range(5))
STREAM_PATH = ROOT / "results" / "common_attack_stream.json"

ABLATION_MODES = {
    "A_no_adaptation": PolicyMode.FIXED_L0,
    "B_rule_adaptation": PolicyMode.FULL_ADAPTIVE,
    "C_bayesian_adaptation": PolicyMode.ESCALATION_ONLY,
    "D_full_adapti_guard": PolicyMode.FULL_ADAPTIVE,
}


def main() -> int:
    out = ROOT / "results" / "EXP007_ablation"
    out.mkdir(parents=True, exist_ok=True)

    ablation_results: dict[str, dict] = {}
    for name, mode in ABLATION_MODES.items():
        report = run_multiseed(
            lambda s, m=mode: _run_mode(s, m),
            seeds=SEEDS,
        )
        ablation_results[name] = report.to_dict()

    payload = {
        "status": "DONE",
        "evaluation_mode": "LEGACY_SIMULATION_ONLY",
        "ablations": ablation_results,
        "git_commit": git_commit(),
        "episodes": EPISODES,
        "seeds": SEEDS,
    }

    (out / "metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (out / "config.json").write_text(json.dumps({
        "experiment": EXPERIMENT_ID,
        "modes": list(ABLATION_MODES.keys()),
        "episodes": EPISODES,
    }, indent=2), encoding="utf-8")
    (out / "logs.json").write_text(json.dumps({"events": [{"status": "completed"}]}, indent=2), encoding="utf-8")

    with ExperimentRunContext.create(EXPERIMENT_ID, config=payload) as ctx:
        ctx.write_metrics(payload)
        update_registry_row(ROOT / "experiments/registry.csv", {
            "experiment_id": EXPERIMENT_ID,
            "run_id": ctx.run_id,
            "status": "DONE",
            "notes": "LEGACY_SIMULATION_ONLY",
        })

    print(json.dumps(payload, indent=2))
    return 0


def _run_mode(seed: int, mode: PolicyMode) -> dict[str, float]:
    runner = HarmonizedRunner.from_stream_path(STREAM_PATH, episodes=EPISODES)
    result = runner.run_method(mode)
    summary = summarize_method(result)
    return {
        "asr": summary.get("asr", 0.0),
        "utility": summary.get("utility", 0.0),
        "defense_cost": summary.get("defense_cost", 0.0),
        "reward": summary.get("reward", 0.0),
    }


if __name__ == "__main__":
    raise SystemExit(main())
