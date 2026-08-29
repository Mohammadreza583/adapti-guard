#!/usr/bin/env python3
"""
Phase 11 — Manuscript Evidence Package (extraction only).

Read-only over Phase 7–10 artifacts. Writes only:
  results/phase11/manuscript_evidence_package_v1.json

Does not overwrite an existing v1 artifact.
Does not rerun experiments or modify prior-phase artifacts.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(".")
OUT = ROOT / "results/phase11/manuscript_evidence_package_v1.json"

REQUIRED_SOURCES = [
    "results/phase10/claim_evidence_matrix_v1.json",
    "results/phase7/fixed_baselines_100_v2.json",
    "results/phase7/adaptive_100_v2.json",
    "results/phase8/multiseed_raw.json",
    "results/phase8/multiseed_summary.json",
    "results/phase8/ablation_v1.json",
    "results/phase8/temporal_analysis_v1.json",
    "results/phase8/attack_family_analysis_v1.json",
    "results/phase8/novel_attack_set_v1.json",
    "results/phase8/evolving_attack_stream_v1.json",
    "results/phase8/robustness_v1.json",
    "results/phase8/statistical_comparison_v1.json",
    "results/phase8/security_utility_cost_v1.json",
]

METHOD_DISPLAY = {
    "fixed_level_0": "Fixed-L0",
    "fixed_level_1": "Fixed-L1",
    "fixed_level_2": "Fixed-L2",
    "fixed_level_3": "Fixed-L3",
    "adaptive": "Adaptive",
    "adaptive_without_historical": "Adaptive without historical signal",
    "adaptive_with_historical": "Adaptive with historical signal",
}

MAIN_METRICS = ["asr", "defense_rate", "utility", "defense_cost", "reward"]
MAIN_METHODS = [
    "fixed_level_0",
    "fixed_level_1",
    "fixed_level_2",
    "fixed_level_3",
    "adaptive",
]


def _load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _sha(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _cell(raw, *, source_artifact, source_field, method, metric, population):
    if raw is None or raw == "MISSING":
        return {
            "raw_value": "MISSING",
            "source_artifact": source_artifact,
            "source_field": source_field,
            "method": method,
            "metric": metric,
            "population": population,
        }
    return {
        "raw_value": raw,
        "source_artifact": source_artifact,
        "source_field": source_field,
        "method": method,
        "metric": metric,
        "population": population,
    }


def _git_porcelain(*paths: str) -> str:
    r = subprocess.run(
        ["git", "status", "--porcelain", "--", *paths],
        capture_output=True,
        text=True,
        check=False,
    )
    return r.stdout.strip()


def build_main_results(ms: dict) -> dict:
    by = {(r["method"], r["metric"]): r for r in ms["summary"]}
    rows = []
    missing = []
    for method in MAIN_METHODS:
        row = {
            "method": method,
            "display_label": METHOD_DISPLAY[method],
            "metrics": {},
        }
        for metric in MAIN_METRICS:
            key = (method, metric)
            if key not in by:
                missing.append(f"{method}.{metric}")
                row["metrics"][metric] = {
                    "mean": _cell(
                        "MISSING",
                        source_artifact="results/phase8/multiseed_summary.json",
                        source_field=f"summary[{method},{metric}].mean",
                        method=method,
                        metric=metric,
                        population="phase8a_multiseed_seeds_1_5",
                    ),
                    "std": _cell(
                        "MISSING",
                        source_artifact="results/phase8/multiseed_summary.json",
                        source_field=f"summary[{method},{metric}].std",
                        method=method,
                        metric=metric,
                        population="phase8a_multiseed_seeds_1_5",
                    ),
                    "ci95_low": _cell(
                        "MISSING",
                        source_artifact="results/phase8/multiseed_summary.json",
                        source_field=f"summary[{method},{metric}].ci95_low",
                        method=method,
                        metric=metric,
                        population="phase8a_multiseed_seeds_1_5",
                    ),
                    "ci95_high": _cell(
                        "MISSING",
                        source_artifact="results/phase8/multiseed_summary.json",
                        source_field=f"summary[{method},{metric}].ci95_high",
                        method=method,
                        metric=metric,
                        population="phase8a_multiseed_seeds_1_5",
                    ),
                    "n": _cell(
                        "MISSING",
                        source_artifact="results/phase8/multiseed_summary.json",
                        source_field=f"summary[{method},{metric}].n",
                        method=method,
                        metric=metric,
                        population="phase8a_multiseed_seeds_1_5",
                    ),
                }
                continue
            r = by[key]
            pop = "phase8a_multiseed_seeds_1_5"
            art = "results/phase8/multiseed_summary.json"
            row["metrics"][metric] = {
                "mean": _cell(
                    r["mean"],
                    source_artifact=art,
                    source_field=f"summary[{method},{metric}].mean",
                    method=method,
                    metric=metric,
                    population=pop,
                ),
                "std": _cell(
                    r["std"],
                    source_artifact=art,
                    source_field=f"summary[{method},{metric}].std",
                    method=method,
                    metric=metric,
                    population=pop,
                ),
                "ci95_low": _cell(
                    r["ci95_low"],
                    source_artifact=art,
                    source_field=f"summary[{method},{metric}].ci95_low",
                    method=method,
                    metric=metric,
                    population=pop,
                ),
                "ci95_high": _cell(
                    r["ci95_high"],
                    source_artifact=art,
                    source_field=f"summary[{method},{metric}].ci95_high",
                    method=method,
                    metric=metric,
                    population=pop,
                ),
                "n": _cell(
                    r["n"],
                    source_artifact=art,
                    source_field=f"summary[{method},{metric}].n",
                    method=method,
                    metric=metric,
                    population=pop,
                ),
            }
        rows.append(row)
    return {
        "authoritative_source": "results/phase8/multiseed_summary.json",
        "population": "phase8a_multiseed_seeds_1_5",
        "protocol": ms.get("protocol"),
        "statistical_method": ms.get("statistical_method"),
        "determinism_note": (ms.get("determinism") or {}).get("note"),
        "rows": rows,
        "missing_fields": missing,
    }


def build_ablation(ab: dict) -> dict:
    art = "results/phase8/ablation_v1.json"
    pop = "phase7_v2_75_25"
    wanted = [
        "fixed_level_0",
        "fixed_level_1",
        "fixed_level_2",
        "fixed_level_3",
        "adaptive_without_historical",
        "adaptive_with_historical",
    ]
    by = {c["condition"]: c for c in ab["conditions"]}
    rows = []
    missing = []
    for cond in wanted:
        if cond not in by:
            missing.append(cond)
            rows.append(
                {
                    "condition": cond,
                    "display_label": METHOD_DISPLAY.get(cond, cond),
                    "metrics": {m: "MISSING" for m in MAIN_METRICS},
                }
            )
            continue
        c = by[cond]
        metrics = {}
        for m in MAIN_METRICS:
            if m not in c["metrics"]:
                missing.append(f"{cond}.{m}")
                metrics[m] = _cell(
                    "MISSING",
                    source_artifact=art,
                    source_field=f"conditions[{cond}].metrics.{m}",
                    method=cond,
                    metric=m,
                    population=pop,
                )
            else:
                metrics[m] = _cell(
                    c["metrics"][m],
                    source_artifact=art,
                    source_field=f"conditions[{cond}].metrics.{m}",
                    method=cond,
                    metric=m,
                    population=pop,
                )
        rows.append(
            {
                "condition": cond,
                "display_label": METHOD_DISPLAY.get(cond, cond),
                "metrics": metrics,
            }
        )
    return {
        "authoritative_source": art,
        "historical_signal_changed_aggregates": ab["historical_signal_changed_aggregates"],
        "paper_constraint": (
            "Do NOT claim historical signal improves performance "
            "(historical_signal_changed_aggregates=false)."
        ),
        "scientific_note": ab.get("scientific_note"),
        "rows": rows,
        "missing_fields": missing,
    }


def build_temporal(tmp: dict) -> dict:
    art = "results/phase8/temporal_analysis_v1.json"
    pop = "adaptive_phase7_v2_100_episodes"
    wv = tmp["window_validation"]
    covered = wv.get("covered_ids") or []
    validation = {
        "n_windows": wv.get("n_windows"),
        "expected_n_windows": 4,
        "unique_coverage": wv.get("unique_coverage"),
        "no_overlap": wv.get("no_overlap"),
        "covered_episode_count": len(covered),
        "expected_episode_count": 100,
        "episodes_per_window": [
            w.get("episode_count") for w in tmp["windows"]
        ],
        "expected_episodes_per_window": 25,
        "coverage_ok": (
            wv.get("n_windows") == 4
            and wv.get("unique_coverage") is True
            and wv.get("no_overlap") is True
            and len(covered) == 100
            and all(w.get("episode_count") == 25 for w in tmp["windows"])
        ),
    }
    fields = [
        "attack_count",
        "legitimate_count",
        "asr",
        "defense_rate",
        "utility",
        "defense_cost",
        "reward",
        "mean_defense_level",
    ]
    rows = []
    missing = []
    for w in tmp["windows"]:
        label = f"{w['episode_start']}–{w['episode_end']}"
        cells = {}
        for f in fields:
            if f not in w:
                missing.append(f"{label}.{f}")
                cells[f] = _cell(
                    "MISSING",
                    source_artifact=art,
                    source_field=f"windows[{label}].{f}",
                    method="adaptive",
                    metric=f,
                    population=pop,
                )
            else:
                cells[f] = _cell(
                    w[f],
                    source_artifact=art,
                    source_field=f"windows[{label}].{f}",
                    method="adaptive",
                    metric=f,
                    population=pop,
                )
        rows.append(
            {
                "window_label": label,
                "episode_start": w["episode_start"],
                "episode_end": w["episode_end"],
                "episode_count": w["episode_count"],
                "fields": cells,
            }
        )
    return {
        "authoritative_source": art,
        "population": pop,
        "window_validation": validation,
        "rows": rows,
        "missing_fields": missing,
    }


def build_attack_family(fam: dict) -> dict:
    art = "results/phase8/attack_family_analysis_v1.json"
    pop = "adaptive_known_attack_episodes_first75"
    expected = [
        "direct_injection",
        "indirect_injection",
        "context_manipulation",
        "tool_output_injection",
    ]
    by = {f["attack_family"]: f for f in fam["families"]}
    fields = ["attack_count", "asr", "detection_rate", "defense_rate", "utility"]
    rows = []
    missing = []
    for name in expected:
        if name not in by:
            missing.append(name)
            rows.append({"attack_family": name, "fields": {f: "MISSING" for f in fields}})
            continue
        f = by[name]
        cells = {}
        for k in fields:
            if k not in f:
                missing.append(f"{name}.{k}")
                cells[k] = _cell(
                    "MISSING",
                    source_artifact=art,
                    source_field=f"families[{name}].{k}",
                    method="adaptive",
                    metric=k,
                    population=pop,
                )
            else:
                cells[k] = _cell(
                    f[k],
                    source_artifact=art,
                    source_field=f"families[{name}].{k}",
                    method="adaptive",
                    metric=k,
                    population=pop,
                )
        rows.append({"attack_family": name, "fields": cells})
    return {
        "authoritative_source": art,
        "population": pop,
        "family_validation": fam.get("family_validation"),
        "rows": rows,
        "missing_fields": missing,
    }


def build_robustness(rob: dict, p10: dict) -> dict:
    art = "results/phase8/robustness_v1.json"
    metric_keys = [
        "asr",
        "detection_rate",
        "defense_rate",
        "utility",
        "defense_cost",
        "reward",
    ]
    rows = []
    missing = []
    for r in rob["results"]:
        cells = {}
        for m in metric_keys:
            if m not in r["metrics"]:
                missing.append(f"{r['scenario']}.{r['method']}.{m}")
                cells[m] = _cell(
                    "MISSING",
                    source_artifact=art,
                    source_field=f"results[{r['scenario']},{r['method']}].metrics.{m}",
                    method=r["method"],
                    metric=m,
                    population=r["scenario"],
                )
            else:
                cells[m] = _cell(
                    r["metrics"][m],
                    source_artifact=art,
                    source_field=f"results[{r['scenario']},{r['method']}].metrics.{m}",
                    method=r["method"],
                    metric=m,
                    population=r["scenario"],
                )
        rows.append(
            {
                "scenario": r["scenario"],
                "method": r["method"],
                "display_label": METHOD_DISPLAY.get(r["method"], r["method"]),
                "attack_count": r.get("attack_count"),
                "legitimate_count": r.get("legitimate_count"),
                "metrics": cells,
            }
        )
    gen = p10["generalization"]
    return {
        "authoritative_source": art,
        "scenarios": ["known", "novel", "evolving"],
        "evaluated_robustness_vs_generalization": {
            "evaluated_robustness": (
                "Robustness metrics are reported for the evaluated known/novel/evolving "
                "attack sets under the controlled protocol."
            ),
            "generalization_status": gen["status"],
            "allowed_wording": gen["allowed_wording"],
            "disallowed_wording": gen["disallowed_wording"],
            "constraint": "Do not upgrade GENERALIZATION beyond LIMITED.",
        },
        "novelty_claim": rob.get("novelty_claim"),
        "evolving_defense_level_changes_across_stages": rob.get(
            "evolving_defense_level_changes_across_stages"
        ),
        "evolving_stages_adaptive": rob.get("evolving_stages_adaptive"),
        "rows": rows,
        "missing_fields": missing,
    }


def build_suc(suc: dict) -> dict:
    art = "results/phase8/security_utility_cost_v1.json"
    by_scenario = {}
    missing = []
    for scenario, block in suc["by_scenario"].items():
        rows = []
        for m in block["methods"]:
            method = m["method"]
            cells = {}
            for key, metric_name in [
                ("asr", "security_proxy_asr_lower_better"),
                ("utility", "utility"),
                ("defense_cost", "defense_cost"),
                ("reward", "reward"),
                ("defense_rate", "defense_rate"),
            ]:
                if key not in m:
                    missing.append(f"{scenario}.{method}.{key}")
                    cells[key] = _cell(
                        "MISSING",
                        source_artifact=art,
                        source_field=f"by_scenario[{scenario}].methods[{method}].{key}",
                        method=method,
                        metric=metric_name,
                        population=scenario,
                    )
                else:
                    cells[key] = _cell(
                        m[key],
                        source_artifact=art,
                        source_field=f"by_scenario[{scenario}].methods[{method}].{key}",
                        method=method,
                        metric=metric_name,
                        population=scenario,
                    )
            rows.append(
                {
                    "method": method,
                    "display_label": METHOD_DISPLAY.get(method, method),
                    "metrics": cells,
                }
            )
        by_scenario[scenario] = {
            "rows": rows,
            "pareto_nondominated": block.get("pareto_nondominated"),
            "pareto_dominated": block.get("pareto_dominated"),
        }
    return {
        "authoritative_source": art,
        "objectives": suc.get("objectives"),
        "observations": suc.get("observations"),
        "known_reference_from_phase8a": suc.get("known_reference_from_phase8a"),
        "by_scenario": by_scenario,
        "missing_fields": missing,
        "note": (
            "Pareto sets are preserved from the existing artifact; "
            "no new optimization metric introduced."
        ),
    }


def build_stats(stats: dict) -> dict:
    art = "results/phase8/statistical_comparison_v1.json"
    tests = []
    for t in stats["episode_level_tests"]:
        tests.append(
            {
                "comparison": t.get("comparison"),
                "scenario": t.get("scenario"),
                "metric": t.get("metric"),
                "test": t.get("test"),
                "sample_definition": t.get("sample_definition"),
                "effect_size_mean_diff": _cell(
                    t.get("effect_size_mean_diff", "MISSING"),
                    source_artifact=art,
                    source_field="episode_level_tests.effect_size_mean_diff",
                    method=t.get("comparison"),
                    metric=t.get("metric"),
                    population=t.get("scenario"),
                ),
                "effect_size_sign_ratio": _cell(
                    t.get("effect_size_sign_ratio", "MISSING"),
                    source_artifact=art,
                    source_field="episode_level_tests.effect_size_sign_ratio",
                    method=t.get("comparison"),
                    metric=t.get("metric"),
                    population=t.get("scenario"),
                ),
                "p_value": _cell(
                    t.get("p_value", "MISSING"),
                    source_artifact=art,
                    source_field="episode_level_tests.p_value",
                    method=t.get("comparison"),
                    metric=t.get("metric"),
                    population=t.get("scenario"),
                ),
                "p_value_holm": _cell(
                    t.get("p_value_holm", "MISSING"),
                    source_artifact=art,
                    source_field="episode_level_tests.p_value_holm",
                    method=t.get("comparison"),
                    metric=t.get("metric"),
                    population=t.get("scenario"),
                ),
                "significant_holm_0.05": t.get("significant_holm_0.05"),
                "n_nonzero": t.get("n_nonzero"),
                "direction_note": t.get("direction_note"),
                "interpretation": t.get("interpretation"),
            }
        )
    return {
        "authoritative_source": art,
        "multiple_comparison_correction": stats.get("multiple_comparison_correction"),
        "statistical_method_note": (
            "Only already-computed episode-level exact sign tests with Holm-Bonferroni "
            "correction are extracted; no new hypothesis tests performed."
        ),
        "seed_variance": stats.get("seed_variance"),
        "episode_level_tests": tests,
        "scenario_level_variance": stats.get("scenario_level_variance"),
        "limitations": stats.get("limitations"),
    }


def build_claim_map(p10: dict) -> dict:
    # Manuscript table/section destinations for each claim (evidence packaging only).
    table_map = {
        "C1": {
            "tables": ["temporal", "main_results"],
            "figures": ["defense_level_over_episodes (to be generated from Phase 7 adaptive episodes in a later phase)"],
            "primary_artifacts": [
                "results/phase7/adaptive_100_v2.json",
                "results/phase8/temporal_analysis_v1.json",
            ],
        },
        "C2": {
            "tables": ["main_results", "robustness", "statistical_comparison"],
            "figures": [],
            "primary_artifacts": [
                "results/phase8/multiseed_summary.json",
                "results/phase8/robustness_v1.json",
                "results/phase8/statistical_comparison_v1.json",
            ],
        },
        "C3": {
            "tables": ["main_results", "ablation"],
            "figures": [],
            "primary_artifacts": [
                "results/phase8/multiseed_summary.json",
                "results/phase8/ablation_v1.json",
            ],
        },
        "C4": {
            "tables": ["security_utility_cost", "main_results"],
            "figures": ["pareto_frontier_known (optional later phase)"],
            "primary_artifacts": [
                "results/phase8/security_utility_cost_v1.json",
            ],
        },
        "C5": {
            "tables": ["main_results", "security_utility_cost", "statistical_comparison"],
            "figures": [],
            "primary_artifacts": [
                "results/phase8/multiseed_summary.json",
                "results/phase8/security_utility_cost_v1.json",
            ],
        },
        "C6": {
            "tables": ["ablation"],
            "figures": [],
            "primary_artifacts": ["results/phase8/ablation_v1.json"],
        },
        "C7": {
            "tables": ["attack_family"],
            "figures": [],
            "primary_artifacts": [
                "results/phase8/attack_family_analysis_v1.json",
            ],
        },
        "C8": {
            "tables": ["robustness"],
            "figures": [],
            "primary_artifacts": [
                "results/phase8/robustness_v1.json",
                "results/phase8/novel_attack_set_v1.json",
            ],
        },
        "C9": {
            "tables": ["robustness"],
            "figures": ["evolving_stages_adaptive (optional later phase)"],
            "primary_artifacts": [
                "results/phase8/robustness_v1.json",
                "results/phase8/evolving_attack_stream_v1.json",
            ],
        },
        "C10": {
            "tables": ["main_results"],
            "figures": [],
            "primary_artifacts": [
                "results/phase8/multiseed_summary.json",
                "results/phase8/multiseed_raw.json",
            ],
        },
    }
    out = {}
    for c in p10["claims"]:
        cid = c["claim_id"]
        status = c["status"]
        entry = {
            "claim_id": cid,
            "claim_text": c.get("claim_text") or c.get("claim"),
            "status": status,
            "paper_safe_wording": c.get("paper_safe_wording"),
            "paper_handling": c.get("paper_handling"),
            "evidence_locations": table_map[cid],
            "phase10_limitations": c.get("limitations") or [],
        }
        if status == "NOT SUPPORTED":
            entry["manuscript_use"] = "NOT ESTABLISHED"
            entry["supporting_evidence_for_affirmation"] = None
            entry["note"] = (
                "Do not create affirmative supporting evidence. "
                "Ablation null result may be cited only as non-establishment."
            )
            entry["disposition"] = c.get("disposition") or p10.get("c6_disposition")
        elif status == "LIMITED":
            entry["manuscript_use"] = "LIMITED — preserve scope qualifications"
        elif status == "PARTIALLY SUPPORTED":
            entry["manuscript_use"] = "PARTIAL — use qualified wording only"
        else:
            entry["manuscript_use"] = "SUPPORTED — use Phase 10 paper_safe_wording"
        out[cid] = entry
    return out


def build_limitations(p10: dict, stats: dict, rob: dict, ab: dict) -> list:
    # Evidence-based, de-duplicated limitations from Phase 10 + recorded artifact notes.
    items = []
    seen = set()

    def add(text: str, source: str):
        key = text.strip().lower()
        if key in seen:
            return
        seen.add(key)
        items.append({"text": text, "source": source})

    add(
        f"Generalization status is {p10['generalization']['status']}: "
        f"{p10['generalization']['allowed_wording']}. "
        f"Do not claim: {p10['generalization']['disallowed_wording']}.",
        "results/phase10/claim_evidence_matrix_v1.json#generalization",
    )
    add(
        "Controlled pipeline is deterministic given frozen stream/schedule "
        "(multi-seed std=0 demonstrates reproducibility, not stochastic robustness).",
        "results/phase8/multiseed_summary.json#determinism",
    )
    add(
        "Finite seed count n=5 under deterministic protocol.",
        "results/phase8/multiseed_summary.json#statistical_method",
    )
    add(
        "Evaluated attack families are limited to the four frozen families "
        "in the first-75 known stream slice (counts 19/19/19/18).",
        "results/phase8/attack_family_analysis_v1.json",
    )
    add(
        "Model/environment scope is the MVP agent/detector/outcome protocol; "
        "results do not establish open-world LLM-agent security.",
        "results/phase10/claim_evidence_matrix_v1.json",
    )
    add(
        "Historical-signal contribution is not established "
        f"(historical_signal_changed_aggregates="
        f"{ab['historical_signal_changed_aggregates']}).",
        "results/phase8/ablation_v1.json",
    )
    for lim in stats.get("limitations") or []:
        add(lim, "results/phase8/statistical_comparison_v1.json#limitations")
    nc = rob.get("novelty_claim") or {}
    if nc.get("reason"):
        add(nc["reason"], "results/phase8/robustness_v1.json#novelty_claim")
    if nc.get("attack_success_heuristic_limitation"):
        add(
            nc["attack_success_heuristic_limitation"],
            "results/phase8/robustness_v1.json#novelty_claim",
        )
    # Pull unique high-level claim limitations that are package-relevant
    for c in p10["claims"]:
        for L in c.get("limitations") or []:
            # Keep package concise: skip ultra-specific duplicates already covered
            if "null aggregate" in L.lower() or "historical" in L.lower():
                continue
            if "std=0" in L.lower() or "deterministic" in L.lower():
                continue
            if "generalization" in L.lower() and "limited" in L.lower():
                continue
            add(L, f"results/phase10/claim_evidence_matrix_v1.json#{c['claim_id']}")
    return items


def validate_package(pkg: dict, source_hashes_before: dict) -> dict:
    checks = {}

    missing_sources = [p for p in REQUIRED_SOURCES if not Path(p).exists()]
    checks["all_required_source_artifacts_exist"] = len(missing_sources) == 0

    # JSON already parsed if we got here
    checks["json_valid"] = True

    def section_ok(name: str) -> bool:
        sec = pkg.get(name) or {}
        mf = sec.get("missing_fields")
        if mf is None:
            return name in pkg and sec != {}
        return name in pkg and mf == []

    checks["main_results"] = section_ok("main_results") and len(
        pkg["main_results"]["rows"]
    ) == 5
    checks["ablation"] = (
        section_ok("ablation")
        and pkg["ablation"]["historical_signal_changed_aggregates"] is False
        and len(pkg["ablation"]["rows"]) == 6
    )
    checks["temporal"] = (
        section_ok("temporal")
        and pkg["temporal"]["window_validation"]["coverage_ok"] is True
        and len(pkg["temporal"]["rows"]) == 4
    )
    checks["attack_family"] = section_ok("attack_family") and len(
        pkg["attack_family"]["rows"]
    ) == 4
    checks["robustness"] = (
        section_ok("robustness")
        and pkg["robustness"]["evaluated_robustness_vs_generalization"][
            "generalization_status"
        ]
        == "LIMITED"
    )
    checks["security_utility_cost"] = section_ok("security_utility_cost")
    checks["statistical_comparison"] = (
        "statistical_comparison" in pkg
        and len(pkg["statistical_comparison"]["episode_level_tests"]) > 0
    )

    cmap = pkg.get("claim_evidence_map") or {}
    mapped = all(f"C{i}" in cmap for i in range(1, 11))
    c6 = cmap.get("C6", {})
    checks["claim_evidence_map"] = (
        mapped
        and c6.get("status") == "NOT SUPPORTED"
        and c6.get("manuscript_use") == "NOT ESTABLISHED"
    )
    checks["limitations"] = len(pkg.get("limitations") or []) > 0

    # Traceability: every numeric cell has source metadata
    def cells_ok(obj) -> bool:
        if isinstance(obj, dict):
            if "raw_value" in obj and "source_artifact" in obj:
                if obj["raw_value"] == "MISSING":
                    return False
                return Path(obj["source_artifact"]).exists()
            return all(cells_ok(v) for v in obj.values())
        if isinstance(obj, list):
            return all(cells_ok(v) for v in obj)
        return True

    trace_sections = [
        "main_results",
        "ablation",
        "temporal",
        "attack_family",
        "robustness",
        "security_utility_cost",
        "statistical_comparison",
    ]
    checks["traceability"] = all(cells_ok(pkg[s]) for s in trace_sections)

    # Artifact safety: prior phases unmodified in working tree
    dirty = _git_porcelain(
        "results/phase7",
        "results/phase8",
        "results/phase9",
        "results/phase10",
    )
    hashes_now = {p: _sha(p) for p in REQUIRED_SOURCES if Path(p).exists()}
    checks["artifact_safety"] = dirty == "" and hashes_now == source_hashes_before

    checks["c6_not_supported"] = pkg["claim_evidence_map"]["C6"]["status"] == "NOT SUPPORTED"
    checks["generalization_limited"] = (
        pkg["robustness"]["evaluated_robustness_vs_generalization"][
            "generalization_status"
        ]
        == "LIMITED"
        and pkg["generalization"]["status"] == "LIMITED"
    )

    report_map = {
        "MAIN RESULTS": checks["main_results"],
        "ABLATION": checks["ablation"],
        "TEMPORAL": checks["temporal"],
        "ATTACK-FAMILY": checks["attack_family"],
        "ROBUSTNESS": checks["robustness"],
        "SECURITY-UTILITY-COST": checks["security_utility_cost"],
        "STATISTICAL COMPARISON": checks["statistical_comparison"],
        "CLAIM-EVIDENCE MAP": checks["claim_evidence_map"],
        "LIMITATIONS": checks["limitations"],
        "TRACEABILITY": checks["traceability"],
        "ARTIFACT SAFETY": checks["artifact_safety"],
    }
    pass_n = sum(1 for v in report_map.values() if v)
    fail_n = sum(1 for v in report_map.values() if not v)
    root_causes = []
    if missing_sources:
        root_causes.append(f"missing sources: {missing_sources}")
    if dirty:
        root_causes.append(f"dirty prior-phase paths: {dirty}")
    for k, v in report_map.items():
        if not v:
            root_causes.append(f"check failed: {k}")

    return {
        "checks": checks,
        "report_map": {k: ("PASS" if v else "FAIL") for k, v in report_map.items()},
        "pass": pass_n,
        "fail": fail_n,
        "warn": 0,
        "root_causes": root_causes,
        "overall": "PHASE 11 READY" if fail_n == 0 else "PHASE 11 NOT READY",
    }


def build_package() -> dict:
    for p in REQUIRED_SOURCES:
        if not Path(p).exists():
            raise FileNotFoundError(p)

    source_hashes_before = {p: _sha(p) for p in REQUIRED_SOURCES}
    p10 = _load("results/phase10/claim_evidence_matrix_v1.json")
    ms = _load("results/phase8/multiseed_summary.json")
    ab = _load("results/phase8/ablation_v1.json")
    tmp = _load("results/phase8/temporal_analysis_v1.json")
    fam = _load("results/phase8/attack_family_analysis_v1.json")
    rob = _load("results/phase8/robustness_v1.json")
    suc = _load("results/phase8/security_utility_cost_v1.json")
    stats = _load("results/phase8/statistical_comparison_v1.json")
    manifest = _load("results/phase7/phase7_manifest.json")

    pkg = {
        "phase": "11",
        "analysis": "manuscript_evidence_package",
        "version": "v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "phase7_frozen": True,
        "phase8_frozen": True,
        "phase9_frozen": True,
        "phase10_frozen": True,
        "phase10_source": "results/phase10/claim_evidence_matrix_v1.json",
        "source_artifacts": list(REQUIRED_SOURCES),
        "source_artifact_hashes": source_hashes_before,
        "phase7_reference": {
            "manifest": "results/phase7/phase7_manifest.json",
            "adaptive_summary": manifest.get("adaptive_summary"),
            "note": (
                "Main manuscript numerical table uses Phase 8A multiseed_summary; "
                "Phase 7 v2 artifacts remain frozen reference/protocol truth."
            ),
        },
        "main_results": build_main_results(ms),
        "ablation": build_ablation(ab),
        "temporal": build_temporal(tmp),
        "attack_family": build_attack_family(fam),
        "robustness": build_robustness(rob, p10),
        "security_utility_cost": build_suc(suc),
        "statistical_comparison": build_stats(stats),
        "claim_evidence_map": build_claim_map(p10),
        "generalization": {
            "status": p10["generalization"]["status"],
            "allowed_wording": p10["generalization"]["allowed_wording"],
            "disallowed_wording": p10["generalization"]["disallowed_wording"],
            "preserved_from_phase10": True,
            "source_artifact": "results/phase10/claim_evidence_matrix_v1.json",
        },
        "limitations": build_limitations(p10, stats, rob, ab),
        "precision_policy": {
            "raw_values_preserved": True,
            "no_percent_conversion_during_extraction": True,
            "no_rounding_during_extraction": True,
        },
        "integrity": {
            "phase7_modified": False,
            "phase8_modified": False,
            "phase9_modified": False,
            "phase10_modified": False,
            "experiments_rerun": False,
            "results_changed": False,
            "values_fabricated": False,
            "new_statistical_tests": False,
        },
    }

    validation = validate_package(pkg, source_hashes_before)
    pkg["validation"] = validation
    pkg["overall_readiness"] = validation["overall"]
    return pkg


def main():
    out_dir = OUT.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        pkg = json.loads(OUT.read_text(encoding="utf-8"))
        print("exists (not overwritten)", OUT)
        print("overall", pkg.get("overall_readiness"))
        vm = (pkg.get("validation") or {}).get("report_map") or {}
        for k, v in vm.items():
            print(f"{k}: {v}")
        return

    pkg = build_package()
    OUT.write_text(json.dumps(pkg, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT)
    print("overall", pkg["overall_readiness"])
    for k, v in pkg["validation"]["report_map"].items():
        print(f"{k}: {v}")
    if pkg["validation"]["root_causes"]:
        print("root_causes:")
        for r in pkg["validation"]["root_causes"]:
            print(" -", r)


if __name__ == "__main__":
    main()
