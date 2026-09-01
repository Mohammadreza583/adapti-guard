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
- 66+ unit tests pass
- EXP001: PARTIAL (smoke benchmark)
- EXP000/EXP002: BLOCKED without OPENROUTER_API_KEY
