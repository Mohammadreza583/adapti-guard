# Q1_REVIEWER_AUDIT

Venue lens: LLM/Agent Security Q1.

## Scores

| Criterion | Score | Note |
|-----------|-------|------|
| Novelty | WEAK–ADEQUATE | Escalate/de-escalate levels prefigured by SafeHarness; AG differentiator is narrower protocol+cost/legitimate trigger |
| Technical contribution | ADEQUATE | Clear L0–L3 MVP controller; heuristics limit depth |
| Methodology | ADEQUATE | Controlled 75/25 is sound for utility; detector MVP weakens realism |
| Experimental rigor | ADEQUATE | Frozen stream, fixed baselines, SUC, ablations present; escalate-only missing |
| Baselines | WEAK | Missing SafeHarness-like and escalate-only; no strong system-level baselines (CaMeL/Progent) |
| Reproducibility | STRONG | Deterministic; artifacts frozen; std=0 documented |
| Statistical validity | ADEQUATE | Holm episode tests exist; multi-seed variance uninformative under determinism |
| Threat-model realism | WEAK | Synthetic stream; AutoDojo/Adaptive Adversaries show adaptive attackers needed |
| Claim-evidence alignment | WEAK if overclaimed; ADEQUATE if Phase10-bounded | C6 null; generalization LIMITED |
| Literature positioning | CRITICAL until TOTAL-- ingested | Local corpus absent in this audit environment |

## CRITICAL issues

1. Local TOTAL-- corpus not available → literature completeness not certifiable for camera-ready Q1 positioning.
2. Discrete escalate/de-escalate levels are not a unique technical idea (SafeHarness); uniqueness claims would be fatal.
3. Evolving/novel generalization claims exceed evidence relative to AutoDojo-class adaptive attackers.

## MAJOR issues

1. Missing escalate-only / de-escalation ablation.
2. No baseline against privilege-degradation or detector-allocation adaptive methods.
3. MVP regex detector + marker sanitize inflate sanitized "defense" on marker-free novel payloads.
4. Historical signal implemented but empirically inert — narrative risk if marketed as key module.

## MINOR issues

1. Family counts uneven (19/19/19/18).
2. Reward weights (0.5/0.4/0.1) not sensitivity-analyzed.
3. Engineering presentation may oversell MVP as agent platform.
