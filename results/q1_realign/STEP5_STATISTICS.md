# STEP 5 — Statistics

- Seeds used for new adaptive/ablation runs: **1, 2, 3**
- Aggregation: mean ± sample std in `*/summary.json`
- **Determinism:** cross-seed std = 0 for frozen-stream adaptive/ablations
- **Interpretation rule:** `std=0` documents reproducibility of the controlled pipeline; it is **not** evidence of stochastic robustness
- Paired Fixed vs Adaptive: compare summary tables directly (same schedule/stream)
- No fabricated CIs beyond empirical seed aggregation

Primary reference tables:
- `results/q1_realign/fixed_vs_adaptive/summary.json`
- `results/q1_realign/ablation/summary.json`
- `results/q1_realign/adaptive_attacker/summary.json`
