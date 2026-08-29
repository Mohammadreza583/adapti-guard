# EXPERIMENT_MANIFEST

Machine-readable companion: `EXPERIMENT_MANIFEST.json`

Provenance model: `experiment → configuration → seed → raw output → aggregation → final metric`

## Integrity
- Old Phase7–11 results: **PRESERVED** (hash-checked unchanged after Q1 runs)
- New results only under `results/q1_realign/`

## Experiment groups

### Q1-FX — Fixed vs Adaptive (frozen stream, 75% attack / 25% legitimate)
- `Q1-FX-L0..L3` → `fixed_vs_adaptive/fixed_L{0-3}.json`
- `Q1-FX-ADAPT-S{1,2,3}` → `fixed_vs_adaptive/adaptive_full_seed{s}.json` + raw episodes
- Aggregate: `fixed_vs_adaptive/summary.json`

### Q1-ABL — Ablations (frozen stream)
- `full`, `no_escalation`, `no_deescalation`, `no_cost_gate`, `no_historical`
- Per seed metrics + raw episodes
- Aggregate: `ablation/summary.json`

### Q1-ADP — AdaptiveAttacker conditions
- Live Adaptive defense seeds + fixed levels under live attacker
- Aggregate: `adaptive_attacker/summary.json`
- Claim bound: **evaluated under AdaptiveAttacker (family-switch MVP)**, not AutoDojo-class robustness

## Observed headline metrics (seed 1; std=0 across seeds)

| Condition | ASR | Legit success | Cost | Esc | De-esc |
| --------- | --- | ------------- | ---- | --- | ------ |
| Fixed L0 | 1.00 | 1.00 | 0.00 | 0 | 0 |
| Fixed L1 | 0.72 | 1.00 | 0.10 | 0 | 0 |
| Fixed L2 | 0.76 | 1.00 | 0.25 | 0 | 0 |
| Fixed L3 | 0.00 | 0.00 | 0.50 | 0 | 0 |
| Adaptive full | 0.373 | 1.00 | 0.329 | 14 | 11 |
| No escalation | 0.72 | 1.00 | 0.075 | 0 | 0 |
| No de-escalation | 0.08 | 1.00 | 0.396 | 3 | 0 |
| No cost gate | 0.40 | 1.00 | 0.303 | 15 | 12 |
| No historical | 0.373 | 1.00 | 0.329 | 14 | 11 |

Note: Adaptive util=1 at high levels can differ from Fixed-L3 util=0 because `DefensePolicyEngine` blends risk with level (LOW-risk legitimate often maps to A2 not A3 even when level is high).
