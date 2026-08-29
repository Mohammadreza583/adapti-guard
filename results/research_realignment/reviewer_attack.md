# Reviewer Attack

Generated: 2026-08-29T15:36:31.416191+00:00

## Reviewer A — Novelty

| # | Objection | Evidence? | Gap | Minimum fix |
| - | --------- | --------- | --- | ----------- |
| 1 | Discrete escalate/de-escalate already in SafeHarness | YES | Uniqueness of levels indefensible | Reframe to intervention semantics + mixed SUC protocol |
| 2 | SCOUT already does safety–utility–cost adaptation | PARTIAL | Different object (detectors) | Explicit differentiation table |
| 3 | AgentAntibody already runtime-adaptive memory defense | PARTIAL | Different mechanism | Position as complementary, not “first adaptive” |
| 4 | Historical memory claimed but null | YES (C6) | Contribution false | REMOVE C6 |
| 5 | Evolving robustness weaker than COPA/HARD/AutoDojo | YES | Threat-model gap | Weaken C9; optional new adaptive-attacker exp |

## Reviewer B — Experimental validity

| # | Objection | Evidence? | Gap | Minimum fix |
| - | --------- | --------- | --- | ----------- |
| 1 | Regex detector + marker sanitize inflate defense | YES (MVP code) | External validity | Disclose MVP limits; avoid strong security claims |
| 2 | No SafeHarness/Task Shield baselines | YES | Relative novelty unclear | Optional light Spotlighting; no fake complex baselines |
| 3 | Missing escalate-only / de-escalate-only ablations | YES | Causal credit for cost-aware de-esc weak | Add escalate-only ablation as new experiment |
| 4 | Primary eval not AutoDojo adaptive attacker | YES | Adaptive-robustness overclaim risk | Fix wording; optional new eval |
| 5 | Workload is attack-heavy 75/25, may skew utility story | YES | Protocol sensitivity | Disclose; optional legitimate-heavy sensitivity later |

## Reviewer C — Reproducibility / statistics

| # | Objection | Evidence? | Gap | Minimum fix |
| - | --------- | --------- | --- | ----------- |
| 1 | std=0 across seeds | YES | No stochastic uncertainty | Disclose determinism; don’t sell as robust multi-seed variance |
| 2 | No REPRODUCIBILITY.md | YES | Onboarding/repro friction | Add REPRODUCIBILITY.md |
| 3 | TOTAL-- corpus absent in env | YES | Lit completeness | Mount TXT corpus; refresh paper matrix |
| 4 | Reward weights 0.5/0.4/0.1 not sensitivity-tested | YES | Hyperparam opacity | Disclose; optional P2 sweep |
| 5 | Provenance good for frozen JSON, weak for narrative claims | PARTIAL | Claim drift risk | Bind paper claims to Phase10 statuses |
