"""
Phase 8A — Multi-seed evaluation on the frozen Phase 7 protocol.

Uses:
    - PHASE7_EPISODE_SCHEDULE (75 attack / 25 legitimate)
    - first 75 records of results/common_attack_stream.json

Does not modify Phase 7 artifacts.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.adapti_guard.adaptation.feedback_engine import FeedbackEngine
from src.adapti_guard.baselines.baseline_runner import BaselineRunner
from src.adapti_guard.experiments.experiment_runner import ExperimentRunner
from src.adapti_guard.experiments.phase7_schedule import (
    PHASE7_ATTACK_STREAM_NAME,
    PHASE7_ATTACK_STREAM_SLICE,
    PHASE7_EPISODE_SCHEDULE,
    PHASE7_EPISODES,
    validate_phase7_schedule,
)
from src.adapti_guard.experiments.phase8_stats import (
    PRIMARY_METRICS,
    aggregate_metric,
)
from src.adapti_guard.experiments.seed_control import set_global_seed


PHASE8_SEEDS = (1, 2, 3, 4, 5)

PHASE8_METHODS = (
    "fixed_level_0",
    "fixed_level_1",
    "fixed_level_2",
    "fixed_level_3",
    "adaptive",
)

METHOD_LEVEL = {
    "fixed_level_0": 0,
    "fixed_level_1": 1,
    "fixed_level_2": 2,
    "fixed_level_3": 3,
}


def load_phase7_stream_slice(
    stream_path: str | Path = "results/common_attack_stream.json",
) -> list[dict]:
    path = Path(stream_path)
    stream = json.loads(path.read_text(encoding="utf-8"))
    start, end = PHASE7_ATTACK_STREAM_SLICE
    slice_ = stream[start:end]
    if len(slice_) != 75:
        raise ValueError(
            f"Expected 75 attack-stream records, got {len(slice_)}"
        )
    return slice_


def metrics_from_episodes(episodes) -> dict[str, float]:
    attack = [e for e in episodes if e.attack_present]
    legit = [e for e in episodes if not e.attack_present]

    n_a = len(attack)
    n_l = len(legit)
    attack_successes = sum(1 for e in attack if e.attack_success)
    legit_successes = sum(1 for e in legit if e.legitimate_success)

    asr = attack_successes / n_a if n_a else 0.0
    defense_rate = 1.0 - asr if n_a else 0.0
    utility = legit_successes / n_l if n_l else 0.0
    defense_cost = (
        sum(e.defense_cost for e in episodes) / len(episodes)
        if episodes
        else 0.0
    )
    reward = (
        sum(e.reward for e in episodes) / len(episodes)
        if episodes
        else 0.0
    )
    security_score = (
        sum(e.security_score for e in episodes) / len(episodes)
        if episodes
        else 0.0
    )

    return _stabilize_metrics({
        "asr": asr,
        "defense_rate": defense_rate,
        "utility": utility,
        "defense_cost": defense_cost,
        "reward": reward,
        "security_score": security_score,
        "attack_count": float(n_a),
        "legitimate_count": float(n_l),
        "episodes": float(len(episodes)),
    })


def _stable(value: float) -> float:
    """Round away pure floating-point noise; does not change metric formulas."""
    return float(f"{float(value):.12g}")


def _stabilize_metrics(metrics: dict[str, float]) -> dict[str, float]:
    return {
        k: _stable(v) if isinstance(v, float) else v
        for k, v in metrics.items()
    }


def metrics_from_baseline_outcomes(outcomes, schedule) -> dict[str, float]:
    feedback_engine = FeedbackEngine()

    attack = [
        o
        for i, o in enumerate(outcomes, start=1)
        if not schedule[i - 1]
    ]
    legit = [
        o
        for i, o in enumerate(outcomes, start=1)
        if schedule[i - 1]
    ]

    n_a = len(attack)
    n_l = len(legit)
    attack_successes = sum(1 for o in attack if o.attack_success)
    legit_successes = sum(1 for o in legit if o.legitimate_success)

    asr = attack_successes / n_a if n_a else 0.0
    defense_rate = 1.0 - asr if n_a else 0.0
    utility = legit_successes / n_l if n_l else 0.0
    defense_cost = (
        sum(o.defense_cost for o in outcomes) / len(outcomes)
        if outcomes
        else 0.0
    )
    security_score = (
        sum(o.security_score for o in outcomes) / len(outcomes)
        if outcomes
        else 0.0
    )
    rewards = [feedback_engine.generate(o).reward for o in outcomes]
    reward = sum(rewards) / len(rewards) if rewards else 0.0

    return _stabilize_metrics({
        "asr": asr,
        "defense_rate": defense_rate,
        "utility": utility,
        "defense_cost": defense_cost,
        "reward": reward,
        "security_score": security_score,
        "attack_count": float(n_a),
        "legitimate_count": float(n_l),
        "episodes": float(len(outcomes)),
    })


def run_fixed_with_outcomes(
    method: str,
    defense_level: int,
    schedule: list[bool],
    stream_slice: list[dict],
) -> dict[str, float]:
    """
    Execute a fixed baseline and return primary metrics.

    Reuses BaselineRunner internals via a thin local loop so reward /
    security are available without regenerating Phase 7 artifacts.
    """

    runner = BaselineRunner(episode_schedule=schedule)
    # Collect outcomes by monkey-patching through public run path:
    # BaselineRunner.run_fixed does not return outcomes; mirror its
    # controlled loop here using the same public helpers.
    from src.adapti_guard.core.models import DefenseAction

    fixed_actions = {
        0: DefenseAction.NO_INTERVENTION,
        1: DefenseAction.SANITIZE,
        2: DefenseAction.TOOL_RESTRICTION,
        3: DefenseAction.BLOCK,
    }
    action = fixed_actions[defense_level]
    outcomes = []
    attack_index = 0

    for episode_id in range(1, PHASE7_EPISODES + 1):
        legitimate = runner._legitimate_task(episode_id)
        if legitimate:
            payload = runner._benign_payload(episode_id)
            family = "legitimate"
        else:
            attack = stream_slice[attack_index]
            attack_index += 1
            payload = attack["payload"]
            family = attack["attack_family"]

        detection = runner.detector.detect(payload)
        runner.risk_engine.assess(
            detection,
            contextual_risk=0.5,
            historical_attack=0.0,
        )
        defense = runner.action_layer.execute(action, payload)

        if legitimate:
            attack_ok = False
            legitimate_succeeded = action != DefenseAction.BLOCK
        else:
            attack_ok = runner._attack_success(action, family, defense)
            legitimate_succeeded = False

        outcome = runner.outcome_evaluator.evaluate(
            action=action,
            allowed=defense.allowed,
            attack_present=not legitimate,
            attack_succeeded=attack_ok,
            legitimate_task=legitimate,
            legitimate_succeeded=legitimate_succeeded,
        )
        outcomes.append(outcome)

    return metrics_from_baseline_outcomes(outcomes, schedule)


def run_one(
    method: str,
    seed: int,
    schedule: list[bool] | None = None,
    stream_slice: list[dict] | None = None,
) -> dict[str, Any]:
    schedule = validate_phase7_schedule(schedule or PHASE7_EPISODE_SCHEDULE)
    stream_slice = (
        list(stream_slice)
        if stream_slice is not None
        else load_phase7_stream_slice()
    )

    seed_info = set_global_seed(seed)

    if method == "adaptive":
        runner = ExperimentRunner(
            attack_stream=stream_slice,
            episode_schedule=schedule,
        )
        episodes = runner.run(PHASE7_EPISODES)
        metrics = metrics_from_episodes(episodes)
        attack_payloads = [
            e.payload for e in episodes if e.attack_present
        ]
        attack_families = [
            e.attack_family for e in episodes if e.attack_present
        ]
    elif method in METHOD_LEVEL:
        metrics = run_fixed_with_outcomes(
            method=method,
            defense_level=METHOD_LEVEL[method],
            schedule=schedule,
            stream_slice=stream_slice,
        )
        # Reconstruct sequence for fairness fingerprint.
        attack_payloads = []
        attack_families = []
        attack_index = 0
        for is_legit in schedule:
            if not is_legit:
                attack_payloads.append(stream_slice[attack_index]["payload"])
                attack_families.append(
                    stream_slice[attack_index]["attack_family"]
                )
                attack_index += 1
    else:
        raise ValueError(f"Unsupported method: {method}")

    return {
        "experiment_id": f"phase8a_{method}_seed{seed}",
        "experiment": "phase8a",
        "method": method,
        "seed": seed,
        "seed_provenance": seed_info,
        "episodes": int(metrics["episodes"]),
        "attack_count": int(metrics["attack_count"]),
        "legitimate_count": int(metrics["legitimate_count"]),
        "attack_stream": PHASE7_ATTACK_STREAM_NAME,
        "attack_stream_slice": list(PHASE7_ATTACK_STREAM_SLICE),
        "schedule": "phase7_v2_75_25",
        "metrics": {k: metrics[k] for k in PRIMARY_METRICS},
        "fairness_fingerprint": {
            "attack_payloads_sha_prefix": _fingerprint(attack_payloads),
            "attack_families": attack_families,
        },
    }


def _fingerprint(payloads: list[str]) -> str:
    import hashlib

    h = hashlib.sha256()
    for p in payloads:
        h.update(p.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:16]


def run_matrix(
    seeds: tuple[int, ...] = PHASE8_SEEDS,
    methods: tuple[str, ...] = PHASE8_METHODS,
) -> list[dict[str, Any]]:
    schedule = validate_phase7_schedule(PHASE7_EPISODE_SCHEDULE)
    stream_slice = load_phase7_stream_slice()
    raw: list[dict[str, Any]] = []

    for method in methods:
        for seed in seeds:
            raw.append(
                run_one(
                    method=method,
                    seed=seed,
                    schedule=schedule,
                    stream_slice=stream_slice,
                )
            )
    return raw


def summarize(raw_runs: list[dict[str, Any]]) -> dict[str, Any]:
    by_method: dict[str, list[dict[str, Any]]] = {}
    for row in raw_runs:
        by_method.setdefault(row["method"], []).append(row)

    rows = []
    for method, runs in by_method.items():
        for metric in PRIMARY_METRICS:
            values = [r["metrics"][metric] for r in runs]
            agg = aggregate_metric(values)
            rows.append(
                {
                    "method": method,
                    "metric": metric,
                    **agg,
                }
            )

    # Determinism note
    variance_by_method = {}
    for method, runs in by_method.items():
        stds = []
        for metric in PRIMARY_METRICS:
            values = [r["metrics"][metric] for r in runs]
            stds.append(aggregate_metric(values)["std"])
        variance_by_method[method] = {
            "max_std": max(stds),
            "all_zero_std": all(s == 0.0 for s in stds),
        }

    return {
        "experiment": "phase8a",
        "version": "multiseed_v1",
        "seeds": list(PHASE8_SEEDS),
        "methods": list(PHASE8_METHODS),
        "n_runs": len(raw_runs),
        "statistical_method": {
            "interval": "95% Student-t CI",
            "formula": "mean ± t_(0.975, n-1) * std / sqrt(n)",
            "n": 5,
            "df": 4,
            "t_crit": 2.7764451051977925,
            "std": "sample std (ddof=1)",
        },
        "protocol": {
            "episodes": PHASE7_EPISODES,
            "attack": 75,
            "legitimate": 25,
            "schedule": "phase7_v2_75_25",
            "attack_stream": PHASE7_ATTACK_STREAM_NAME,
            "attack_stream_slice": list(PHASE7_ATTACK_STREAM_SLICE),
        },
        "determinism": {
            "note": (
                "Controlled Phase 7/8A pipeline is deterministic given "
                "frozen stream + schedule; cross-seed std is expected "
                "to be 0 unless stochastic components are introduced."
            ),
            "by_method": variance_by_method,
        },
        "summary": rows,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def save_artifacts(
    raw_runs: list[dict[str, Any]],
    summary: dict[str, Any],
    output_dir: str | Path = "results/phase8",
) -> dict[str, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    raw_path = out / "multiseed_raw.json"
    summary_path = out / "multiseed_summary.json"

    raw_path.write_text(
        json.dumps(raw_runs, indent=2),
        encoding="utf-8",
    )
    summary_path.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    return {"raw": raw_path, "summary": summary_path}
