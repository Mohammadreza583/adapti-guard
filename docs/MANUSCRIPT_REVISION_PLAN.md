# Manuscript Revision Plan

## Paper structure

1. Introduction — runtime adaptive defense under security–utility–cost trade-offs  
2. Related Work — guardrails, injection benchmarks, adaptive policies  
3. Threat Model — direct/indirect injection, agent/RAG (scope TBD by experiments)  
4. ADAPTI-GUARD Framework — detector, risk, policy, actions  
5. Adaptive Policy Mechanism — threshold + optional Bayesian/context controllers  
6. Experimental Setup — benchmark_v3, 3 target models, independent judge  
7. Results — **pending EXP002–008 execution**  
8. Ablation Study — EXP007  
9. Limitations — simulation legacy, dataset scope, judge dependence  
10. Conclusion  

## Evidence requirements before submission

| Section | Required experiment | Status |
|---------|---------------------|--------|
| Results (ASR) | EXP002 + EXP003 | NOT_RUN |
| Cross-model | EXP002 × 3 models | NOT_RUN |
| Baselines | EXP003 | NOT_RUN |
| RAG | EXP005 | BLOCKED |
| Agent | EXP006 | BLOCKED |
| Statistics | Bootstrap + McNemar | NOT_RUN |

## Tables/figures to generate (after experiments)

- Table 1: Dataset statistics (`benchmark_v3/statistics.json`)
- Table 2: ASR ± CI per model and baseline
- Table 3: Utility / FPR / latency
- Figure 1: Architecture diagram (defense → target → judge)
- Figure 2: Security–utility–cost Pareto (if supported by data)

**Do not include fabricated numbers.**
