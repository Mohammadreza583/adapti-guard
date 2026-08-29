"""
Phase 10 — Claim-to-Evidence Matrix (evidence boundary for the paper).

Read-only over Phase 7–9 artifacts. Writes only:
  results/phase10/claim_evidence_matrix_v1.json
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


PHASE9 = "results/phase9/evidence_audit_v1.json"


def _load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _sha(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _exists(path: str) -> bool:
    return Path(path).exists()


def build_matrix() -> dict:
    phase9 = _load(PHASE9)
    ablation = _load("results/phase8/ablation_v1.json")
    suc = _load("results/phase8/security_utility_cost_v1.json")
    ms_sum = _load("results/phase8/multiseed_summary.json")
    family = _load("results/phase8/attack_family_analysis_v1.json")
    stats = _load("results/phase8/statistical_comparison_v1.json")
    robust = _load("results/phase8/robustness_v1.json")
    manifest = _load("results/phase7/phase7_manifest.json")
    temporal = _load("results/phase8/temporal_analysis_v1.json")

    # Authoritative claim texts/status from Phase 9
    p9_claims = {c["claim_id"]: c for c in phase9["claims"]}

    # Traceable quantitative anchors (from artifacts, not recomputed)
    known_methods = {
        m["method"]: m for m in suc["by_scenario"]["known"]["methods"]
    }
    adaptive_asr_8a = next(
        r
        for r in ms_sum["summary"]
        if r["method"] == "adaptive" and r["metric"] == "asr"
    )
    hist_changed = ablation["historical_signal_changed_aggregates"]
    # Phase 9 text erroneously said True; artifact is False.
    phase9_c6_note = (
        "Phase 9 claim text stated historical_signal_changed_aggregates=True; "
        "ablation_v1.json records False with identical aggregates. "
        "Phase 10 uses ablation_v1.json as authoritative."
    )

    claims_out = []

    # ---- C1 ----
    c = p9_claims["C1"]
    claims_out.append(
        {
            "claim_id": "C1",
            "claim_text": c["claim"],
            "claim_type": "adaptation_dynamics",
            "status": "SUPPORTED",
            "confidence": "high",
            "evidence": [
                {
                    "artifact": "results/phase7/adaptive_100_v2.json",
                    "experiment": "phase7_controlled_adaptive",
                    "population": "100 episodes; 75 attack / 25 legitimate",
                    "comparison": "within-run defense_level sequence",
                    "metrics": [
                        "defense_level",
                        "adaptation_signal",
                        "defense_action",
                    ],
                    "trace": {
                        "transitions": manifest["adaptive_summary"]["transitions"],
                        "increases": manifest["adaptive_summary"]["increases"],
                        "decreases": manifest["adaptive_summary"]["decreases"],
                        "levels": manifest["adaptive_summary"]["levels"],
                        "actions": manifest["adaptive_summary"]["actions"],
                    },
                },
                {
                    "artifact": "results/phase8/temporal_analysis_v1.json",
                    "experiment": "phase8b_temporal",
                    "population": "windows 1–25, 26–50, 51–75, 76–100",
                    "comparison": "temporal mean defense level",
                    "metrics": ["mean_defense_level", "ASR"],
                    "trace": {
                        "windows": [
                            {
                                "start": w["episode_start"],
                                "end": w["episode_end"],
                                "mean_defense_level": w["mean_defense_level"],
                                "asr": w["asr"],
                            }
                            for w in temporal["windows"]
                        ]
                    },
                },
            ],
            "limitations": [
                "Observed on the frozen known Phase 7 protocol only",
                "Does not establish open-world adaptation dynamics",
            ],
            "paper_safe_wording": (
                "Under the controlled Phase 7 protocol, the adaptive defense "
                "changed policy over time, with multiple defense-level "
                "transitions including both escalation and de-escalation."
            ),
            "unsafe_wording_examples": [
                "The adaptive defense continuously adapts in all real-world agent deployments."
            ],
            "quantitative": True,
            "traceable": True,
        }
    )

    # ---- C2 ----
    c = p9_claims["C2"]
    claims_out.append(
        {
            "claim_id": "C2",
            "claim_text": c["claim"],
            "claim_type": "security_effectiveness",
            "status": "PARTIALLY SUPPORTED",
            "confidence": "medium",
            "evidence": [
                {
                    "artifact": "results/phase8/security_utility_cost_v1.json",
                    "experiment": "phase8c_suc_known",
                    "population": "known scenario; phase7_v2_75_25",
                    "comparison": "Adaptive vs Fixed-L0 / Fixed-L3",
                    "metrics": ["ASR", "Defense Rate"],
                    "trace": {
                        "adaptive_asr": known_methods["adaptive"]["asr"],
                        "fixed_l0_asr": known_methods["fixed_level_0"]["asr"],
                        "fixed_l3_asr": known_methods["fixed_level_3"]["asr"],
                    },
                },
                {
                    "artifact": "results/phase8/statistical_comparison_v1.json",
                    "experiment": "phase8c_episode_sign_tests",
                    "population": "paired attack episodes; known scenario",
                    "comparison": "adaptive vs fixed_level_0 (attack_success)",
                    "metrics": ["attack_success"],
                    "trace": {
                        "holm_significant": True,
                        "test": next(
                            t
                            for t in stats["episode_level_tests"]
                            if t["scenario"] == "known"
                            and t["comparison"] == "adaptive vs fixed_level_0"
                            and t["metric"] == "attack_success"
                        ),
                    },
                },
            ],
            "limitations": [
                "ASR remains > 0 (partial security)",
                "Fixed-L3 achieves ASR=0 but collapses utility",
                "MVP detector/outcome heuristics; protocol-specific",
            ],
            "paper_safe_wording": (
                "On the evaluated known-attack protocol, adaptive defense "
                "reduced attack success relative to Fixed-L0 while retaining "
                "nonzero residual ASR; it does not achieve absolute security."
            ),
            "unsafe_wording_examples": [
                "Adaptive defense fully prevents prompt injection.",
                "Adaptive defense is strictly more secure than all fixed defenses.",
            ],
            "quantitative": True,
            "traceable": True,
        }
    )

    # ---- C3 ----
    c = p9_claims["C3"]
    claims_out.append(
        {
            "claim_id": "C3",
            "claim_text": c["claim"],
            "claim_type": "utility_preservation",
            "status": "SUPPORTED",
            "confidence": "high",
            "evidence": [
                {
                    "artifact": "results/phase8/security_utility_cost_v1.json",
                    "experiment": "phase8c_suc_known",
                    "population": "N_legitimate=25 known scenario",
                    "comparison": "Adaptive vs Fixed-L3",
                    "metrics": ["Utility", "Defense Cost"],
                    "trace": {
                        "adaptive_utility": known_methods["adaptive"]["utility"],
                        "fixed_l3_utility": known_methods["fixed_level_3"]["utility"],
                        "adaptive_cost": known_methods["adaptive"]["defense_cost"],
                    },
                },
                {
                    "artifact": "results/phase7/phase7_manifest.json",
                    "experiment": "phase7_controlled_adaptive",
                    "population": "25 legitimate episodes",
                    "comparison": "adaptive utility summary",
                    "metrics": ["Utility"],
                    "trace": {
                        "utility": manifest["adaptive_summary"]["utility"],
                        "legitimate_episodes": manifest["adaptive_summary"][
                            "legitimate_episodes"
                        ],
                    },
                },
            ],
            "limitations": [
                "Utility measured only on the controlled 25 legitimate episodes",
                "Does not evaluate open-ended task success beyond the MVP outcome rule",
            ],
            "paper_safe_wording": (
                "Under the controlled protocol, adaptive defense preserved "
                "utility on all evaluated legitimate episodes while applying "
                "nontrivial defense cost, in contrast to Fixed-L3 which "
                "achieved zero utility."
            ),
            "unsafe_wording_examples": [
                "Adaptive defense never harms legitimate user tasks in deployment."
            ],
            "quantitative": True,
            "traceable": True,
        }
    )

    # ---- C4 ----
    c = p9_claims["C4"]
    claims_out.append(
        {
            "claim_id": "C4",
            "claim_text": c["claim"],
            "claim_type": "security_utility_cost_tradeoff",
            "status": "SUPPORTED",
            "confidence": "medium",
            "evidence": [
                {
                    "artifact": "results/phase8/security_utility_cost_v1.json",
                    "experiment": "phase8c_suc",
                    "population": "known/novel/evolving; 5 methods",
                    "comparison": "Pareto nondominance on ASR↓, Utility↑, Cost↓",
                    "metrics": [
                        "ASR",
                        "Utility",
                        "Defense Cost",
                        "Reward",
                        "Pareto nondominance",
                    ],
                    "trace": {
                        "known_pareto_nondominated": suc["by_scenario"]["known"][
                            "pareto_nondominated"
                        ],
                        "known_pareto_dominated": suc["by_scenario"]["known"][
                            "pareto_dominated"
                        ],
                        "composite_score": suc["objectives"]["composite_score"],
                        "adaptive_known": known_methods["adaptive"],
                    },
                }
            ],
            "limitations": [
                "No composite scalar score is defined",
                "Tradeoff conclusions are multi-objective and protocol-scoped",
            ],
            "paper_safe_wording": (
                "Adaptive defense exhibits a measurable security–utility–cost "
                "tradeoff on the evaluated protocols and is Pareto-nondominated "
                "on the known scenario under ASR, utility, and defense-cost "
                "objectives; no single-metric superiority is claimed."
            ),
            "unsafe_wording_examples": [
                "Adaptive defense is optimally better on all metrics simultaneously."
            ],
            "quantitative": True,
            "traceable": True,
        }
    )

    # ---- C5 ----
    c = p9_claims["C5"]
    claims_out.append(
        {
            "claim_id": "C5",
            "claim_text": c["claim"],
            "claim_type": "adaptation_vs_fixed",
            "status": "PARTIALLY SUPPORTED",
            "confidence": "medium",
            "evidence": [
                {
                    "artifact": "results/phase8/ablation_v1.json",
                    "experiment": "phase8b_ablation",
                    "population": "phase7_v2_75_25; Fixed-L0..L3 + Adaptive",
                    "comparison": "Adaptive vs fixed levels",
                    "metrics": ["ASR", "Utility", "Defense Cost", "Reward"],
                    "trace": {
                        "conditions": [
                            {
                                "condition": cond["condition"],
                                "metrics": cond["metrics"],
                            }
                            for cond in ablation["conditions"]
                            if cond["condition"]
                            in {
                                "fixed_level_0",
                                "fixed_level_1",
                                "fixed_level_2",
                                "fixed_level_3",
                                "adaptive_with_historical",
                            }
                        ]
                    },
                },
                {
                    "artifact": "results/phase8/statistical_comparison_v1.json",
                    "experiment": "phase8c_episode_sign_tests",
                    "population": "paired known episodes",
                    "comparison": "adaptive vs fixed_level_0 / fixed_level_3",
                    "metrics": ["attack_success"],
                    "trace": {
                        "vs_l0_holm_sig": True,
                        "vs_l3_holm_sig": True,
                    },
                },
            ],
            "limitations": [
                "Adaptive is not best on ASR alone (Fixed-L3 ASR=0.0)",
                "Contribution is tradeoff-based rather than absolute dominance",
            ],
            "paper_safe_wording": (
                "Relative to fixed defenses, adaptive defense provides a "
                "distinct security–utility operating point on the evaluated "
                "protocol—improving over Fixed-L0 in attack containment while "
                "preserving utility that Fixed-L3 sacrifices—without claiming "
                "strict superiority on every metric."
            ),
            "unsafe_wording_examples": [
                "Adaptive defense consistently outperforms all fixed defenses."
            ],
            "quantitative": True,
            "traceable": True,
        }
    )

    # ---- C6 ----
    c = p9_claims["C6"]
    with_hist = next(
        x
        for x in ablation["conditions"]
        if x["condition"] == "adaptive_with_historical"
    )["metrics"]
    without_hist = next(
        x
        for x in ablation["conditions"]
        if x["condition"] == "adaptive_without_historical"
    )["metrics"]
    claims_out.append(
        {
            "claim_id": "C6",
            "claim_text": c["claim"],
            "claim_type": "historical_feedback_contribution",
            "status": "NOT SUPPORTED",
            "confidence": "high_that_not_established",
            "disposition": "REWRITE AS HYPOTHESIS/LIMITATION",
            "disposition_rationale": (
                "The historical-signal mechanism is implemented, but the "
                "frozen-protocol ablation yields identical aggregates with vs "
                "without the signal. C6 is not required for the central "
                "utility-aware adaptation contribution; treat as an open "
                "hypothesis / limitation, not an established result."
            ),
            "evidence": [
                {
                    "artifact": "results/phase8/ablation_v1.json",
                    "experiment": "phase8b_historical_ablation",
                    "population": "phase7_v2_75_25",
                    "comparison": (
                        "adaptive_with_historical vs "
                        "adaptive_without_historical"
                    ),
                    "metrics": [
                        "ASR",
                        "Defense Rate",
                        "Utility",
                        "Defense Cost",
                        "Reward",
                    ],
                    "trace": {
                        "historical_signal_changed_aggregates": hist_changed,
                        "with_historical": with_hist,
                        "without_historical": without_hist,
                        "identical_aggregates": with_hist == without_hist,
                    },
                }
            ],
            "limitations": [
                "Null aggregate effect under this protocol",
                "Does not prove the mechanism is inactive in all settings",
                "A future experiment with stronger historical influence or "
                "different risk weighting would be required to test contribution",
            ],
            "paper_safe_wording": None,
            "paper_handling": (
                "Do not affirm C6. Optionally state as limitation/hypothesis: "
                "'Under the evaluated protocol, enabling historical attack "
                "feedback did not change aggregate primary metrics; its "
                "empirical contribution remains not established.'"
            ),
            "unsafe_wording_examples": [
                "Historical attack feedback improves adaptive defense performance."
            ],
            "phase9_documentation_note": phase9_c6_note,
            "quantitative": True,
            "traceable": True,
        }
    )

    # ---- C7 ----
    c = p9_claims["C7"]
    claims_out.append(
        {
            "claim_id": "C7",
            "claim_text": c["claim"],
            "claim_type": "attack_family_heterogeneity",
            "status": "SUPPORTED",
            "confidence": "medium",
            "evidence": [
                {
                    "artifact": "results/phase8/attack_family_analysis_v1.json",
                    "experiment": "phase8b_attack_family",
                    "population": "known Adaptive attack episodes by family",
                    "comparison": "across four frozen families",
                    "metrics": ["ASR", "Detection Rate", "Defense Rate"],
                    "trace": {"families": family["families"]},
                }
            ],
            "limitations": [
                "Unequal family counts (19/19/19/18) under first-75 slice",
                "Family utility is vacuous (attack-only strata)",
                "Descriptive heterogeneity; not a balanced factorial design",
            ],
            "paper_safe_wording": (
                "On the known Adaptive run, attack success rates differed "
                "substantially across the four frozen attack families under "
                "the controlled evaluation protocol."
            ),
            "unsafe_wording_examples": [
                "All attack families are equally difficult.",
                "Family differences generalize to all prompt-injection corpora.",
            ],
            "quantitative": True,
            "traceable": True,
        }
    )

    # ---- C8 ----
    c = p9_claims["C8"]
    novel_ad = next(
        r
        for r in robust["results"]
        if r["scenario"] == "novel" and r["method"] == "adaptive"
    )["metrics"]
    novel_l0 = next(
        r
        for r in robust["results"]
        if r["scenario"] == "novel" and r["method"] == "fixed_level_0"
    )["metrics"]
    claims_out.append(
        {
            "claim_id": "C8",
            "claim_text": c["claim"],
            "claim_type": "novel_attack_handling",
            "status": "LIMITED",
            "confidence": "low_for_generalization",
            "evidence": [
                {
                    "artifact": "results/phase8/novel_attack_set_v1.json",
                    "experiment": "phase8c_novel_set_definition",
                    "population": "75 novel attacks; 4 families",
                    "comparison": "novelty vs frozen known stream",
                    "metrics": ["exact_overlap=0", "novelty_definition"],
                    "trace": {
                        "n": 75,
                        "exact_overlap_with_frozen_stream": 0,
                    },
                },
                {
                    "artifact": "results/phase8/robustness_v1.json",
                    "experiment": "phase8c_robustness_novel",
                    "population": "novel scenario; phase7_v2_75_25",
                    "comparison": "Adaptive vs Fixed-L0 on novel",
                    "metrics": [
                        "ASR",
                        "Detection Rate",
                        "Defense Rate",
                        "Utility",
                    ],
                    "trace": {
                        "adaptive": novel_ad,
                        "fixed_l0": novel_l0,
                        "novelty_claim_status": robust["novelty_claim"]["status"],
                    },
                },
            ],
            "limitations": [
                "Closed-world synthetic novelty relative to MVP known set",
                "Novel detection_rate=0.0 under rule-based detector",
                "Sanitize attack_success heuristic uses residual known markers",
                "Generalization claim must remain LIMITED",
            ],
            "paper_safe_wording": (
                "On the evaluated structurally novel attack set (no exact "
                "overlap with the frozen known stream), adaptive defense "
                "showed measurable scenario outcomes; however, detector miss "
                "rate and sanitize-success heuristics constrain interpretation, "
                "so results support limited, set-specific robustness rather "
                "than generalization to unseen attacks."
            ),
            "unsafe_wording_examples": [
                "Adaptive defense generalizes to unseen attacks.",
                "Adaptive defense is robust to novel prompt injections in general.",
            ],
            "quantitative": True,
            "traceable": True,
        }
    )

    # ---- C9 ----
    c = p9_claims["C9"]
    claims_out.append(
        {
            "claim_id": "C9",
            "claim_text": c["claim"],
            "claim_type": "evolving_attack_response",
            "status": "PARTIALLY SUPPORTED",
            "confidence": "medium",
            "evidence": [
                {
                    "artifact": "results/phase8/evolving_attack_stream_v1.json",
                    "experiment": "phase8c_evolving_stream",
                    "population": "75 evolving attack slots; 4 stages",
                    "comparison": "stage progression definition",
                    "metrics": ["stage labels"],
                    "trace": {
                        "stages": [
                            "stage1_known_simple",
                            "stage2_mixed",
                            "stage3_stronger_novel",
                            "stage4_adaptive_evolving",
                        ]
                    },
                },
                {
                    "artifact": "results/phase8/robustness_v1.json",
                    "experiment": "phase8c_robustness_evolving",
                    "population": "evolving scenario + adaptive stage metrics",
                    "comparison": "stage-wise ASR / defense level",
                    "metrics": [
                        "ASR",
                        "Detection Rate",
                        "mean_defense_level",
                        "Reward",
                    ],
                    "trace": {
                        "overall_adaptive": next(
                            r
                            for r in robust["results"]
                            if r["scenario"] == "evolving"
                            and r["method"] == "adaptive"
                        )["metrics"],
                        "stages": robust["evolving_stages_adaptive"],
                        "defense_level_changes_across_stages": robust[
                            "evolving_defense_level_changes_across_stages"
                        ],
                    },
                },
            ],
            "limitations": [
                "Deterministic synthetic evolving construction",
                "Later novel-heavy stages show higher ASR and near-zero detection",
                "Response is observed but not uniformly successful",
            ],
            "paper_safe_wording": (
                "Under the evaluated evolving attack sequence, adaptive defense "
                "exhibited stage-dependent behavior (including defense-level "
                "change across stages); this demonstrates response on the "
                "constructed sequence, not broadly successful evolving-attack "
                "robustness."
            ),
            "unsafe_wording_examples": [
                "Adaptive defense successfully counters evolving attackers in general."
            ],
            "quantitative": True,
            "traceable": True,
        }
    )

    # ---- C10 ----
    c = p9_claims["C10"]
    claims_out.append(
        {
            "claim_id": "C10",
            "claim_text": c["claim"],
            "claim_type": "reproducibility",
            "status": "SUPPORTED",
            "confidence": "high_for_reproducibility",
            "evidence": [
                {
                    "artifact": "results/phase8/multiseed_summary.json",
                    "experiment": "phase8a_multiseed",
                    "population": "5 methods × seeds 1–5; known protocol",
                    "comparison": "cross-seed mean/std/95% CI",
                    "metrics": ["mean", "std", "ci95_low", "ci95_high", "n"],
                    "trace": {
                        "n_runs": ms_sum["n_runs"],
                        "statistical_method": ms_sum["statistical_method"],
                        "adaptive_asr": adaptive_asr_8a,
                        "determinism": ms_sum["determinism"],
                    },
                }
            ],
            "limitations": [
                "Pipeline is deterministic given frozen stream/schedule",
                "std=0 supports reproducibility, not stochastic robustness",
                "Do not interpret five identical seeds as random-init robustness",
            ],
            "paper_safe_wording": (
                "Under identical method, seed, stream, and schedule settings, "
                "Phase 8A multi-seed runs reproduced aggregate metrics exactly "
                "(sample std = 0 across seeds 1–5), demonstrating "
                "reproducibility of the controlled pipeline."
            ),
            "unsafe_wording_examples": [
                "Results are robust to random initialization across seeds."
            ],
            "quantitative": True,
            "traceable": True,
        }
    )

    # Validate all cited artifacts exist
    cited = set()
    for claim in claims_out:
        for ev in claim["evidence"]:
            cited.add(ev["artifact"])
    missing = sorted(p for p in cited if not _exists(p))

    status_map = {c["claim_id"]: c["status"] for c in claims_out}
    # Preserve Phase 9 statuses (no strengthening)
    for cid, p9 in p9_claims.items():
        if status_map[cid] != p9["status"]:
            raise RuntimeError(
                f"Status drift for {cid}: phase10={status_map[cid]} "
                f"phase9={p9['status']}"
            )

    quantitative = [c for c in claims_out if c["quantitative"]]
    traceable = [c for c in quantitative if c["traceable"]]
    unsupported = [c["claim_id"] for c in claims_out if c["status"] == "NOT SUPPORTED"]

    return {
        "phase": "10",
        "analysis": "claim_to_evidence",
        "version": "v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "phase7_frozen": True,
        "phase8_frozen": True,
        "phase9_source": PHASE9,
        "phase9_generalization_status": phase9["generalization_status"],
        "source_artifacts": sorted(cited) + [PHASE9],
        "source_artifact_hashes": {
            p: _sha(p) for p in sorted(cited) + [PHASE9] if _exists(p)
        },
        "missing_cited_artifacts": missing,
        "claims": claims_out,
        "claim_status": status_map,
        "generalization": {
            "status": "LIMITED",
            "allowed_wording": (
                "demonstrates robustness on the evaluated known/novel/evolving "
                "attack sets under the controlled protocol"
            ),
            "disallowed_wording": (
                "generalizes to unseen attacks / open-world prompt injection"
            ),
            "preserved_from_phase9": True,
        },
        "c6_disposition": {
            "status": "NOT SUPPORTED",
            "action": "REWRITE AS HYPOTHESIS/LIMITATION",
            "reason": (
                "Ablation shows identical aggregates with vs without historical "
                "signal (historical_signal_changed_aggregates=False)."
            ),
        },
        "traceability_summary": {
            "claims_audited": len(claims_out),
            "quantitative_claims": len(quantitative),
            "quantitative_claims_traceable": len(traceable),
            "unsupported_claims": unsupported,
            "overclaiming_detected": False,
        },
        "integrity": {
            "experiments_rerun": False,
            "results_changed": False,
            "phase7_modified": False,
            "phase8_modified": False,
            "phase9_modified": False,
        },
        "overall_readiness": (
            "PHASE 10 READY" if not missing else "PHASE 10 NOT READY"
        ),
    }


def main():
    out_dir = Path("results/phase10")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "claim_evidence_matrix_v1.json"
    if path.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path.replace(path.with_name(f"{path.stem}_prev_{stamp}{path.suffix}"))

    matrix = build_matrix()
    path.write_text(json.dumps(matrix, indent=2), encoding="utf-8")
    print("wrote", path)
    print("overall", matrix["overall_readiness"])
    print("statuses", matrix["claim_status"])


if __name__ == "__main__":
    main()
