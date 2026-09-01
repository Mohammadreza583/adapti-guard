# ADAPTI-GUARD Q1 Research Audit

**Date:** 2026-09-01  
**Git commit:** `612f577118a19949b4862a3b27b801db8c7eef65`  
**Branch:** `cursor/q1-scientific-upgrade-88b3`

---

## 1. Current architecture

### Legacy (pre-upgrade) — still present

```
Text → PromptInjectionDetector (regex) → RiskEngine → PolicyEngine
     → DefenseActionLayer → OutcomeEvaluator (LEGACY_SIMULATION_ONLY)
     → FeedbackEngine → PolicyUpdateEngine (threshold counters)
```

### Target (implemented in this upgrade)

```
Attack/Benign Prompt → ADAPTI-GUARD Defense → Target LLM → Independent LLM Judge → Metrics
```

Modules: `real_llm_pipeline.py`, `target_model.py`, `llm_judge.py`, `experiment_logging.py`

---

## 2. Existing implemented components

| Component | Status | Location |
|-----------|--------|----------|
| Regex detector | IMPLEMENTED | `detector/prompt_injection_detector.py`, `detectors/regex_detector.py` |
| Risk engine | IMPLEMENTED | `risk/risk_engine.py` |
| Policy engine L0–L3 | IMPLEMENTED | `policy/policy_engine.py` |
| Defense actions | IMPLEMENTED | `defense/action_layer.py` |
| Threshold adaptive controller | IMPLEMENTED | `adaptation/policy_update_engine.py` |
| Bayesian / context controllers | IMPLEMENTED (new, untested on data) | `controllers/adaptive_controller.py` |
| Harmonized simulation runner | IMPLEMENTED (legacy) | `experiments/harmonized_runner.py` |
| Target LLM adapters | IMPLEMENTED (new) | `evaluation/target_model.py` (OpenRouter, Ollama, mock) |
| Independent judge | IMPLEMENTED (new) | `evaluation/llm_judge.py` |
| Real E2E pipeline | IMPLEMENTED (new) | `evaluation/real_llm_pipeline.py` |
| Experiment logging | IMPLEMENTED (new) | `evaluation/experiment_logging.py` |
| Statistics helpers | IMPLEMENTED (new) | `evaluation/statistics.py` |
| benchmark_v3 builder | IMPLEMENTED (new) | `scripts/build_benchmark_v3.py` |
| RAG evaluation | STUB (BLOCKED) | `evaluation/rag_security.py` |
| Agent evaluation | STUB (BLOCKED) | `evaluation/agent_security.py` |
| External baselines (Llama Guard, etc.) | NOT IMPLEMENTED | `baselines/comparison_framework.py` registry only |

---

## 3. Missing components

| Gap | Priority |
|-----|----------|
| Publication datasets in clone (NotInject, BIPIA, InjecAgent) | P0 |
| Executed real LLM experiments at scale | P0 |
| Llama Guard / Prompt Guard / NeMo integrations | P0 |
| RAG pipeline (embeddings, vector DB, retriever) | P1 |
| Agent environment (AgentDojo/InjecAgent) | P1 |
| ML/LLM detector implementations | P2 |
| Human judge audit (N≥100) | P1 |
| Multi-seed statistical reports on real results | P0 |
| Detector refactor (split 1,387-line file) | P2 |

---

## 4. Scientific weaknesses

1. **Primary historical ASR was simulated** (`attack_outcome.py` substring matching) — circular with detector.
2. **No publication-scale judge-based results** in repository artifacts.
3. **benchmark_v3 smoke-only** when external datasets absent (11 deduped samples).
4. **Held-out NotInject F1 ≈ 0.41** (committed EXP-017/018 metrics) — poor generalization.
5. **Adaptive controller not empirically validated** on real LLMs post-upgrade.
6. **No defense-aware attacker evaluation**.
7. **No cross-model results** (GPT-4o-mini, Llama-3.1-8B, Qwen2.5-7B) executed in repo.

---

## 5. Engineering weaknesses

1. Monolithic `prompt_injection_detector.py` (~1,387 lines, duplicated patches).
2. `results/` gitignored — clone not self-contained.
3. Garak/Inspect adapters expected `DefensePipeline` — **fixed** via alias.
4. Heavy `requirements.txt` (222 packages) vs lean `requirements-core.txt`.
5. No CI workflow for EXP000 gate.

---

## 6. Reproducibility issues

| Issue | Severity |
|-------|----------|
| Datasets gitignored | High |
| API key required but not in repo | Expected |
| No committed Phase 8 harmonized artifacts | Medium |
| Windows-oriented full lockfile | Medium |
| EXP002 sample limit via env var | Low |

Mitigations added: `run_all_experiments.sh`, `Dockerfile`, `environment.yml`, `docs/README_REPRODUCIBILITY.md`, experiment logging.

---

## 7. Paper-level weaknesses

- No tables with real judge-based ASR ± CI across models.
- No SOTA baseline comparison table with executed runs.
- No RAG/agent experimental section possible yet.
- Threat model and novelty not validated against executed evidence.
- Statistical tests implemented but **not applied** to real experiment outputs.

---

## 8. Priority ranking

### P0 (publication blockers)

1. Acquire and integrate external benchmarks (NotInject, BIPIA, InjecAgent)
2. Execute EXP002/EXP003 at scale with independent judge
3. Implement and run external baselines on identical protocol
4. Multi-model evaluation (3 targets × shared judge)
5. Bootstrap CI + McNemar on paired policy comparisons

### P1 (major)

6. RAG security pipeline + EXP005
7. Agent environment + EXP006
8. Human judge audit subset
9. Ablation + latency/cost (EXP007/EXP008)
10. Bayesian/context controller empirical comparison (EXP004)

### P2 (improvements)

11. Detector modularization without deleting history
12. ML/LLM detector backends
13. Defense-aware attacker protocol
14. CI/CD and artifact publishing policy

---

## Experiment status (honest)

| ID | Status |
|----|--------|
| EXP000 | NOT_RUN / BLOCKED without API key |
| EXP001 | PARTIAL (smoke data) |
| EXP002 | NOT_RUN / BLOCKED without API key |
| EXP003–008 | NOT_RUN |
