#!/usr/bin/env python3
"""EXP004 — Adaptive controller comparison (Fixed L0/L3, Rule, Bayesian)."""

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

EXPERIMENT_ID = "EXP004"
EPISODES = int(__import__("os").getenv("EXP004_EPISODES", "100"))
SEEDS = list(range(5))
STREAM_PATH = ROOT / "results" / "common_attack_stream.json"


def run_controller(seed: int, mode: PolicyMode) -> dict[str, float]:
    runner = HarmonizedRunner.from_stream_path(STREAM_PATH, episodes=EPISODES)
    result = runner.run_method(mode)
    summary = summarize_method(result)
    return {
        "asr": summary.get("asr", 0.0),
        "utility": summary.get("utility", 0.0),
        "defense_cost": summary.get("defense_cost", 0.0),
        "reward": summary.get("reward", 0.0),
    }


def main() -> int:
    out = ROOT / "results" / "EXP004_adaptive_controller"
    out.mkdir(parents=True, exist_ok=True)

    modes = {
        "fixed_l0": PolicyMode.FIXED_L0,
        "fixed_l3": PolicyMode.FIXED_L3,
        "rule_adaptive": PolicyMode.FULL_ADAPTIVE,
        "bayesian_adaptive": PolicyMode.FULL_ADAPTIVE,  # harmonized uses policy engine; Bayesian tested separately
    }

    # Also test BayesianRiskController via direct simulation
    from src.adapti_guard.controllers.adaptive_controller import BayesianRiskController, RuleBasedController
    from src.adapti_guard.adaptation.feedback_engine import FeedbackSignal
    from src.adapti_guard.adaptation.policy_update_engine import PolicyState

    controller_results: dict[str, dict] = {}
    for name, mode in modes.items():
        if name == "bayesian_adaptive":
            continue
        report = run_multiseed(lambda s: run_controller(s, mode), seeds=SEEDS)
        controller_results[name] = report.to_dict()

    # Bayesian controller unit trajectory (5 seeds simulated attack feedback)
    bayesian_reports = []
    for seed in SEEDS:
        ctrl = BayesianRiskController()
        state = PolicyState(defense_level=0)
        attacks = [True, False, True, False, True]
        for atk in attacks:
            fb = FeedbackSignal(
                reward=-1.0 if atk else 0.5,
                security_feedback=-1.0 if atk else 0.5,
                utility_feedback=0.0,
                cost_penalty=0.1,
                adaptation_signal="INCREASE_DEFENSE" if atk else "HOLD",
                attack_success=atk,
                legitimate_success=not atk,
            )
            state = ctrl.step(fb, state)
        bayesian_reports.append({"seed": seed, "final_level": state.defense_level})

    controller_results["bayesian_adaptive"] = {
        "per_seed": bayesian_reports,
        "mean_final_level": sum(r["final_level"] for r in bayesian_reports) / len(bayesian_reports),
        "evaluation_mode": "LEGACY_SIMULATION_ONLY",
    }

    payload = {
        "status": "DONE",
        "evaluation_mode": "LEGACY_SIMULATION_ONLY",
        "note": "Harmonized runner uses simulated ASR (attack_outcome.py). Real judge validation pending EXP002.",
        "controllers": controller_results,
        "git_commit": git_commit(),
        "episodes": EPISODES,
        "seeds": SEEDS,
    }

    (out / "metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (out / "config.json").write_text(json.dumps({
        "experiment": EXPERIMENT_ID,
        "episodes": EPISODES,
        "seeds": SEEDS,
        "modes": list(modes.keys()),
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


if __name__ == "__main__":
    raise SystemExit(main())
