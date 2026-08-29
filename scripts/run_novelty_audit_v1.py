#!/usr/bin/env python3
"""
Final novelty audit — literature comparison only.

Writes:
  ANALYSIS/novelty_audit_v1.json
  ANALYSIS/novelty_audit_v1.txt

Does not modify source code or Phase 7–11 artifacts.
Does not overwrite existing novelty_audit_v1.* files.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

OUT_JSON = Path("ANALYSIS/novelty_audit_v1.json")
OUT_TXT = Path("ANALYSIS/novelty_audit_v1.txt")

PRIOR_PATHS = [
    "results/phase7",
    "results/phase8",
    "results/phase9",
    "results/phase10",
    "results/phase11",
    "src",
]


def _sha(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build() -> dict:
    # Local folders named in the task were absent from this cloud workspace.
    # Inventory is therefore the publicly retrieved unique papers matching the
    # named critical works plus clearly relevant adjacent papers retrieved for
    # comparison. This limitation is recorded explicitly (no fabricated local PDF inventory).

    papers = [
        {
            "paper_id": "P01_AgentAntibody",
            "title": "AgentAntibody: An Adaptive Immune System for Defending LLM Agents against Prompt Injection",
            "arxiv": "2608.04053",
            "source_group": "critical+05_2025_2026_proxy",
            "source_uri": "https://arxiv.org/abs/2608.04053",
            "profile": {
                "threat_model": "prompt injection exploiting underspecified user security boundary",
                "attack_setting": "agent tasks; LatentBoundaryBench + AgentDyn-style settings",
                "defense_mechanism": "training-free antibody library with epitope matching and targeted responses (sanitize/constrain/revise/confirm)",
                "adaptive_mechanism": "online maturation/induction of antibodies from action-level feedback",
                "memory_history": True,
                "feedback_signal": "user AS/FP labels and weak BA evidence",
                "adaptation_timing": "runtime",
                "utility_preservation": True,
                "defense_cost": "not as explicit discrete cost metric; response specificity aims to avoid full refusal",
                "temporal_adaptation": True,
                "evaluation_protocol": "multi-benchmark, multi-backbone; cumulative ASR over encounters",
                "novel_evolving_eval": "transfer across attacks; cumulative immunity gain; not AG 75/25 protocol",
            },
            "overlap_class": "PARTIAL_OVERLAP",
            "overlap_explanation": {
                "paper_mechanism": "Persistent evolving antibody memory adapts runtime responses to learned user boundary.",
                "adapti_guard_mechanism": "Discrete defense levels L0–L3 with policy escalate/de-escalate under utility-aware reward/SUC on a controlled mixed stream.",
                "shared": ["runtime adaptation", "history/memory", "utility preservation goal"],
                "differing": [
                    "no explicit discrete defense-level state machine",
                    "no explicit defense-cost accounting / Pareto vs fixed levels",
                    "adaptation target is user boundary antibodies, not intensity levels",
                ],
            },
            "checklist_A_to_G": {
                "A_runtime_defense_level_adaptation": False,
                "B_utility_aware_escalation_deescalation": "partial_utility_preserving_responses_not_level_policy",
                "C_explicit_defense_policy_state_transitions": False,
                "D_history_conditioned_policy_updates": True,
                "E_simultaneous_security_utility_cost_optimization": False,
                "F_controlled_mixed_attack_legitimate_protocol": False,
                "G_adaptation_under_evolving_attacks": "partial_cumulative_transfer",
            },
        },
        {
            "paper_id": "P02_COPA",
            "title": "COPA: Continual Preference Optimization for Adaptive Prompt Injection Defense",
            "arxiv": "2608.19982",
            "source_group": "critical+05_2025_2026_proxy",
            "source_uri": "https://arxiv.org/abs/2608.19982",
            "profile": {
                "threat_model": "evolving prompt-injection attack distribution / adaptive adversaries",
                "attack_setting": "lifelong CyberSecEval variant stream",
                "defense_mechanism": "LoRA adapter + GRPO preference optimization",
                "adaptive_mechanism": "continual training on new attack variants with margin-weighted replay",
                "memory_history": "replay buffer of preference pairs",
                "feedback_signal": "safety preference / judge rewards",
                "adaptation_timing": "training_time_continual",
                "utility_preservation": "benign capability retention objective",
                "defense_cost": "not discrete runtime defense cost",
                "temporal_adaptation": "across lifelong tasks, not episode defense levels",
                "evaluation_protocol": "sequential attack curriculum; backward transfer",
                "novel_evolving_eval": True,
            },
            "overlap_class": "PARTIAL_OVERLAP",
            "overlap_explanation": {
                "paper_mechanism": "Training-time continual preference optimization against evolving attack streams.",
                "adapti_guard_mechanism": "Runtime policy adaptation of defense intensity without weight updates.",
                "shared": ["adaptation to evolving attacks", "retain prior robustness", "utility concern"],
                "differing": [
                    "COPA updates model parameters; AG updates discrete policy state",
                    "no AG-style defense levels or SUC episode protocol",
                ],
            },
            "checklist_A_to_G": {
                "A_runtime_defense_level_adaptation": False,
                "B_utility_aware_escalation_deescalation": False,
                "C_explicit_defense_policy_state_transitions": False,
                "D_history_conditioned_policy_updates": "replay_during_training_only",
                "E_simultaneous_security_utility_cost_optimization": False,
                "F_controlled_mixed_attack_legitimate_protocol": False,
                "G_adaptation_under_evolving_attacks": True,
            },
        },
        {
            "paper_id": "P03_BeyondHandcrafted_HARD",
            "title": "Beyond Handcrafted Security: Towards Self-Evolving Defense for LLM Agents (HARD)",
            "arxiv": "2608.12977",
            "source_group": "critical+05_2025_2026_proxy",
            "source_uri": "https://arxiv.org/abs/2608.12977",
            "profile": {
                "threat_model": "DPI/IPI/memory contamination/skill poisoning; adaptive/long-horizon attacks",
                "attack_setting": "AgentCanary (+ AgentHazard translation)",
                "defense_mechanism": "editable harness interventions (context construction + action interpretation)",
                "adaptive_mechanism": "LLM evolvers refine harness artifacts from failure trajectories (offline/iterative evolution)",
                "memory_history": "failure trajectory pool across evolution iterations",
                "feedback_signal": "failed trajectories / safety-utility objectives",
                "adaptation_timing": "runtime_defense_artifacts_evolved_between_deployments",
                "utility_preservation": True,
                "defense_cost": "security–utility optimization formulation; not AG discrete cost levels",
                "temporal_adaptation": "evolution iterations",
                "evaluation_protocol": "static + adaptive attack settings; BU/UA metrics",
                "novel_evolving_eval": True,
            },
            "overlap_class": "PARTIAL_OVERLAP",
            "overlap_explanation": {
                "paper_mechanism": "Self-evolving harness refinement from failures; improves runtime defenses over evolution cycles.",
                "adapti_guard_mechanism": "Fixed rule/policy adapts defense level within a single episode stream; no harness rewriting evolver.",
                "shared": ["runtime defense paradigm", "security–utility tradeoff", "evolving/adaptive attack eval"],
                "differing": [
                    "HARD evolves defense artifacts via LLM evolvers; AG transitions discrete levels",
                    "not the same as episode-level escalate/de-escalate policy",
                ],
            },
            "checklist_A_to_G": {
                "A_runtime_defense_level_adaptation": False,
                "B_utility_aware_escalation_deescalation": "partial_utility_preserving_evolution_not_level_policy",
                "C_explicit_defense_policy_state_transitions": False,
                "D_history_conditioned_policy_updates": "failure_trace_conditioned_evolution",
                "E_simultaneous_security_utility_cost_optimization": "partial_security_utility_not_explicit_cost_levels",
                "F_controlled_mixed_attack_legitimate_protocol": False,
                "G_adaptation_under_evolving_attacks": True,
            },
        },
        {
            "paper_id": "P04_SecOPD",
            "title": "SecOPD: Mitigating Adaptive Prompt Injections by On-Policy Distillation",
            "arxiv": "2608.21500",
            "source_group": "critical+05_2025_2026_proxy",
            "source_uri": "https://arxiv.org/abs/2608.21500",
            "profile": {
                "threat_model": "adaptive prompt injections (PISmith) against model-level defenses",
                "attack_setting": "SEP + AgentDojo transfer",
                "defense_mechanism": "token-level on-policy distillation from clean-teacher scores",
                "adaptive_mechanism": "none at runtime; training recipe improves static model robustness",
                "memory_history": False,
                "feedback_signal": "token-level teacher advantages",
                "adaptation_timing": "training_time",
                "utility_preservation": True,
                "defense_cost": "training/compute; not runtime defense-cost levels",
                "temporal_adaptation": False,
                "evaluation_protocol": "static + adaptive ASR; utility benchmarks",
                "novel_evolving_eval": "adaptive_attack_eval_not_runtime_adaptation",
            },
            "overlap_class": "ADJACENT",
            "overlap_explanation": {
                "paper_mechanism": "Model-level fine-tuning with token-level feedback against adaptive attacks.",
                "adapti_guard_mechanism": "Runtime discrete defense policy over a fixed detector/sanitizer stack.",
                "shared": ["prompt injection", "utility preservation", "adaptive-attack evaluation"],
                "differing": ["no runtime policy adaptation", "no defense levels"],
            },
            "checklist_A_to_G": {
                "A_runtime_defense_level_adaptation": False,
                "B_utility_aware_escalation_deescalation": False,
                "C_explicit_defense_policy_state_transitions": False,
                "D_history_conditioned_policy_updates": False,
                "E_simultaneous_security_utility_cost_optimization": False,
                "F_controlled_mixed_attack_legitimate_protocol": False,
                "G_adaptation_under_evolving_attacks": False,
            },
        },
        {
            "paper_id": "P05_AdaptiveAdversaries",
            "title": "Adaptive Adversaries: A Multi-Turn, Multi-LLM Benchmark for LLM Agent Security",
            "arxiv": "2607.18063",
            "source_group": "critical+05_2025_2026_proxy",
            "source_uri": "https://arxiv.org/abs/2607.18063",
            "profile": {
                "threat_model": "adaptive multi-round LLM attackers vs memoryless defenders",
                "attack_setting": "21-scenario multi-turn benchmark",
                "defense_mechanism": "none (evaluation benchmark)",
                "adaptive_mechanism": "attacker adapts across rounds; defender is memoryless by design",
                "memory_history": "attacker observes prior defender responses",
                "feedback_signal": "n/a (benchmark)",
                "adaptation_timing": "n/a",
                "utility_preservation": "n/a",
                "defense_cost": "n/a",
                "temporal_adaptation": "multi-round attacker adaptation",
                "evaluation_protocol": "adaptive multi-turn ASR; multi-attacker pooling",
                "novel_evolving_eval": True,
            },
            "overlap_class": "COMPLEMENTARY",
            "overlap_explanation": {
                "paper_mechanism": "Benchmark showing adaptive multi-turn attackers beat single-turn evaluation.",
                "adapti_guard_mechanism": "Defense system with controlled evolving synthetic stream evaluation.",
                "shared": ["evolving/adaptive attack evaluation concern"],
                "differing": [
                    "not a defense method",
                    "AG evolving protocol is synthetic staged stream, not multi-turn LLM attacker",
                ],
            },
            "checklist_A_to_G": {
                "A_runtime_defense_level_adaptation": False,
                "B_utility_aware_escalation_deescalation": False,
                "C_explicit_defense_policy_state_transitions": False,
                "D_history_conditioned_policy_updates": False,
                "E_simultaneous_security_utility_cost_optimization": False,
                "F_controlled_mixed_attack_legitimate_protocol": False,
                "G_adaptation_under_evolving_attacks": "attacker_side_only",
            },
        },
        {
            "paper_id": "P06_SCOUT",
            "title": "Send a SCOUT First: Pre-hoc Reasoning for Adaptive Detector Allocation in Prompt-Injection Defense",
            "arxiv": "2605.30837",
            "source_group": "critical+05_2025_2026_proxy",
            "source_uri": "https://arxiv.org/abs/2605.30837",
            "profile": {
                "threat_model": "heterogeneous prompt-injection detectors with uneven coverage",
                "attack_setting": "SCOUT-450 + BIPIA/IPI/IHEval transfer",
                "defense_mechanism": "per-input detector allocation / escalate to LLM judge",
                "adaptive_mechanism": "predictor estimates per-detector reliability/latency from fingerprint history; threshold τ routes",
                "memory_history": "detector fingerprints from similar past inputs (anchor bank)",
                "feedback_signal": "predicted correctness/latency; operator threshold",
                "adaptation_timing": "runtime_routing_with_trained_predictor",
                "utility_preservation": "benign-pass + wall-clock utility",
                "defense_cost": "explicit latency/cost via predicted wall-clock and τ",
                "temporal_adaptation": "per-request allocation (not defense-level trajectory)",
                "evaluation_protocol": "safety–utility–latency frontier sweeps",
                "novel_evolving_eval": "external transfer; not AG evolving stream",
            },
            "overlap_class": "PARTIAL_OVERLAP",
            "overlap_explanation": {
                "paper_mechanism": "Adaptive selection among detectors under a safety–utility–latency threshold.",
                "adapti_guard_mechanism": "Adaptive selection among discrete defense intensity levels with escalate/de-escalate and SUC reward.",
                "shared": [
                    "runtime adaptive defense intensity/resource allocation",
                    "explicit safety–utility (and cost/latency) tradeoff control",
                    "history-informed decisions",
                ],
                "differing": [
                    "SCOUT allocates detectors; AG allocates defense levels L0–L3",
                    "SCOUT does not implement AG-style escalation/de-escalation state machine over mixed attack/legitimate episodes",
                ],
            },
            "checklist_A_to_G": {
                "A_runtime_defense_level_adaptation": "partial_detector_allocation_not_L0_L3_levels",
                "B_utility_aware_escalation_deescalation": "partial_threshold_escalation_to_judge",
                "C_explicit_defense_policy_state_transitions": False,
                "D_history_conditioned_policy_updates": True,
                "E_simultaneous_security_utility_cost_optimization": "partial_safety_utility_latency",
                "F_controlled_mixed_attack_legitimate_protocol": False,
                "G_adaptation_under_evolving_attacks": False,
            },
        },
        {
            "paper_id": "P07_SafeHarness",
            "title": "SafeHarness: Lifecycle-Integrated Security Architecture for LLM-based Agent Deployment",
            "arxiv": "2604.13630",
            "source_group": "adjacent_discovered_strong_overlap",
            "source_uri": "https://arxiv.org/abs/2604.13630",
            "profile": {
                "threat_model": "harness-phase attacks across input/decision/action/state; memory corruption",
                "attack_setting": "multi-harness configurations; attack scenarios A1–A5",
                "defense_mechanism": "Inform/Verify/Constrain/Correct layers with privilege tiers",
                "adaptive_mechanism": "Correct degradation levels 0–4 escalate on attack; recover/de-escalate after safe window; entropy monitor escalates verification",
                "memory_history": "checkpoints, protected memory, windowed violation rate",
                "feedback_signal": "attack detections, violation-rate entropy, consecutive safe actions",
                "adaptation_timing": "runtime",
                "utility_preservation": True,
                "defense_cost": "security–efficiency trade-offs via interception; not AG SUC reward formulation",
                "temporal_adaptation": True,
                "evaluation_protocol": "ASR/unsafe behavior vs baselines; utility retained",
                "novel_evolving_eval": "composite/evolving attack discussion; not AG protocol",
            },
            "overlap_class": "DIRECT_OVERLAP",
            "overlap_explanation": {
                "paper_mechanism": "Explicit multi-level degradation with escalate on detected attack and de-escalate after consecutive safe actions; privilege ceiling tightens with level.",
                "adapti_guard_mechanism": "Explicit multi-level defense intensity with escalate/de-escalate under utility-aware feedback and defense cost.",
                "shared": [
                    "runtime discrete defense/privilege levels",
                    "explicit escalate and de-escalate transitions",
                    "utility-preserving recovery intent",
                    "history/windowed signals influencing policy",
                ],
                "differing": [
                    "SafeHarness levels map to tool-privilege ceilings; AG levels map to detect/sanitize intensity stack",
                    "SafeHarness lacks AG's explicit SUC composite + fixed-level Pareto protocol and 75/25 mixed schedule analysis package",
                    "AG historical-signal ablation is null (C6 NOT SUPPORTED); SafeHarness uses violation windows/checkpoints operationally",
                ],
                "novelty_impact": "Strongly weakens any claim that discrete runtime escalate/de-escalate defense levels are unique to ADAPTI-GUARD.",
            },
            "checklist_A_to_G": {
                "A_runtime_defense_level_adaptation": True,
                "B_utility_aware_escalation_deescalation": True,
                "C_explicit_defense_policy_state_transitions": True,
                "D_history_conditioned_policy_updates": True,
                "E_simultaneous_security_utility_cost_optimization": False,
                "F_controlled_mixed_attack_legitimate_protocol": False,
                "G_adaptation_under_evolving_attacks": "partial",
            },
        },
        {
            "paper_id": "P08_CaMeL",
            "title": "Defeating Prompt Injections by Design (CaMeL)",
            "arxiv": "2503.18813",
            "source_group": "03_DEFENSE_proxy",
            "source_uri": "https://arxiv.org/abs/2503.18813",
            "profile": {
                "threat_model": "prompt injection into agent tool/data flows",
                "attack_setting": "AgentDojo",
                "defense_mechanism": "extract trusted control/data flow; capability policies; out-of-band enforcement",
                "adaptive_mechanism": False,
                "memory_history": False,
                "feedback_signal": "n/a",
                "adaptation_timing": "static_runtime_architecture",
                "utility_preservation": True,
                "defense_cost": "utility drop vs undefended",
                "temporal_adaptation": False,
                "evaluation_protocol": "AgentDojo tasks under attack",
                "novel_evolving_eval": False,
            },
            "overlap_class": "ADJACENT",
            "overlap_explanation": {
                "paper_mechanism": "Deterministic system-layer control/data-flow isolation.",
                "adapti_guard_mechanism": "Adaptive intensity policy over heuristic detect/sanitize stack.",
                "shared": ["agent prompt-injection defense", "utility consideration"],
                "differing": ["static architectural defense vs adaptive levels"],
            },
        },
        {
            "paper_id": "P09_Progent",
            "title": "Progent: Programmable Privilege Control for LLM Agents",
            "arxiv": "2504.11703",
            "source_group": "03_DEFENSE_proxy",
            "source_uri": "https://arxiv.org/abs/2504.11703",
            "profile": {
                "threat_model": "tool misuse via prompt injection",
                "attack_setting": "AgentDojo-style agent tool calling",
                "defense_mechanism": "programmable privilege/policy control at tool boundary",
                "adaptive_mechanism": False,
                "memory_history": False,
                "feedback_signal": "n/a",
                "adaptation_timing": "static_runtime_enforcement",
                "utility_preservation": True,
                "defense_cost": "utility impact reported vs baselines",
                "temporal_adaptation": False,
                "evaluation_protocol": "AgentDojo + adaptive-attack discussions in follow-on eval literature",
                "novel_evolving_eval": False,
            },
            "overlap_class": "ADJACENT",
            "overlap_explanation": {
                "paper_mechanism": "Privilege policies at tool boundary.",
                "adapti_guard_mechanism": "Adaptive defense levels over detect/sanitize pipeline.",
                "shared": ["runtime agent defense", "privilege/intensity notion"],
                "differing": ["Progent policies are not AG episode escalate/de-escalate SUC controller"],
            },
        },
        {
            "paper_id": "P10_MetaSecAlign",
            "title": "Meta SecAlign: A Secure Foundation LLM Against Prompt Injection Attacks",
            "arxiv": "2507.02735",
            "source_group": "03_DEFENSE_proxy",
            "source_uri": "https://arxiv.org/abs/2507.02735",
            "profile": {
                "threat_model": "prompt injection",
                "attack_setting": "SEP, AgentDojo, others",
                "defense_mechanism": "model-level SecAlign-style fine-tuning with secure delimiters",
                "adaptive_mechanism": False,
                "memory_history": False,
                "feedback_signal": "training preferences",
                "adaptation_timing": "training_time",
                "utility_preservation": True,
                "defense_cost": "n/a runtime levels",
                "temporal_adaptation": False,
                "evaluation_protocol": "security–utility tradeoff across benchmarks",
                "novel_evolving_eval": False,
            },
            "overlap_class": "ADJACENT",
            "overlap_explanation": {
                "paper_mechanism": "Static model-level separation training.",
                "adapti_guard_mechanism": "Runtime adaptive levels.",
                "shared": ["security–utility tradeoff reporting"],
                "differing": ["no runtime adaptation"],
            },
        },
        {
            "paper_id": "P11_AttriGuard",
            "title": "AttriGuard: Defeating Indirect Prompt Injection in LLM Agents via Causal Attribution of Tool Invocations",
            "arxiv": "2603.10749",
            "source_group": "02_AGENT_SECURITY_proxy",
            "source_uri": "https://arxiv.org/abs/2603.10749",
            "profile": {
                "threat_model": "indirect prompt injection via tool observations",
                "attack_setting": "AgentDojo, ASB; adaptive optimization attacks",
                "defense_mechanism": "runtime counterfactual causal attribution of tool calls",
                "adaptive_mechanism": False,
                "memory_history": "teacher-forced replay for attribution",
                "feedback_signal": "counterfactual survival tests",
                "adaptation_timing": "runtime_static_procedure",
                "utility_preservation": True,
                "defense_cost": "token overhead ~2x",
                "temporal_adaptation": False,
                "evaluation_protocol": "static + adaptive ASR; utility",
                "novel_evolving_eval": "adaptive_attack_eval",
            },
            "overlap_class": "ADJACENT",
            "overlap_explanation": {
                "paper_mechanism": "Per-call causal attribution defense with cost/utility tradeoff.",
                "adapti_guard_mechanism": "Level-based escalate/de-escalate controller.",
                "shared": ["runtime defense", "utility vs cost"],
                "differing": ["no discrete level policy state machine"],
            },
        },
        {
            "paper_id": "P12_AgentVisor",
            "title": "AgentVisor: Defending LLM Agents Against Prompt Injection via Semantic Virtualization",
            "arxiv": "2604.24118",
            "source_group": "02_AGENT_SECURITY_proxy",
            "source_uri": "https://arxiv.org/abs/2604.24118",
            "profile": {
                "threat_model": "direct/indirect prompt injection",
                "attack_setting": "agent tool-use settings",
                "defense_mechanism": "semantic virtualization / STI audit + one-shot self-correction",
                "adaptive_mechanism": "self-correction on violation (not multi-level policy)",
                "memory_history": False,
                "feedback_signal": "semantic exceptions",
                "adaptation_timing": "runtime",
                "utility_preservation": True,
                "defense_cost": "low reported utility drop",
                "temporal_adaptation": False,
                "evaluation_protocol": "ASR and utility",
                "novel_evolving_eval": False,
            },
            "overlap_class": "ADJACENT",
            "overlap_explanation": {
                "paper_mechanism": "Semantic privilege separation with self-correction.",
                "adapti_guard_mechanism": "Discrete defense levels with SUC feedback.",
                "shared": ["runtime agent defense", "utility preservation"],
                "differing": ["no AG-style level transitions / SUC protocol"],
            },
        },
        {
            "paper_id": "P13_SHE",
            "title": "SHE: Trajectory-driven Safety Harness Evolution for LLM Agents",
            "arxiv": "2608.09885",
            "source_group": "05_2025_2026_proxy",
            "source_uri": "https://arxiv.org/abs/2608.09885",
            "profile": {
                "threat_model": "agent safety failures beyond single-turn moderation",
                "attack_setting": "trajectory-based harness evolution settings",
                "defense_mechanism": "evolvable safety harness artifacts",
                "adaptive_mechanism": "trajectory-driven harness evolution",
                "memory_history": "trajectory feedback",
                "feedback_signal": "failure trajectories",
                "adaptation_timing": "offline_evolution",
                "utility_preservation": True,
                "defense_cost": "not AG discrete cost levels",
                "temporal_adaptation": "evolution iterations",
                "evaluation_protocol": "harness evolution experiments",
                "novel_evolving_eval": "partial",
            },
            "overlap_class": "PARTIAL_OVERLAP",
            "overlap_explanation": {
                "paper_mechanism": "Evolve safety harness from trajectories.",
                "adapti_guard_mechanism": "Within-run defense-level policy transitions.",
                "shared": ["adaptation from experience", "runtime harness/defense view"],
                "differing": ["SHE evolves artifacts across iterations; AG transitions levels online"],
            },
        },
        {
            "paper_id": "P14_AgentDojo",
            "title": "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents",
            "arxiv": "2406.13352",
            "source_group": "01_CORE_proxy",
            "source_uri": "https://arxiv.org/abs/2406.13352",
            "profile": {
                "threat_model": "prompt injection in tool-using agents",
                "attack_setting": "dynamic agent environment benchmark",
                "defense_mechanism": "benchmark (hosts defenses)",
                "adaptive_mechanism": "n/a",
                "memory_history": "n/a",
                "feedback_signal": "n/a",
                "adaptation_timing": "n/a",
                "utility_preservation": "utility under attack is a core metric",
                "defense_cost": "n/a",
                "temporal_adaptation": "n/a",
                "evaluation_protocol": "security + utility under attack",
                "novel_evolving_eval": False,
            },
            "overlap_class": "COMPLEMENTARY",
            "overlap_explanation": {
                "paper_mechanism": "Evaluation environment for attacks/defenses.",
                "adapti_guard_mechanism": "Custom controlled 75/25 protocol + analyses.",
                "shared": ["need to measure security and utility together"],
                "differing": ["AG does not use AgentDojo as primary protocol"],
            },
        },
        {
            "paper_id": "P15_GreshakeIPI",
            "title": "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection",
            "arxiv": "2302.12173",
            "source_group": "01_CORE_proxy",
            "source_uri": "https://arxiv.org/abs/2302.12173",
            "profile": {
                "threat_model": "indirect prompt injection",
                "attack_setting": "LLM-integrated applications",
                "defense_mechanism": "attack paper",
                "adaptive_mechanism": "n/a",
                "memory_history": "n/a",
                "feedback_signal": "n/a",
                "adaptation_timing": "n/a",
                "utility_preservation": "n/a",
                "defense_cost": "n/a",
                "temporal_adaptation": "n/a",
                "evaluation_protocol": "attack demonstrations",
                "novel_evolving_eval": False,
            },
            "overlap_class": "NO_MATERIAL_OVERLAP",
            "overlap_explanation": {
                "paper_mechanism": "Foundational attack/threat exposition.",
                "adapti_guard_mechanism": "Defense system.",
                "shared": ["threat domain"],
                "differing": ["not a defense method"],
            },
        },
    ]

    # Deduplicate by arxiv id
    seen = set()
    unique = []
    for p in papers:
        key = p.get("arxiv") or p["title"]
        if key in seen:
            continue
        seen.add(key)
        unique.append(p)

    by_class = {
        "DIRECT_OVERLAP": [],
        "PARTIAL_OVERLAP": [],
        "ADJACENT": [],
        "COMPLEMENTARY": [],
        "NO_MATERIAL_OVERLAP": [],
    }
    for p in unique:
        by_class[p["overlap_class"]].append(
            {
                "paper_id": p["paper_id"],
                "title": p["title"],
                "arxiv": p.get("arxiv"),
                "overlap_explanation": p.get("overlap_explanation"),
            }
        )

    critical = {
        "AgentAntibody": next(p for p in unique if p["paper_id"] == "P01_AgentAntibody"),
        "COPA": next(p for p in unique if p["paper_id"] == "P02_COPA"),
        "Beyond_Handcrafted_HARD": next(
            p for p in unique if p["paper_id"] == "P03_BeyondHandcrafted_HARD"
        ),
        "SecOPD": next(p for p in unique if p["paper_id"] == "P04_SecOPD"),
        "Adaptive_Adversaries": next(
            p for p in unique if p["paper_id"] == "P05_AdaptiveAdversaries"
        ),
        "SCOUT": next(p for p in unique if p["paper_id"] == "P06_SCOUT"),
    }

    critical_summary = {}
    for name, p in critical.items():
        critical_summary[name] = {
            "overlap_class": p["overlap_class"],
            "one_line": p["overlap_explanation"]["paper_mechanism"],
            "vs_adapti_guard": p["overlap_explanation"]["adapti_guard_mechanism"],
            "checklist_A_to_G": p["checklist_A_to_G"],
        }

    # Phase 10 claim repair under novelty pressure (do not edit Phase 10 file)
    claim_repair = [
        {
            "claim_id": "C1",
            "phase10_status": "SUPPORTED",
            "novelty_status": "SUPPORTED_EMPIRICALLY_BUT_NOT_UNIQUE",
            "status_for_paper": "SUPPORTED",
            "risk": "Empirical transitions remain supported in AG artifacts, but discrete runtime level change is no longer novel given SafeHarness.",
            "safe_wording": "Under the controlled protocol, ADAPTI-GUARD changed defense levels over time, including escalation and de-escalation.",
            "unsafe_wording": "We introduce the first runtime defense that adapts its protection level over time.",
        },
        {
            "claim_id": "C2",
            "phase10_status": "PARTIALLY SUPPORTED",
            "novelty_status": "PARTIAL",
            "status_for_paper": "PARTIALLY SUPPORTED",
            "risk": "Security gains are protocol-specific; many stronger runtime/model defenses exist.",
            "safe_wording": "On the evaluated known-attack protocol, adaptive levels reduced ASR relative to Fixed-L0 while leaving residual ASR.",
            "unsafe_wording": "ADAPTI-GUARD provides strong/general prompt-injection security.",
        },
        {
            "claim_id": "C3",
            "phase10_status": "SUPPORTED",
            "novelty_status": "SUPPORTED_EMPIRICALLY_COMMON_GOAL",
            "status_for_paper": "SUPPORTED",
            "risk": "Utility preservation is widely claimed (AgentAntibody, HARD, SCOUT, SafeHarness, SecOPD).",
            "safe_wording": "Under the controlled protocol, adaptive defense preserved utility on legitimate episodes while Fixed-L3 collapsed utility.",
            "unsafe_wording": "Unlike prior defenses, ADAPTI-GUARD uniquely preserves utility.",
        },
        {
            "claim_id": "C4",
            "phase10_status": "SUPPORTED",
            "novelty_status": "PARTIAL",
            "status_for_paper": "SUPPORTED",
            "risk": "Security–utility–cost/latency frontiers are also central to SCOUT and security–utility to HARD/SafeHarness; AG's specific SUC+Pareto vs fixed levels remains a contribution but not a unique idea class.",
            "safe_wording": "ADAPTI-GUARD exhibits a measurable security–utility–cost operating point versus fixed levels under the evaluated protocol.",
            "unsafe_wording": "We are the first to jointly optimize security, utility, and defense cost.",
        },
        {
            "claim_id": "C5",
            "phase10_status": "PARTIALLY SUPPORTED",
            "novelty_status": "PARTIAL",
            "status_for_paper": "PARTIALLY SUPPORTED",
            "risk": "Beyond-fixed-baseline adaptation is also demonstrated by SafeHarness degradation and SCOUT allocation.",
            "safe_wording": "Relative to fixed AG levels, the adaptive controller provides a distinct tradeoff point on this protocol, without claiming absolute metric dominance.",
            "unsafe_wording": "Adaptation uniquely contributes beyond any fixed defense.",
        },
        {
            "claim_id": "C6",
            "phase10_status": "NOT SUPPORTED",
            "novelty_status": "NOT SUPPORTED",
            "status_for_paper": "NOT SUPPORTED",
            "risk": "Historical contribution is empirically null in AG ablation; literature (AgentAntibody/SCOUT/SafeHarness) shows history can matter elsewhere—do not claim AG historical feedback helps.",
            "safe_wording": None,
            "paper_handling": "NOT ESTABLISHED / limitation: under this protocol, historical signal did not change aggregates.",
            "unsafe_wording": "Historical attack feedback improves adaptive performance.",
        },
        {
            "claim_id": "C7",
            "phase10_status": "SUPPORTED",
            "novelty_status": "SUPPORTED_EMPIRICALLY_DESCRIPTIVE",
            "status_for_paper": "SUPPORTED",
            "risk": "Family heterogeneity is descriptive; not a novelty pillar.",
            "safe_wording": "On the known Adaptive run, ASR differed across the four frozen attack families.",
            "unsafe_wording": "ADAPTI-GUARD uniquely characterizes attack-family robustness.",
        },
        {
            "claim_id": "C8",
            "phase10_status": "LIMITED",
            "novelty_status": "LIMITED",
            "status_for_paper": "LIMITED",
            "risk": "Novel-set results remain set-specific; AgentAntibody/HARD/SecOPD make stronger transfer claims in their settings.",
            "safe_wording": "On the evaluated structurally novel set, outcomes are measurable but do not establish open-world generalization.",
            "unsafe_wording": "ADAPTI-GUARD generalizes to unseen attacks.",
        },
        {
            "claim_id": "C9",
            "phase10_status": "PARTIALLY SUPPORTED",
            "novelty_status": "PARTIAL",
            "status_for_paper": "PARTIALLY SUPPORTED",
            "risk": "COPA/HARD/AgentAntibody/Adaptive Adversaries address evolving threats more directly; AG shows response on a constructed stream, not broad evolving robustness.",
            "safe_wording": "Under the constructed evolving stream, defense-level change across stages was observed; this is response evidence, not uniformly successful evolving-attack defense.",
            "unsafe_wording": "ADAPTI-GUARD robustly defends against evolving adaptive adversaries.",
        },
        {
            "claim_id": "C10",
            "phase10_status": "SUPPORTED",
            "novelty_status": "SUPPORTED_EMPIRICALLY_NOT_NOVELTY",
            "status_for_paper": "SUPPORTED",
            "risk": "Reproducibility of a deterministic pipeline is not a scientific novelty claim.",
            "safe_wording": "Under identical settings, multi-seed aggregates reproduced exactly (std=0), indicating pipeline reproducibility.",
            "unsafe_wording": "Multi-seed results demonstrate stochastic robustness.",
        },
    ]

    audit = {
        "analysis": "novelty_audit",
        "version": "v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "corpus_status": {
            "requested_local_groups": [
                "01_CORE/",
                "02_AGENT_SECURITY/",
                "03_DEFENSE/",
                "04_BACKGROUND/",
                "05_2025_2026/",
                "07_VERIFIED_AGENT_PAPERS/",
                "supporting/",
            ],
            "local_corpus_present": False,
            "inventory_basis": (
                "Public arXiv/HTML retrieval of named critical papers plus "
                "adjacent publicly identified papers required for a non-optimistic novelty check. "
                "Local PDF folders were missing in the cloud workspace; no local PDFs were deleted or moved."
            ),
            "limitation": (
                "This audit is NOT a complete inventory of the user's private literature folders. "
                "If those folders contain additional direct-overlap systems, novelty may be weaker."
            ),
        },
        "adapti_guard_profile": {
            "runtime_adaptive_defense": True,
            "explicit_defense_levels": "L0-L3",
            "policy_based_escalation_deescalation": True,
            "utility_aware_feedback": True,
            "historical_signal": "implemented_but_C6_NOT_SUPPORTED",
            "defense_transitions": True,
            "security_utility_cost_evaluation": True,
            "controlled_mixed_75_25_protocol": True,
            "multiseed_evaluation": True,
            "temporal_analysis": True,
            "attack_family_analysis": True,
            "novel_evolving_attack_evaluation": True,
            "phase10_boundary": "results/phase10/claim_evidence_matrix_v1.json",
        },
        "unique_papers": unique,
        "unique_paper_count": len(unique),
        "direct_overlaps": by_class["DIRECT_OVERLAP"],
        "partial_overlaps": by_class["PARTIAL_OVERLAP"],
        "adjacent_work": by_class["ADJACENT"],
        "complementary_work": by_class["COMPLEMENTARY"],
        "no_material_overlap": by_class["NO_MATERIAL_OVERLAP"],
        "critical_papers": critical_summary,
        "not_novel_anymore": [
            "Runtime adaptive defense against prompt injection in general",
            "History/memory-conditioned runtime defense (AgentAntibody, SCOUT fingerprints, SafeHarness windows)",
            "Security–utility tradeoff as an evaluation objective (widely studied)",
            "Explicit escalate/de-escalate multi-level runtime defense intensity/privilege (SafeHarness degradation levels)",
            "Adaptation under evolving attack curricula (COPA training-time; HARD evolution; AgentAntibody cumulative learning)",
            "Claim that AG historical feedback contributes (already empirically NOT SUPPORTED)",
        ],
        "adapti_guard_unique_contributions": [
            "Within this audited set: a controlled 75/25 mixed attack/legitimate protocol with multi-seed, temporal, family, novel/evolving, SUC/Pareto, and statistical packaging focused on discrete detect/sanitize defense levels L0–L3.",
            "Explicit comparison of an adaptive level controller against fixed level baselines under a unified ASR/utility/defense-cost/reward accounting in that protocol.",
            "These are primarily methodological/systems-evaluation contributions; they are weaker as algorithmic novelty once SafeHarness-level escalate/de-escalate is acknowledged.",
        ],
        "engineering_combination_risk": (
            "Combining known pieces (runtime guards + level-like intensity + utility feedback + history) "
            "without a stronger differentiating mechanism risks reading as an engineering combination. "
            "AG's strongest differentiator in this audit is the controlled evaluation package around discrete costed levels, not uniqueness of adaptation itself."
        ),
        "safe_claims": [
            c["safe_wording"]
            for c in claim_repair
            if c.get("safe_wording")
        ],
        "unsupported_claims": [
            "Historical attack feedback contributes to AG adaptation (C6).",
            "Open-world generalization to unseen attacks.",
            "First / unique runtime multi-level escalate/de-escalate defense.",
            "First joint security–utility–cost adaptive defense.",
            "Uniformly successful evolving-attack robustness.",
            "Stochastic multi-seed robustness (std=0 is reproducibility).",
        ],
        "claim_repair": claim_repair,
        "limitations": [
            "Local literature folders were absent; audit uses public proxies for named papers + discovered strong-overlap SafeHarness.",
            "Phase 10 empirical claim statuses are preserved; this audit adds novelty pressure, not new experimental results.",
            "MVP detector/outcome heuristics limit external validity of AG claims regardless of literature novelty.",
            "Generalization remains LIMITED per Phase 10.",
            "C6 remains NOT SUPPORTED.",
        ],
        "overall_novelty": "WEAK",
        "overall_novelty_rationale": (
            "Named critical papers create partial overlaps on runtime adaptation, history, evolving attacks, "
            "and safety–utility frontiers. SafeHarness provides DIRECT_OVERLAP on discrete runtime escalate/"
            "de-escalate levels with utility-aware recovery, removing uniqueness from ADAPTI-GUARD's core "
            "adaptive principle. Remaining differentiators are mainly controlled-protocol packaging and "
            "detect/sanitize-level cost accounting—closer to an engineering/evaluation combination than a "
            "strong algorithmic novelty claim. Local corpus absence may hide additional overlaps."
        ),
        "verdict": "CLAIMS REQUIRE REVISION",
        "integrity": {
            "source_code_modified": False,
            "phase7_modified": False,
            "phase8_modified": False,
            "phase9_modified": False,
            "phase10_modified": False,
            "experiments_rerun": False,
            "papers_deleted_or_moved": False,
            "fabricated_evidence": False,
            "local_corpus_inventoried": False,
        },
    }
    return audit


def validate(audit: dict, pre_hashes: dict) -> dict:
    checks = {}
    ids = [p["paper_id"] for p in audit["unique_papers"]]
    arxivs = [p.get("arxiv") for p in audit["unique_papers"]]
    checks["no_duplicate_paper_ids"] = len(ids) == len(set(ids))
    checks["no_duplicate_arxiv"] = len([a for a in arxivs if a]) == len(
        set(a for a in arxivs if a)
    )
    critical_names = {
        "AgentAntibody",
        "COPA",
        "Beyond_Handcrafted_HARD",
        "SecOPD",
        "Adaptive_Adversaries",
        "SCOUT",
    }
    checks["all_critical_papers_included"] = critical_names.issubset(
        set(audit["critical_papers"].keys())
    )
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--", *PRIOR_PATHS],
        capture_output=True,
        text=True,
    ).stdout.strip()
    checks["no_phase7_11_or_src_modified"] = dirty == ""
    # hash check for tracked result files if present
    hash_ok = True
    for p, h in pre_hashes.items():
        if Path(p).exists() and _sha(p) != h:
            hash_ok = False
    checks["prior_result_hashes_unchanged"] = hash_ok
    checks["c6_remains_not_supported"] = any(
        c["claim_id"] == "C6" and c["status_for_paper"] == "NOT SUPPORTED"
        for c in audit["claim_repair"]
    )
    checks["generalization_not_upgraded"] = any(
        c["claim_id"] == "C8" and c["status_for_paper"] == "LIMITED"
        for c in audit["claim_repair"]
    )
    checks["direct_overlap_acknowledged"] = len(audit["direct_overlaps"]) >= 1
    checks["overall_novelty_not_overclaimed"] = audit["overall_novelty"] in {
        "MODERATE",
        "WEAK",
        "UNCLEAR",
    }
    checks["local_corpus_absence_documented"] = (
        audit["corpus_status"]["local_corpus_present"] is False
    )

    report = {k: ("PASS" if v else "FAIL") for k, v in checks.items()}
    fails = [k for k, v in checks.items() if not v]
    return {
        "checks": checks,
        "report": report,
        "fail_count": len(fails),
        "root_causes": fails,
        "overall": "NOVELTY AUDIT VALIDATED" if not fails else "NOVELTY AUDIT INVALID",
    }


def render_txt(audit: dict, validation: dict) -> str:
    lines = []
    lines.append("ADAPTI-GUARD — NOVELTY AUDIT v1")
    lines.append("=" * 60)
    lines.append(f"timestamp_utc: {audit['timestamp_utc']}")
    lines.append(
        f"local_corpus_present: {audit['corpus_status']['local_corpus_present']}"
    )
    lines.append(f"unique_papers: {audit['unique_paper_count']}")
    lines.append(f"direct_overlap: {len(audit['direct_overlaps'])}")
    lines.append(f"partial_overlap: {len(audit['partial_overlaps'])}")
    lines.append(f"adjacent: {len(audit['adjacent_work'])}")
    lines.append(f"complementary: {len(audit['complementary_work'])}")
    lines.append(f"no_material_overlap: {len(audit['no_material_overlap'])}")
    lines.append("")
    lines.append("CRITICAL PAPERS")
    for name, block in audit["critical_papers"].items():
        lines.append(f"- {name}: {block['overlap_class']}")
        lines.append(f"  {block['one_line']}")
    lines.append("")
    lines.append("DIRECT OVERLAP DETAIL")
    for d in audit["direct_overlaps"]:
        lines.append(f"- {d['title']}")
        lines.append(f"  paper: {d['overlap_explanation']['paper_mechanism']}")
        lines.append(f"  AG:    {d['overlap_explanation']['adapti_guard_mechanism']}")
    lines.append("")
    lines.append("REMAINING NOVELTY")
    for i, x in enumerate(audit["adapti_guard_unique_contributions"], 1):
        lines.append(f"{i}. {x}")
    lines.append("")
    lines.append("NOT NOVEL ANYMORE")
    for x in audit["not_novel_anymore"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("UNSUPPORTED / DISALLOWED CLAIMS")
    for x in audit["unsupported_claims"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("CLAIM REPAIR")
    for c in audit["claim_repair"]:
        lines.append(
            f"{c['claim_id']} phase10={c['phase10_status']} paper_status={c['status_for_paper']}"
        )
        if c.get("safe_wording"):
            lines.append(f"  SAFE: {c['safe_wording']}")
        if c.get("paper_handling"):
            lines.append(f"  HANDLE: {c['paper_handling']}")
        lines.append(f"  UNSAFE: {c['unsafe_wording']}")
    lines.append("")
    lines.append(f"OVERALL NOVELTY: {audit['overall_novelty']}")
    lines.append(f"VERDICT: {audit['verdict']}")
    lines.append("")
    lines.append("VALIDATION")
    for k, v in validation["report"].items():
        lines.append(f"  {k}: {v}")
    lines.append(f"validation_overall: {validation['overall']}")
    return "\n".join(lines) + "\n"


def main():
    Path("ANALYSIS").mkdir(parents=True, exist_ok=True)
    if OUT_JSON.exists() or OUT_TXT.exists():
        print("exists (not overwritten)", OUT_JSON if OUT_JSON.exists() else OUT_TXT)
        return

    pre = {}
    for p in [
        "results/phase7/adaptive_100_v2.json",
        "results/phase7/fixed_baselines_100_v2.json",
        "results/phase8/multiseed_summary.json",
        "results/phase8/ablation_v1.json",
        "results/phase10/claim_evidence_matrix_v1.json",
        "results/phase11/manuscript_evidence_package_v1.json",
    ]:
        if Path(p).exists():
            pre[p] = _sha(p)

    audit = build()
    validation = validate(audit, pre)
    audit["validation"] = validation

    OUT_JSON.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    OUT_TXT.write_text(render_txt(audit, validation), encoding="utf-8")
    print("wrote", OUT_JSON)
    print("wrote", OUT_TXT)
    print("unique_papers", audit["unique_paper_count"])
    print("direct", len(audit["direct_overlaps"]))
    print("partial", len(audit["partial_overlaps"]))
    print("adjacent", len(audit["adjacent_work"]))
    print("overall_novelty", audit["overall_novelty"])
    print("verdict", audit["verdict"])
    print("validation", validation["overall"])
    for k, v in validation["report"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
