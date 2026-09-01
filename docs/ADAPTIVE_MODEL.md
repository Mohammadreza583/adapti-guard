# Adaptive Controller — Mathematical Formulation

## Objective (context-aware controller)

Maximize per-step objective:

\[
J_t = \Delta\text{Security}_t - \gamma \cdot \text{Cost}_t - \delta \cdot \text{UtilityLoss}_t
\]

Where:

- \(\Delta\text{Security}_t = 1\) if adaptation signal is `INCREASE_DEFENSE` after successful attack containment feedback
- \(\text{Cost}_t\) = measured or legacy proxy defense cost
- \(\text{UtilityLoss}_t\) = 1 when legitimate utility degraded under expensive defense
- \(\gamma, \delta\) = configurable weights (sensitivity analysis required)

## Controllers

| Controller | Type | Implementation |
|------------|------|----------------|
| RuleBasedController | Threshold counters | `PolicyUpdateEngine` |
| BayesianRiskController | Beta-Bernoulli posterior on attack success | `controllers/adaptive_controller.py` |
| ContextAwarePolicyController | Cost/utility-weighted gate on rule-based updates | `controllers/adaptive_controller.py` |

## Scientific classification

- **Adaptive:** yes  
- **Learning-based (RL/gradient):** no  
- **Bayesian:** partial (BayesianRiskController only)

## Validation status

**NOT_RUN** — empirical comparison via EXP004 required.
