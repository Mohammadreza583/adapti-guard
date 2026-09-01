# Manuscript Upgrade Plan

**Target venue tier:** Q1 security / trustworthy AI  
**Current readiness:** 4.5 / 10  
**Date:** 2026-09-01

---

## Paper structure

### 1. Introduction
- Problem: adaptive LLM defense under attack–utility–cost tradeoffs
- Gap: fragmented evaluation, circular ASR metrics in prior work
- Contribution: harmonized evaluation framework + adaptive controller + real judge pipeline

### 2. Related Work
- Prompt injection benchmarks (NotInject, BIPIA, InjecAgent)
- Guard models (Llama Guard, Prompt Guard, NeMo)
- Adaptive security systems

### 3. Threat Model
- Direct/indirect injection, jailbreak, RAG, agent, tool attacks
- Attacker capabilities and defender assumptions
- Reference: `docs/Q1_RESEARCH_AUDIT.md`

### 4. ADAPTI-GUARD Architecture
- Detection → Risk → Policy → Action pipeline
- Hybrid detector: regex + ML + optional LLM scorer
- Diagram: `docs/architecture/` (to be generated from code)

### 5. Adaptive Controller
- Formal objective: maximize Security Gain − γ·Latency Cost − δ·Utility Loss
- Controllers: RuleBased, BayesianRisk, ContextAware
- Reference: `docs/ADAPTIVE_MODEL.md`

### 6. Experimental Setup
- Dataset: benchmark_v4 (when publication_ready)
- Target models: GPT-4o-mini, Llama-3.1-8B, Qwen2.5-7B
- Judge: independent LLM (Gemma-2-9B-IT)
- Baselines: 6-way comparison (EXP003)
- Seeds: ≥5 with bootstrap CI

### 7. Results
**Populate only from executed experiments:**

| Table | Source | Status |
|-------|--------|--------|
| Main ASR/Utility | EXP002 + EXP003 | BLOCKED |
| Baseline comparison | `results/baseline_comparison.csv` | BLOCKED |
| RAG metrics | EXP005 | DONE (offline) |
| Agent metrics | EXP006 | DONE (offline) |
| Controller ablation | EXP004/EXP007 | DONE (simulation) |

### 8. Ablation
- A: No adaptation (Fixed L0)
- B: Rule adaptation
- C: Bayesian adaptation
- D: Full ADAPTI-GUARD
- Source: `results/EXP007_ablation/metrics.json`

### 9. Limitations
- Smoke dataset until external integration
- Simulation ASR in harmonized runner (LEGACY_SIMULATION_ONLY)
- No human judge audit
- NeMo Guardrails not integrated

### 10. Conclusion
- Framework contribution vs. novel defense mechanism
- Path to full validation

---

## Required artifacts before submission

- [ ] EXP002 executed at scale (≥500 test × 3 models)
- [ ] EXP003 baseline CSV with real rows
- [ ] benchmark_v4 `publication_ready: true`
- [ ] Statistical significance tests on real results
- [ ] Architecture diagram (PDF/SVG)
- [ ] Reproducibility package (Docker + locked deps)

---

## Result tables (templates)

### Table 1: Attack Success Rate by Defense

| Defense | ASR ↓ | 95% CI | Utility ↑ | Latency (ms) |
|---------|------:|--------|----------:|-------------:|
| No Defense | — | — | — | — |
| Regex | — | — | — | — |
| ADAPTI-GUARD | — | — | — | — |
| Llama Guard | — | — | — | — |

*Fill from `results/baseline_comparison.csv` after API execution.*

### Table 2: Adaptive Controller Comparison

| Controller | ASR | Utility | Cost | Transitions |
|------------|----:|--------:|-----:|------------:|
| Fixed L0 | — | — | — | 0 |
| Fixed L3 | — | — | — | 0 |
| Rule Adaptive | — | — | — | — |
| Bayesian | — | — | — | — |

*Fill from EXP004 after real-judge validation.*

---

## Recommendation

**Do not submit** until EXP002/EXP003 produce judge-based results at publication scale. Current manuscript plan documents structure and honest gaps.
