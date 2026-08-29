# Novelty Claims v2

Generated: 2026-08-29T15:36:31.416191+00:00
Basis: Phase11 audit + implementation + Phase7–10 evidence. No new unsupported claims.

## Combination under test

`L0–L3 policy + adaptive escalation + cost-aware de-escalation + mixed workload + fixed-level comparison + adaptive-attacker evaluation`

| Component | Status | Evidence |
| --------- | ------ | -------- |
| Discrete L0–L3 intervention policy (sanitize/restrict/block) | **PARTIAL** | Implemented; SafeHarness has discrete levels with different semantics (privilege 0–4) |
| Adaptive escalation on attack success | **PARTIAL** | Implemented + Phase7 ↑14; SafeHarness/SCOUT also escalate |
| Cost-aware de-escalation on legitimate + cost thresholds | **PARTIAL** | Implemented + Phase7 ↓11; SafeHarness recovers via safe-window (different trigger) |
| Mixed workload protocol | **PARTIAL** | Present as **75% attack / 25% legitimate** (not 75% legit). Protocol itself is AG-specific packaging |
| Fixed-level comparison under unified SUC | **UNIQUE*** | Phase7/8 Fixed L0–L3 vs Adaptive; *provisional — TOTAL-- TXT absent |
| Adaptive-attacker evaluation (AutoDojo-class) | **UNSUPPORTED** as AG primary result | `AdaptiveAttacker` exists but Phase7/8 primary uses frozen stream; observe() skipped when stream set |

## System + Policy + Evaluation novelty (not “a defense”)

| Layer | Verdict |
| ----- | ------- |
| System (MVP detector/action heuristics) | KNOWN / engineering integration |
| Policy (discrete escalate + cost-aware de-escalate) | PARTIAL vs SafeHarness |
| Evaluation (mixed fixed-vs-adaptive SUC) | UNIQUE* among audited set (provisional) |
| Adaptive-attacker robustness claim | UNSUPPORTED / must weaken wording |

## Allowed novelty statement (defensible)

> ADAPTI-GUARD studies a **discrete runtime intervention-level controller** with attack-triggered escalation and **legitimate-task cost-triggered de-escalation**, evaluated against **fixed levels** under a **mixed attack/legitimate workload** with explicit **security–utility–cost** metrics.

## Disallowed novelty statement

> First/unique adaptive multi-level defense; historical-memory contribution; open-world/AutoDojo-robust adaptive defense.

## Research gap (bounded)

Full combination including AutoDojo-class adaptive attacker eval is **not** demonstrated by AG and not fully present as one prior package in the audited corpus. Do not overclaim the gap beyond audited evidence.
