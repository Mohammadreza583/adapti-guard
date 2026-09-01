# Q1 Scientific Upgrade Changelog

## 2026-09-01

### Added
- Real LLM evaluation pipeline (`target_model.py`, `llm_judge.py`, `real_llm_pipeline.py`)
- Independent judge (no detector rules)
- Experiment logging (`experiment_logging.py`, `experiment_logger.py`)
- benchmark_v3 dataset builder
- Adaptive controllers (rule, Bayesian, context-aware)
- Statistics module (bootstrap, McNemar, Wilcoxon)
- Detectors/evaluators/controllers package structure
- EXP000–EXP002 experiment runners + EXP003–008 stubs
- Reproducibility: Dockerfile, environment.yml, run_all_experiments.sh
- Documentation: Q1_RESEARCH_AUDIT, Q1_FINAL_READINESS_REPORT, etc.

### Changed
- `attack_outcome.py` marked LEGACY_SIMULATION_ONLY
- `DefensePipeline` alias restored in pipeline.py
- Extended metrics (latency, tokens, ASR CI)
- artifact_standard.py project root path fixed

### Scientific impact
- Enables judge-based ASR; no publication results executed in automation environment

### Validation
- 81 unit tests pass (2 skipped)
- EXP001: PARTIAL (smoke benchmark)
- EXP004/EXP005/EXP006/EXP007: DONE (simulation or offline mock LLM)
- EXP000/EXP002/EXP003: BLOCKED without OPENROUTER_API_KEY

## Q1 Enhancement Mission (2026-09-01)

### Added
- `docs/Q1_IMPROVEMENT_TRACKER.md` — phase-by-phase gap tracking
- `datasets/benchmark_v4/` builder with 7-category smoke coverage
- Baseline comparison framework (6 defenses) + EXP003 runner
- Hybrid detector (regex + ML + optional LLM)
- Real RAG (EXP005) and agent (EXP006) evaluation environments
- Multi-seed statistical validation (5 seeds, bootstrap CI)
- EXP004/EXP007 adaptive controller ablations
- `docs/MANUSCRIPT_UPGRADE_PLAN.md`, `DATASET_QUALITY_REPORT.md`, `STATISTICAL_REPORT.md`
- `requirements-lock.txt`

### Readiness score
- Updated: 3.5 → **4.5 / 10** (target 7–8 not achieved)
