# STEP 2 — Claim Repair

Source: Phase10 statuses + STEP1 forensics. Paper body not rewritten here.

## Classification

| Claim / phrasing | Action | Replacement / note |
| ---------------- | ------ | ------------------ |
| Adaptive defense changes over time (C1) | **KEEP** | System property; no uniqueness. |
| Meaningful security vs PI (C2) | **WEAKEN** | Protocol-local SUC; Fixed-L3 can have lower ASR with collapsed utility. |
| Preserves utility under defense (C3) | **KEEP** | Scope to mixed protocol evidence. |
| Measurable SUC tradeoff (C4) | **KEEP** | |
| Adaptation beyond fixed levels (C5) | **WEAKEN** | Distinct SUC operating point, not ASR dominance. |
| Historical attack feedback contributes (C6) | **REMOVE** | Ablation null (`historical_signal_changed_aggregates=false`). |
| Differs across attack families (C7) | **KEEP** | Descriptive. |
| Handles novel attacks / open-world (C8) | **WEAKEN** | “On evaluated novel set under controlled protocol” only. |
| Responds to evolving / adaptive attackers (C9) | **WEAKEN** | Ban “robust against adaptive attackers” until STEP4 new experiment exists; use “constructed evolving sequences” / “adaptive-attacker conditions” precisely. |
| Reproducible across seeds (C10) | **WEAKEN** | Reproducibility under determinism; not stochastic robustness (`std=0`). |
| first / SOTA / uniquely adaptive defense | **REMOVE** | SafeHarness / SCOUT / AgentAntibody block uniqueness. |
| solves / guarantees security | **REMOVE** | MVP heuristics. |

## Preferred contribution framing (use these)

1. **Adaptive discrete intervention policy** (L0–L3 → sanitize / restrict / block).
2. **Attack-pressure escalation + legitimate-cost-aware de-escalation.**
3. **Evaluation of adaptive vs fixed intervention levels under mixed workloads** (75% attack / 25% legitimate).

## Explicitly not a contribution

- Historical attack feedback / memory term in risk.
- AutoDojo-class adaptive-attacker robustness (unless STEP4 experiment lands and supports it).
