# Claim–Evidence Matrix

Evidence restricted to `results/q1_realign/` (+ `REPRODUCIBILITY.md`).  
Strength: **Strong** / **Moderate** / **Weak** / **Unsupported**.

| Claim | Evidence | Result/Table | Strength | Limitation |
| ----- | -------- | ------------ | -------- | ---------- |
| AG is a runtime discrete L0–L3 intervention policy | Methods + full adaptive transitions | Manifest; adaptive esc=14/de-esc=11 | Strong | Levels not unique vs prior discrete controllers |
| Escalation responds to attack pressure | Ablation no_escalation vs full | ASR 0.72 → 0.373; level stays 0 without escalation | Strong | Protocol-specific; MVP detector |
| De-escalation manages cost/level occupancy under legitimate-cost signals | Full vs no_deescalation trajectories | Mean cost 0.329 vs 0.396; mean level 2.43 vs 2.70; L3 attack eps 38 vs 65 | Strong as cost/level effect | Does **not** improve ASR (opposite) |
| Adaptive yields a distinct SUC point vs fixed levels | Fixed L0–L3 vs Adaptive | Adaptive ASR 0.373 util 1.0 cost 0.329 vs Fixed-L3 ASR 0 util 0 cost 0.50 | Strong | Not Pareto-best on ASR |
| Adaptive preserves legitimate utility under this protocol | Fixed vs Adaptive; ablations | util=1.0 for Adaptive/full/ablations except Fixed-L3 | Strong | Aided by risk–level blend (legit mostly A2) |
| Historical attack feedback contributes | Ablation no_historical | Identical to full (ASR/util/cost/transitions) | **Unsupported** | Must REMOVE |
| Adaptive strictly best security | Fixed-L3 ASR=0 < Adaptive 0.373 | Fixed vs Adaptive table | **Unsupported** | WEAKEN to SUC tradeoff |
| First / SOTA / uniquely adaptive | STEP2 + prior novelty audits (referenced only) | — | **Unsupported** | REMOVE |
| Open-world / novel-attack generalization | Not evidenced in q1_realign primary tables | — | **Unsupported** here | Do not claim from these runs |
| Robust against AutoDojo adaptive attackers | adaptive_attacker summary flags | `auto_dojo_class=false` | **Unsupported** | Only “evaluated under AdaptiveAttacker conditions” |
| Evaluated under AdaptiveAttacker (family-switch) | adaptive_attacker/summary.json | Live adaptive ASR 0.373 util 1.0; Fixed-L3 util 0 | Moderate | Attacker observes success/fail only |
| Cost gate matters | no_cost_gate vs full | ASR 0.40 vs 0.373; transitions 27 vs 25 | Weak–Moderate | Small effect under this protocol |
| Results reproducible across seeds 1–3 | seed aggregates std=0 | fixed_vs_adaptive & ablation summaries | Strong as determinism | Not stochastic robustness |
| Guaranteed / solves security | — | — | **Unsupported** | REMOVE |
| No de-escalation “paradox” without explanation | Raw trajectories full vs no_deesc | Higher L3 occupancy → lower ASR; util via A2 on legit | Strong observational | Causal story limited to logged level/action paths |
| Adaptive L3 ≡ Fixed L3 | Policy blend + tables | Fixed-L3 util 0; adaptive high-level util 1 | **False** | Must disclose non-isomorphism |

## Preferred paper claims (keep)

1. Discrete adaptive intervention policy under mixed workload.  
2. Escalation needed to leave under-defense; de-escalation trades ASR for lower sustained level/cost.  
3. Fixed-vs-adaptive comparison as SUC evaluation—not absolute ranking.
