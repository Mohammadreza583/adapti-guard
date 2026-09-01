# Statistical Validation Report

**Date:** 2026-09-01  
**Status:** Framework implemented; applied to offline experiments

---

## Methods implemented

| Method | Module | Used in |
|--------|--------|---------|
| Bootstrap 95% CI | `evaluation/statistics.py` | ASR, multiseed aggregation |
| McNemar exact test | `evaluation/statistics.py` | Paired baseline comparison |
| Wilcoxon signed-rank | `evaluation/statistics.py` | Continuous metric comparison |
| Cohen's h | `evaluation/statistics.py` | Proportion effect size |
| Cohen's d | `evaluation/statistics.py` | Continuous effect size |
| Multi-seed runner | `evaluation/multiseed.py` | EXP004–007 |

---

## Seed protocol

All multiseed experiments use **minimum 5 seeds** (`seeds = [0, 1, 2, 3, 4]`).

Reported per metric:
- Mean
- Standard deviation (ddof=1)
- 95% bootstrap confidence interval

---

## Experiment statistical status

| Experiment | Seeds | CI reported | Significance tests | Mode |
|------------|------:|-------------|-------------------|------|
| EXP002 | — | BLOCKED | — | Real LLM (needs API) |
| EXP003 | — | BLOCKED | — | Real LLM (needs API) |
| EXP004 | 5 | yes | pending paired comparison | LEGACY_SIMULATION_ONLY |
| EXP005 | 5 | yes | — | Offline mock LLM |
| EXP006 | 5 | yes | — | Offline mock LLM |
| EXP007 | 5 | yes | pending | LEGACY_SIMULATION_ONLY |

---

## Example: EXP005 multiseed output

After running `python experiments/EXP005_rag_security/run.py`, see:

```
results/EXP005_rag_security/metrics.json → multiseed.aggregated
```

Each metric includes `mean`, `std`, `ci_95_lower`, `ci_95_upper`, `n_seeds`.

---

## Pending analyses (require EXP002/EXP003 execution)

1. McNemar test: ADAPTI-GUARD vs No Defense on paired judge verdicts
2. Wilcoxon: latency distributions across baselines
3. Cohen's h: ASR difference between defenses
4. Human judge correlation (κ) — NOT_PERFORMED

---

## Reproducibility

Every experiment artifact includes:
- `git_commit` in config.json
- `dataset_hash` where applicable
- `timestamp` (UTC)
- `random_seed` / `seeds` list

Run full pipeline:

```bash
./run_all_experiments.sh
```
