# Adaptive Controller — Mathematical Formulation

**Version:** v2 (Q1 enhancement)  
**Date:** 2026-09-01

---

## Objective

The adaptive controller maximizes a per-step security–cost–utility tradeoff:

\[
\max_{\ell_t} \; J_t = \Delta\text{Security}_t - \gamma \cdot \text{LatencyCost}_t - \delta \cdot \text{UtilityLoss}_t
\]

Where:
- \(\ell_t \in \{0,1,2,3\}\) is the defense level at time \(t\)
- \(\Delta\text{Security}_t\) = reduction in attack success probability from escalation
- \(\text{LatencyCost}_t\) = measured or proxy defense latency/cost
- \(\text{UtilityLoss}_t\) = legitimate task failure rate under strict defense
- \(\gamma, \delta\) = tunable weights (sensitivity analysis via EXP004)

---

## Controllers

| Controller | Class | Mechanism |
|------------|-------|-----------|
| RuleBasedController | Threshold | Attack/legitimate pressure counters → level change |
| BayesianRiskController | Probabilistic | Beta-Bernoulli posterior on attack success; escalate when \(E[p] > \tau_{\uparrow}\) |
| ContextAwarePolicyController | Heuristic gate | Applies rule-based updates only when \(J_t\) exceeds thresholds |

Implementation: `src/adapti_guard/controllers/adaptive_controller.py`

---

## Comparison protocol (EXP004)

| Variant | Description |
|---------|-------------|
| Fixed L0 | No defense escalation (level 0) |
| Fixed L3 | Maximum static defense (level 3) |
| Rule Adaptive | `PolicyMode.FULL_ADAPTIVE` via harmonized runner |
| Bayesian Adaptive | `BayesianRiskController` trajectory + harmonized runner |

**Current evaluation mode:** LEGACY_SIMULATION_ONLY (harmonized runner uses `attack_outcome.py`).  
Real-judge validation requires EXP002 execution with API access.

---

## Security gain definition

\[
\Delta\text{Security}_t = \mathbb{1}[\text{adaptation\_signal} = \text{INCREASE\_DEFENSE} \land \text{attack\_contained}]
\]

Proxy in simulation: feedback from `FeedbackEngine` after episode outcome.

---

## Validation status

| Test | Status |
|------|--------|
| EXP004 multiseed (5 seeds) | DONE (simulation) |
| EXP007 ablation | DONE (simulation) |
| Real LLM + judge | NOT_RUN |
| Statistical significance | Pending real results |

---

## Scientific classification

- **Adaptive:** yes
- **Learning-based (RL/gradient):** no
- **Bayesian:** partial (BayesianRiskController)
- **Novelty claim:** cost-aware gating over rule-based adaptation (requires empirical validation)
