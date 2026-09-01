# Q1 Improvement Tracker

**Project:** ADAPTI-GUARD  
**Baseline score:** 3.5 / 10 (research prototype)  
**Target score:** 7–8 / 10 (scientifically validated framework)  
**Last updated:** 2026-09-01

---

## Score summary

| Dimension | Before | Current | Target |
|-----------|-------:|--------:|-------:|
| Real LLM evaluation | 2 | 4 | 8 |
| Dataset quality | 2 | 3 | 7 |
| Baselines | 1 | 4 | 8 |
| Adaptive controller science | 3 | 5 | 7 |
| Detector architecture | 3 | 5 | 7 |
| RAG security eval | 0 | 5 | 7 |
| Agent security eval | 0 | 5 | 7 |
| Statistical validation | 1 | 5 | 8 |
| Reproducibility | 4 | 6 | 8 |
| Manuscript readiness | 2 | 4 | 7 |
| **Overall** | **3.5** | **4.5** | **7–8** |

---

## Improvement registry

| ID | Phase | Improvement | Priority | Scientific impact | Status |
|----|-------|-------------|----------|-------------------|--------|
| I-001 | 0 | Q1 gap analysis tracker | P0 | Enables audit trail | DONE |
| I-002 | 1 | Real LLM pipeline (defense→target→judge) | P0 | Core validity | IMPLEMENTED |
| I-003 | 1 | Multi-provider target models (OpenRouter/Ollama) | P0 | Reproducibility | IMPLEMENTED |
| I-004 | 1 | Independent LLM judge (6-field verdict) | P0 | Removes circular ASR | IMPLEMENTED |
| I-005 | 1 | EXP002 execution with logs | P0 | Publication evidence | BLOCKED (no API key) |
| I-006 | 2 | benchmark_v4 dataset builder | P0 | Fair evaluation | DONE (smoke) |
| I-007 | 2 | Dataset provenance + SHA256 hashes | P0 | Reproducibility | DONE |
| I-008 | 2 | External dataset integration (NotInject/BIPIA) | P0 | Publication scale | BLOCKED |
| I-009 | 2 | DATASET_QUALITY_REPORT.md | P1 | Reviewer transparency | DONE |
| I-010 | 3 | Unified baseline comparison framework | P0 | SOTA comparison | IMPLEMENTED |
| I-011 | 3 | No Defense + Regex + ADAPTI-GUARD baselines | P0 | Minimum baselines | IMPLEMENTED |
| I-012 | 3 | Llama Guard / Prompt Guard / NeMo adapters | P1 | Full SOTA | PARTIAL |
| I-013 | 3 | EXP003 baseline_comparison.csv | P0 | Results table | PARTIAL |
| I-014 | 4 | RuleBasedController | P1 | Baseline adaptive | IMPLEMENTED |
| I-015 | 4 | BayesianRiskController | P1 | Novelty candidate | IMPLEMENTED |
| I-016 | 4 | ContextAwareController | P1 | Cost-utility tradeoff | IMPLEMENTED |
| I-017 | 4 | ADAPTIVE_MODEL.md formalization | P1 | Theory section | DONE |
| I-018 | 4 | EXP004 controller comparison | P1 | Empirical validation | DONE (simulation) |
| I-019 | 5 | Hybrid detector (regex+ML+LLM) | P1 | Architecture upgrade | IMPLEMENTED |
| I-020 | 5 | ML detector (TF-IDF + optional transformers) | P1 | ML baseline | IMPLEMENTED |
| I-021 | 5 | LLM safety scorer detector | P2 | High-cost defense | IMPLEMENTED |
| I-022 | 5 | Detector metrics (F1/AUROC/AUPRC) | P1 | Classifier eval | DONE (smoke) |
| I-023 | 6 | RAG environment (embed→retrieve→LLM) | P1 | RAG threat model | IMPLEMENTED |
| I-024 | 6 | EXP005 RAG security | P1 | RAG ASR evidence | DONE (offline) |
| I-025 | 7 | Agent environment (planner→tools→memory) | P1 | Agent threat model | IMPLEMENTED |
| I-026 | 7 | EXP006 agent security | P1 | Agent ASR evidence | DONE (offline) |
| I-027 | 8 | Bootstrap CI + McNemar + Wilcoxon | P0 | Statistical rigor | IMPLEMENTED |
| I-028 | 8 | Multi-seed runner (≥5 seeds) | P0 | Variance reporting | IMPLEMENTED |
| I-029 | 8 | STATISTICAL_REPORT.md | P1 | Methods section | DONE |
| I-030 | 9 | EXP007 ablation study | P1 | Component analysis | DONE (simulation) |
| I-031 | 10 | requirements-lock.txt + environment.yml | P1 | Reproducibility | DONE |
| I-032 | 10 | Dockerfile + run_all_experiments.sh | P1 | One-command repro | DONE |
| I-033 | 10 | Provenance in every experiment artifact | P0 | Audit trail | IMPLEMENTED |
| I-034 | 11 | MANUSCRIPT_UPGRADE_PLAN.md | P2 | Paper structure | DONE |
| I-035 | 11 | Q1_FINAL_READINESS_REPORT.md | P0 | Final assessment | DONE |
| I-036 | — | Legacy simulation labeled LEGACY_SIMULATION_ONLY | P0 | Honest claims | DONE |
| I-037 | — | Human judge audit | P2 | External validity | NOT_PERFORMED |

---

## Remaining weaknesses (P0)

1. **No executed real-LLM results at publication scale** — EXP002 BLOCKED without `OPENROUTER_API_KEY`
2. **benchmark_v4 is smoke-only** — external datasets not present in clone
3. **SOTA baselines (Llama Guard, NeMo) not fully integrated** — adapters exist, execution BLOCKED
4. **Human judge correlation audit** — NOT_PERFORMED
5. **Multi-model EXP002 (3 targets × ≥500 samples)** — NOT_RUN

---

## Experiment status

| Experiment | Description | Status | Evidence path |
|------------|-------------|--------|---------------|
| EXP000 | API smoke test | BLOCKED | `results/EXP000_api_smoke/` |
| EXP001 | Dataset analysis | PARTIAL | `results/EXP001_dataset_analysis/` |
| EXP002 | Real LLM evaluation | BLOCKED | `results/EXP002/` |
| EXP003 | Baseline comparison | PARTIAL | `results/baseline_comparison.csv` |
| EXP004 | Adaptive controller | DONE (sim) | `results/EXP004_adaptive_controller/` |
| EXP005 | RAG security | DONE (offline) | `results/EXP005_rag_security/` |
| EXP006 | Agent security | DONE (offline) | `results/EXP006_agent_security/` |
| EXP007 | Ablation study | DONE (sim) | `results/EXP007_ablation/` |

---

## Critical path to 7/10

1. Set `OPENROUTER_API_KEY` → PASS EXP000 → RUN EXP002 (≥500 test × 3 models)
2. Place NotInject/BIPIA under `dataset/` → rebuild benchmark_v4 with `publication_ready: true`
3. Execute EXP003 with all baselines sharing judge + dataset
4. Run EXP004/007 with real judge (not simulation only)
5. Human judge audit on 100-sample subset
