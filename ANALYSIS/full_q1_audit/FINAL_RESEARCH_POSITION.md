# FINAL_RESEARCH_POSITION

## Decision: **B — MINOR PIVOT**

### 1. Why

A defensible contribution remains if reframed away from "unique adaptive defense / unique discrete levels" toward a **controlled security–utility–cost study of discrete intervention-level policies with attack-triggered escalation and legitimate-task cost-triggered de-escalation under mixed workloads**. SafeHarness blocks DIRECT uniqueness of escalate/de-escalate levels, but does not fully cover AG’s intervention semantics + fixed-level SUC protocol + legitimate-cost de-escalation package. Corpus incompleteness raises positioning risk but does not by itself force redesign of the controller.

Not A: current uniqueness framing is not Q1-safe.  
Not C/D: core L0–L3 controller need not be discarded; gap is ablation + adaptive-attacker eval + claim rewrite.

### 2. What must change

- Claim language (remove first/unique/SOTA; position vs SafeHarness/SCOUT/HARD/COPA/AutoDojo)
- Add escalate-only ablation
- If keeping evolving-robustness claims: AutoDojo-like adaptive attacker evaluation
- Prefer baseline vs privilege-degradation adaptive levels
- Ingest full TOTAL-- for camera-ready lit review

### 3. What must NOT change

- Frozen Phase7–10 artifacts / metrics / 75/25 stream (evidence boundary)
- Discrete L0–L3 intervention mapping as object of study
- Honest C6 NOT_SUPPORTED / LIMITED generalization

### 4. Strongest defensible contribution

Controlled evaluation of a discrete runtime intervention-level policy (sanitize/restrict/block) that escalates on attack success and de-escalates on legitimate-task utility/cost feedback, versus fixed levels, under a mixed attack/legitimate workload with explicit security, utility, and defense-cost metrics.

### 5. Strongest defensible research question

Does legitimate-task cost-triggered de-escalation improve the security–utility–cost frontier of discrete intervention levels relative to fixed levels and escalate-only policies under mixed workloads, and does any advantage survive adaptive black-box attacks?

### 6. Minimum experiments needed

1. Fixed L0–L3 (have)  
2. Full adaptive with de-escalation (have)  
3. Escalate-only ablation (need)  
4. Mixed 75/25 (have)  
5. SUC/Pareto (have)  
6. Adaptive/black-box attacker eval (need for evolving claims)  
7. Optional HIGH-VALUE: vs SafeHarness-style levels; legitimate-heavy workload

### 7. Claims that must be removed

- First/unique runtime multi-level adaptive defense
- Historical signal contributes (C6)
- Open-world novel-attack generalization
- Strong evolving-adversary robustness without AutoDojo-class eval
- Unified community evaluation framework novelty
- Stochastic multi-seed robustness (std=0)

### 8. Claims that can remain

- AG implements discrete L0–L3 interventions with runtime escalate/de-escalate under stated rules
- Under 75/25 protocol, adaptive yields a measured SUC operating point vs fixed levels (utility preserved vs Fixed-L3)
- De-escalation events occur and are tied to legitimate-task/cost feedback in this system
- Historical signal ablation is null under current protocol
- Results are pipeline-reproducible

## Gap test (requested combination)

Combination: discrete runtime intervention levels + attack escalation + legitimate cost/utility de-escalation + mixed workloads + SUC eval + adaptive attacker

| Component | Covered by prior? | Who |
|-----------|-------------------|-----|
| Discrete runtime levels | YES | SafeHarness (privilege 0–4) |
| Attack-triggered escalation | YES | SafeHarness; SCOUT (to judge) |
| Legitimate-task cost/utility de-escalation | PARTIAL | SafeHarness recovers after safe window (not AG cost≥ thresholds on legitimate schedule) |
| Mixed attack/legitimate workload SUC vs fixed levels | NOT EVIDENCED in compared set as AG protocol | — AG differentiator |
| Adaptive attacker evaluation | YES as method | AutoDojo / Adaptive Adversaries — **AG lacks this as primary** |

**Narrow gap that remains:** mixed-workload SUC evaluation of intervention-level policies with legitimate-cost de-escalation vs fixed and escalate-only — **contingent on not claiming level adaptation writ large**.

## Q1 risk

**HIGH** (CRITICAL if uniqueness claims retained or TOTAL-- never ingested for positioning).
