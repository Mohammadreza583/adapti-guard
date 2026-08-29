"""
Phase 8C — Robustness, statistical comparison, and Security–Utility–Cost.

Does not modify Phase 7 / 8A / 8B artifacts or metric formulas.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.adapti_guard.experiments.experiment_runner import ExperimentRunner
from src.adapti_guard.experiments.phase7_schedule import (
    PHASE7_ATTACK_STREAM_NAME,
    PHASE7_ATTACK_STREAM_SLICE,
    PHASE7_EPISODE_SCHEDULE,
    PHASE7_EPISODES,
    validate_phase7_schedule,
)
from src.adapti_guard.experiments.phase8_multiseed import (
    METHOD_LEVEL,
    PHASE8_METHODS,
    load_phase7_stream_slice,
    metrics_from_episodes,
    run_fixed_with_outcomes,
    _stabilize_metrics,
)
from src.adapti_guard.experiments.phase8_stats import (
    sample_mean,
    sample_std,
)
from src.adapti_guard.experiments.seed_control import set_global_seed


DETECTION_THRESHOLD = 0.25
PHASE8C_VERSION = "phase8c_v1"
SCENARIOS = ("known", "novel", "evolving")
METHODS = PHASE8_METHODS


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _provenance(**extra: Any) -> dict[str, Any]:
    base = {
        "version": PHASE8C_VERSION,
        "experiment": "phase8c",
        "protocol": "phase7_v2_75_25",
        "episode_count": PHASE7_EPISODES,
        "schedule": "phase7_v2_75_25",
        "metric_version": "phase8_primary_v1",
        "configuration": {
            "methods": list(METHODS),
            "scenarios": list(SCENARIOS),
            "detection_threshold": DETECTION_THRESHOLD,
        },
        "timestamp_utc": _now(),
    }
    base.update(extra)
    return base


def _episode_detection_rate(episodes) -> float:
    attacks = [e for e in episodes if e.attack_present]
    if not attacks:
        return 0.0
    detected = sum(
        1
        for e in attacks
        if float(e.detection_score) >= DETECTION_THRESHOLD
    )
    return detected / len(attacks)


def _full_metrics(episodes) -> dict[str, float]:
    base = metrics_from_episodes(episodes)
    base["detection_rate"] = _stabilize_metrics(
        {"detection_rate": _episode_detection_rate(episodes)}
    )["detection_rate"]
    return base


def _metrics_from_fixed_outcomes(outcomes, schedule) -> dict[str, float]:
    from src.adapti_guard.experiments.phase8_multiseed import (
        metrics_from_baseline_outcomes,
    )

    base = metrics_from_baseline_outcomes(outcomes, schedule)
    # Baseline outcomes lack detection_score; recompute via detector path
    # is already done inside run_fixed — attach detection by re-detecting
    # is expensive. Fixed path below returns detection via custom runner.
    return base


def run_method_on_stream(
    method: str,
    stream_slice: list[dict],
    schedule: list[bool],
    seed: int = 1,
) -> dict[str, Any]:
    set_global_seed(seed)

    if method == "adaptive":
        runner = ExperimentRunner(
            attack_stream=stream_slice,
            episode_schedule=schedule,
        )
        episodes = runner.run(len(schedule))
        metrics = _full_metrics(episodes)
        episode_rows = [
            {
                "episode_id": e.episode_id,
                "attack_present": e.attack_present,
                "attack_family": e.attack_family,
                "attack_success": e.attack_success,
                "legitimate_success": e.legitimate_success,
                "detection_score": e.detection_score,
                "defense_level": e.defense_level,
                "defense_cost": e.defense_cost,
                "reward": e.reward,
                "security_score": e.security_score,
                "utility_score": e.utility_score,
            }
            for e in episodes
        ]
        return {"metrics": metrics, "episodes": episode_rows}

    # Fixed levels: reuse harness then attach detection_rate by scanning
    # payloads through the same detector used in the baseline loop.
    from src.adapti_guard.baselines.baseline_runner import BaselineRunner
    from src.adapti_guard.core.models import DefenseAction
    from src.adapti_guard.adaptation.feedback_engine import FeedbackEngine

    level = METHOD_LEVEL[method]
    runner = BaselineRunner(episode_schedule=schedule)
    fixed_actions = {
        0: DefenseAction.NO_INTERVENTION,
        1: DefenseAction.SANITIZE,
        2: DefenseAction.TOOL_RESTRICTION,
        3: DefenseAction.BLOCK,
    }
    action = fixed_actions[level]
    outcomes = []
    detections = []
    attack_index = 0
    episode_rows = []

    for episode_id in range(1, len(schedule) + 1):
        legitimate = schedule[episode_id - 1]
        if legitimate:
            payload = runner._benign_payload(episode_id)
            family = "legitimate"
        else:
            attack = stream_slice[attack_index]
            attack_index += 1
            payload = attack["payload"]
            family = attack["attack_family"]

        detection = runner.detector.detect(payload)
        detections.append(detection)
        runner.risk_engine.assess(
            detection, contextual_risk=0.5, historical_attack=0.0
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
        feedback = FeedbackEngine().generate(outcome)
        episode_rows.append(
            {
                "episode_id": episode_id,
                "attack_present": not legitimate,
                "attack_family": family,
                "attack_success": outcome.attack_success,
                "legitimate_success": outcome.legitimate_success,
                "detection_score": detection.score,
                "defense_level": level,
                "defense_cost": outcome.defense_cost,
                "reward": feedback.reward,
                "security_score": outcome.security_score,
                "utility_score": outcome.utility_score,
            }
        )

    class _E:
        pass

    objs = []
    for row in episode_rows:
        o = _E()
        o.__dict__.update(row)
        objs.append(o)
    metrics = _full_metrics(objs)
    return {"metrics": metrics, "episodes": episode_rows}


def load_scenario_stream(scenario: str) -> list[dict]:
    if scenario == "known":
        return load_phase7_stream_slice()
    if scenario == "novel":
        doc = json.loads(
            Path("results/phase8/novel_attack_set_v1.json").read_text(
                encoding="utf-8"
            )
        )
        return doc["attacks"]
    if scenario == "evolving":
        doc = json.loads(
            Path("results/phase8/evolving_attack_stream_v1.json").read_text(
                encoding="utf-8"
            )
        )
        return doc["attacks"]
    raise ValueError(f"Unknown scenario: {scenario}")


def evaluate_robustness(seed: int = 1) -> dict[str, Any]:
    schedule = validate_phase7_schedule(PHASE7_EPISODE_SCHEDULE)
    results = []

    for scenario in SCENARIOS:
        stream = load_scenario_stream(scenario)
        if len(stream) != 75:
            raise ValueError(
                f"{scenario} stream must have 75 attacks, got {len(stream)}"
            )
        for method in METHODS:
            run = run_method_on_stream(method, stream, schedule, seed=seed)
            m = run["metrics"]
            results.append(
                {
                    "scenario": scenario,
                    "method": method,
                    "seed": seed,
                    "episodes": int(m["episodes"]),
                    "attack_count": int(m["attack_count"]),
                    "legitimate_count": int(m["legitimate_count"]),
                    "metrics": {
                        "asr": m["asr"],
                        "detection_rate": m["detection_rate"],
                        "defense_rate": m["defense_rate"],
                        "utility": m["utility"],
                        "defense_cost": m["defense_cost"],
                        "reward": m["reward"],
                    },
                    "episodes_detail": run["episodes"],
                }
            )

    # Evolving stage breakdown (adaptive method, attack slots only)
    evolving_doc = json.loads(
        Path("results/phase8/evolving_attack_stream_v1.json").read_text(
            encoding="utf-8"
        )
    )
    adaptive_evolving = next(
        r
        for r in results
        if r["scenario"] == "evolving" and r["method"] == "adaptive"
    )
    stage_rows = []
    attack_eps = [
        e for e in adaptive_evolving["episodes_detail"] if e["attack_present"]
    ]
    for stage_meta, (start, end) in zip(
        evolving_doc["stages"],
        ((0, 19), (19, 38), (38, 57), (57, 75)),
    ):
        subset = attack_eps[start:end]
        class _E:
            pass
        objs = []
        for row in subset:
            o = _E()
            # treat as attack-only population for stage ASR/detection
            o.__dict__.update(row)
            objs.append(o)
        # Stage metrics on attack-only subset: utility vacuous (0) by definition
        metrics = _full_metrics(objs)
        stage_rows.append(
            {
                "stage": stage_meta["name"],
                "attack_slot_start": start,
                "attack_slot_end": end - 1,
                "attack_count": len(subset),
                "metrics": {
                    "asr": metrics["asr"],
                    "detection_rate": metrics["detection_rate"],
                    "defense_rate": metrics["defense_rate"],
                    "utility": metrics["utility"],
                    "defense_cost": metrics["defense_cost"],
                    "reward": metrics["reward"],
                },
                "mean_defense_level": sample_mean(
                    [float(e["defense_level"]) for e in subset]
                )
                if subset
                else 0.0,
            }
        )

    levels = [s["mean_defense_level"] for s in stage_rows]
    defense_changes = any(
        abs(a - b) > 1e-12 for a, b in zip(levels, levels[1:])
    )

    return {
        **_provenance(
            source_artifacts=[
                "results/common_attack_stream.json",
                "results/phase8/novel_attack_set_v1.json",
                "results/phase8/evolving_attack_stream_v1.json",
                "results/phase7/phase7_schedule.json",
            ],
            seed=seed,
            attack_protocol="75_attack_25_legitimate_shared_schedule",
            attack_set_version={
                "known": PHASE7_ATTACK_STREAM_NAME,
                "novel": "novel_attack_set_v1",
                "evolving": "evolving_attack_stream_v1",
            },
        ),
        "results": [
            {k: v for k, v in row.items() if k != "episodes_detail"}
            for row in results
        ],
        "episode_level": {
            f"{row['scenario']}::{row['method']}": row["episodes_detail"]
            for row in results
        },
        "evolving_stages_adaptive": stage_rows,
        "evolving_defense_level_changes_across_stages": defense_changes,
        "novelty_claim": {
            "status": "LIMITED",
            "reason": (
                "Novel set is structurally/lexically separated from the "
                "frozen MVP known set, but remains closed-world synthetic "
                "prompt-injection templates in the same four families."
            ),
            "attack_success_heuristic_limitation": (
                "MVP attack_success for SANITIZE is defined via residual "
                "known malicious markers. Novel marker-free payloads can "
                "therefore be labeled unsuccessful after SANITIZE even when "
                "detection_score=0. Fixed-L0 (no sanitize) still shows "
                "ASR=1.0 on novel, confirming population fairness while "
                "limiting claims about sanitize generalization."
            ),
        },
    }


def _holm_adjust(pvalues: list[float]) -> list[float]:
    """Holm–Bonferroni adjusted p-values."""
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    adjusted = [0.0] * m
    running = 0.0
    for rank, idx in enumerate(order):
        factor = m - rank
        val = min(1.0, pvalues[idx] * factor)
        running = max(running, val)
        adjusted[idx] = running
    return adjusted


def _wilson_sign_test(diff: list[float]) -> dict[str, Any]:
    """
    Exact two-sided sign test on paired episode-level differences.

    H0: P(diff>0) = P(diff<0). Zeros are dropped.
    Returns exact binomial two-sided p-value.
    """
    nonzero = [d for d in diff if d != 0]
    n = len(nonzero)
    if n == 0:
        return {
            "test": "sign_test",
            "n_nonzero": 0,
            "p_value": 1.0,
            "interpretation": "no nonzero paired differences",
        }
    plus = sum(1 for d in nonzero if d > 0)
    # two-sided exact binomial under p=0.5
    # p = 2 * sum_{k=0}^{min(plus,n-plus)} C(n,k) / 2^n  for the smaller tail,
    # more carefully: 2 * P(X <= k) where k = min(plus, n-plus)
    k = min(plus, n - plus)

    def comb(nn: int, kk: int) -> int:
        return math.comb(nn, kk)

    tail = sum(comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    p = min(1.0, 2.0 * tail)
    return {
        "test": "exact_sign_test",
        "n_nonzero": n,
        "n_positive": plus,
        "n_negative": n - plus,
        "p_value": p,
        "effect_size_sign_ratio": (plus / n) if n else None,
        "interpretation": (
            "paired episode-level sign test on metric differences; "
            "valid under exchangeability of signs under H0"
        ),
    }


def run_statistical_comparison(
    robustness: dict[str, Any],
) -> dict[str, Any]:
    """
    Statistical comparisons with explicit sample definitions.

    Seed variance: use Phase 8A multi-seed summary (known protocol only).
    Episode-level variance: paired sign tests across methods on shared
    episode IDs within a scenario (attack episodes only for ASR proxy
    via attack_success; utility via legitimate episodes).
    """

    multiseed = json.loads(
        Path("results/phase8/multiseed_summary.json").read_text(encoding="utf-8")
    )
    raw = json.loads(
        Path("results/phase8/multiseed_raw.json").read_text(encoding="utf-8")
    )

    seed_variance = {
        "definition": (
            "Cross-seed variance of aggregate run metrics under the frozen "
            "known protocol (Phase 8A)."
        ),
        "observation": multiseed.get("determinism"),
        "implication": (
            "All methods have std≈0 across seeds 1–5; inferential tests on "
            "seed means are not informative (no seed-level variance)."
        ),
        "by_method_metric": multiseed.get("summary"),
    }

    # Episode-level paired comparisons on known scenario:
    # Adaptive vs Fixed-L0 / L3 for attack_success (security) and reward.
    comparisons = []
    episode_map = robustness["episode_level"]

    def paired_metric(scenario: str, method_a: str, method_b: str, field: str, population: str):
        a = episode_map[f"{scenario}::{method_a}"]
        b = episode_map[f"{scenario}::{method_b}"]
        if population == "attack":
            a_rows = [e for e in a if e["attack_present"]]
            b_rows = [e for e in b if e["attack_present"]]
        elif population == "legitimate":
            a_rows = [e for e in a if not e["attack_present"]]
            b_rows = [e for e in b if not e["attack_present"]]
        else:
            a_rows, b_rows = a, b
        if len(a_rows) != len(b_rows):
            raise ValueError("Unequal paired populations")
        # align by episode_id
        b_by_id = {e["episode_id"]: e for e in b_rows}
        diffs = []
        for ea in a_rows:
            eb = b_by_id[ea["episode_id"]]
            va = float(ea[field]) if not isinstance(ea[field], bool) else float(ea[field])
            vb = float(eb[field]) if not isinstance(eb[field], bool) else float(eb[field])
            diffs.append(va - vb)
        return diffs

    planned = [
        ("known", "adaptive", "fixed_level_0", "attack_success", "attack", "security_proxy_lower_better"),
        ("known", "adaptive", "fixed_level_3", "attack_success", "attack", "security_proxy_lower_better"),
        ("known", "adaptive", "fixed_level_0", "reward", "all", "reward_higher_better"),
        ("novel", "adaptive", "fixed_level_0", "attack_success", "attack", "security_proxy_lower_better"),
        ("evolving", "adaptive", "fixed_level_0", "attack_success", "attack", "security_proxy_lower_better"),
    ]

    raw_tests = []
    for scenario, ma, mb, field, population, note in planned:
        if population == "all":
            a = episode_map[f"{scenario}::{ma}"]
            b = episode_map[f"{scenario}::{mb}"]
            b_by_id = {e["episode_id"]: e for e in b}
            diffs = [
                float(e[field]) - float(b_by_id[e["episode_id"]][field])
                for e in a
            ]
        else:
            diffs = paired_metric(scenario, ma, mb, field, population)
        test = _wilson_sign_test(diffs)
        mean_diff = sample_mean(diffs) if diffs else 0.0
        raw_tests.append(
            {
                "comparison": f"{ma} vs {mb}",
                "scenario": scenario,
                "metric": field,
                "test": test["test"],
                "sample_definition": (
                    f"paired episode-level differences on {population} "
                    f"episodes; n_pairs={len(diffs)}; same schedule/stream "
                    f"within scenario={scenario}"
                ),
                "effect_size_mean_diff": mean_diff,
                "effect_size_sign_ratio": test.get("effect_size_sign_ratio"),
                "p_value": test["p_value"],
                "n_nonzero": test.get("n_nonzero"),
                "direction_note": note,
                "interpretation_pre_correction": test["interpretation"],
            }
        )

    adjusted = _holm_adjust([t["p_value"] for t in raw_tests])
    for t, p_adj in zip(raw_tests, adjusted):
        t["p_value_holm"] = p_adj
        t["significant_holm_0.05"] = p_adj < 0.05
        if sample_std(
            [
                float(x)
                for x in ([0.0] if t["n_nonzero"] == 0 else [1.0])
            ]
        ) or True:
            # interpretation after correction
            if t["n_nonzero"] == 0:
                t["interpretation"] = (
                    "No episode-level differences; methods identical on this "
                    "metric/population — do not claim significance."
                )
            elif t["significant_holm_0.05"]:
                t["interpretation"] = (
                    "Holm-adjusted p < 0.05: paired episode-level difference "
                    "survives multiple-comparison correction."
                )
            else:
                t["interpretation"] = (
                    "Not significant after Holm correction (or weak evidence)."
                )

    scenario_variance = []
    for method in METHODS:
        asrs = []
        for scenario in SCENARIOS:
            row = next(
                r
                for r in robustness["results"]
                if r["method"] == method and r["scenario"] == scenario
            )
            asrs.append(row["metrics"]["asr"])
        scenario_variance.append(
            {
                "method": method,
                "metric": "asr",
                "values_by_scenario": dict(zip(SCENARIOS, asrs)),
                "std_across_scenarios": sample_std(asrs),
                "definition": (
                    "Scenario-level dispersion of aggregate ASR across "
                    "known/novel/evolving under identical schedule."
                ),
            }
        )

    return {
        **_provenance(
            source_artifacts=[
                "results/phase8/multiseed_raw.json",
                "results/phase8/multiseed_summary.json",
                "results/phase8/robustness_v1.json",
            ],
            seed="phase8a_seeds_1to5 + phase8c_seed_1_episode_pairs",
            attack_protocol="mixed: known from 8A; novel/evolving from 8C",
            attack_set_version={
                "known": PHASE7_ATTACK_STREAM_NAME,
                "novel": "novel_attack_set_v1",
                "evolving": "evolving_attack_stream_v1",
            },
            multiple_comparison_correction="Holm-Bonferroni",
        ),
        "seed_variance": seed_variance,
        "episode_level_tests": raw_tests,
        "scenario_level_variance": scenario_variance,
        "limitations": [
            "Seed-level t-tests between methods are not used because Phase 8A "
            "seed variance is zero under the deterministic controlled stack.",
            "Episode-level sign tests require paired shared episode IDs within "
            "a scenario; they are not applied across incompatible populations.",
            "Boolean attack_success differences yield discrete paired signs; "
            "effect sizes are reported as mean diff and sign ratio.",
        ],
    }


def dominates(a: dict[str, float], b: dict[str, float]) -> bool:
    """
    Pareto dominance for (security, utility, cost):
      lower ASR better, higher Utility better, lower Cost better.
    a dominates b if a is <=ASR, >=Utility, <=Cost, and strict in one.
    """
    better_or_eq = (
        a["asr"] <= b["asr"]
        and a["utility"] >= b["utility"]
        and a["defense_cost"] <= b["defense_cost"]
    )
    strict = (
        a["asr"] < b["asr"]
        or a["utility"] > b["utility"]
        or a["defense_cost"] < b["defense_cost"]
    )
    return better_or_eq and strict


def run_security_utility_cost(
    robustness: dict[str, Any],
) -> dict[str, Any]:
    # Focus primary SUC table on known scenario (Phase 7 protocol),
    # and include novel/evolving as robustness context.
    tables = {}
    for scenario in SCENARIOS:
        rows = []
        for method in METHODS:
            r = next(
                x
                for x in robustness["results"]
                if x["scenario"] == scenario and x["method"] == method
            )
            rows.append(
                {
                    "method": method,
                    "asr": r["metrics"]["asr"],
                    "defense_rate": r["metrics"]["defense_rate"],
                    "utility": r["metrics"]["utility"],
                    "defense_cost": r["metrics"]["defense_cost"],
                    "reward": r["metrics"]["reward"],
                }
            )
        # Pareto on ASR/Utility/Cost
        nondominated = []
        dominated = []
        for i, a in enumerate(rows):
            if any(
                dominates(rows[j], a) for j in range(len(rows)) if j != i
            ):
                dominated.append(a["method"])
            else:
                nondominated.append(a["method"])
        tables[scenario] = {
            "methods": rows,
            "pareto_nondominated": nondominated,
            "pareto_dominated": dominated,
        }

    known = tables["known"]["methods"]
    observations = {
        "security_improvements": (
            "Relative to Fixed-L0 (ASR=1.0), higher fixed levels and "
            "Adaptive reduce ASR on the known protocol."
        ),
        "utility_preservation": (
            "Fixed-L0/L1/L2 and Adaptive preserve utility=1.0 on known; "
            "Fixed-L3 collapses utility to 0 via blanket BLOCK."
        ),
        "cost_increases": (
            "Mean defense_cost rises with fixed level; Adaptive sits "
            "between L2 and L3 on known."
        ),
        "cost_efficient_note": (
            "Pareto nondominated methods are those not worse on all of "
            "ASR↓, Utility↑, Cost↓. No single-metric superiority claim."
        ),
    }

    return {
        **_provenance(
            source_artifacts=[
                "results/phase8/robustness_v1.json",
                "results/phase8/multiseed_summary.json",
            ],
            seed=1,
            attack_protocol="phase7_v2_75_25 per scenario",
            attack_set_version={
                "known": PHASE7_ATTACK_STREAM_NAME,
                "novel": "novel_attack_set_v1",
                "evolving": "evolving_attack_stream_v1",
            },
        ),
        "objectives": {
            "security": "lower ASR / higher Defense Rate",
            "utility": "higher Utility",
            "cost": "lower Defense Cost",
            "composite_score": None,
        },
        "by_scenario": tables,
        "observations": observations,
        "known_reference_from_phase8a": {
            "note": "Phase 8A known-protocol aggregates (deterministic).",
            "rows": [
                {
                    "method": r["method"],
                    "metric": r["metric"],
                    "mean": r["mean"],
                    "std": r["std"],
                }
                for r in json.loads(
                    Path("results/phase8/multiseed_summary.json").read_text(
                        encoding="utf-8"
                    )
                )["summary"]
                if r["metric"] in {"asr", "utility", "defense_cost", "reward"}
            ],
        },
    }


def _safe_write(path: Path, payload: dict) -> None:
    if path.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path.replace(path.with_name(f"{path.stem}_prev_{stamp}{path.suffix}"))
    # Drop bulky episode_level from robustness file written to disk? Keep it
    # for stats but maybe strip for size — user asked for robustness_v1.json
    # with provenance; episode_level is needed for statistical validity.
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_phase8c() -> dict[str, Path]:
    from src.adapti_guard.experiments.phase8c_attack_sets import (
        save_attack_sets,
    )

    set_paths = save_attack_sets()
    robustness = evaluate_robustness(seed=1)
    stats = run_statistical_comparison(robustness)
    suc = run_security_utility_cost(robustness)

    out = Path("results/phase8")
    paths = {
        "novel": set_paths["novel"],
        "evolving": set_paths["evolving"],
        "robustness": out / "robustness_v1.json",
        "statistical": out / "statistical_comparison_v1.json",
        "suc": out / "security_utility_cost_v1.json",
    }
    _safe_write(paths["robustness"], robustness)
    _safe_write(paths["statistical"], stats)
    _safe_write(paths["suc"], suc)
    return paths
