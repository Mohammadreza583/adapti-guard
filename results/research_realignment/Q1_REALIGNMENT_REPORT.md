# ADAPTI-GUARD — Q1 Research Re-alignment Report

Generated: 2026-08-29T15:36:31.416191+00:00  
Scope: audit-only (`CODE CHANGES = NO`). Prior Phase7–10 results immutable.

## 1. CURRENT RESEARCH POSITION
ADAPTI-GUARD is an MVP runtime discrete intervention-level controller (L0–L3 / A0–A3) with attack-triggered escalation and legitimate-task cost-triggered de-escalation, evaluated against fixed levels under a **75% attack / 25% legitimate** mixed protocol with ASR/utility/defense-cost metrics. It is **not** currently a demonstrated AutoDojo-robust adaptive defense, and discrete escalate/de-escalate levels are **not** uniquely AG’s.

## 2. TRUE NOVELTY
- **PARTIAL:** cost-aware de-escalation trigger + sanitize/restrict/block semantics (vs SafeHarness privilege recovery).
- **UNIQUE\***: mixed-workload fixed-vs-adaptive discrete intervention SUC protocol package among audited papers (\*provisional; `TOTAL--` TXT absent).
- **NOT novel:** discrete adaptive levels writ large; historical-memory contribution; open-world evolving robustness.

## 3. OVERLAP RISKS
| Risk | Severity | Mitigation |
| ---- | -------- | ---------- |
| SafeHarness escalate/de-escalate levels | HIGH | Reframe; differentiation table |
| SCOUT SUC-latency allocation | MEDIUM | Different adaptation object |
| AgentAntibody/HARD/COPA adaptive defenses | MEDIUM | Regime/mechanism differentiation |
| AutoDojo adaptive eval expectation | HIGH for C9 | Weaken wording / optional new exp |

Direct competitors in audited set: **0**. Partial overlap: **13**.

## 4. UNSUPPORTED CLAIMS
- Historical attack feedback contributes (Phase10 **C6 NOT SUPPORTED**; ablation null).
- First/unique adaptive multi-level defense.
- Robust against AutoDojo-class adaptive attackers (primary protocol = frozen stream).
- Open-world novel-attack generalization (Phase10 **C8 LIMITED**).
- Stochastic multi-seed robustness (std=0 determinism).

## 5. EXPERIMENTAL GAPS
- Escalate-only / de-escalate-only / cost-gate ablations missing.
- External reproducible baselines (Spotlighting optional; SafeHarness/MELON/VIGIL not currently reproducible here).
- Primary adaptive-attacker evaluation missing despite `AdaptiveAttacker` class.
- Detector FPR/FNR/F1 and latency/token overhead not measured (only needed if claimed).

## 6. STATISTICAL GAPS
- Seeds 1–5 + 95% CI exist, but **std=0** → CI uninformative.
- Holm tests exist at episode level; seed-level inference not meaningful under determinism.
- Disclose determinism; do not market as variance robustness.

## 7. REPRODUCIBILITY GAPS
- No `REPRODUCIBILITY.md`.
- `TOTAL--` corpus not available in this VM.
- MVP heuristic defender/model stack must be stated explicitly (not a frontier agent harness).
- Config provenance is good in frozen JSON; narrative claims must stay bound to Phase10.

## 8. REQUIRED CHANGES (P0–P1)
1. Claim rewrite: remove first/SOTA/unique; REMOVE C6; weaken C8/C9/C10.
2. Correct protocol language: **75% attack / 25% legitimate**.
3. Add escalate-only (and preferably de-escalate-only) ablation as **new** experiment outputs.
4. Add `REPRODUCIBILITY.md`.
5. Mount `TOTAL--` TXT and refresh paper matrix when available.

## 9. OPTIONAL CHANGES (P2)
- Light Spotlighting baseline if cheap/reproducible.
- Legitimate-heavy sensitivity run.
- Live AdaptiveAttacker or AutoDojo-style eval (new files only).
- Reward-weight sensitivity; intervention/false-intervention rates.

## 10. FINAL Q1 READINESS SCORE

| Dimension | Score (0–5) | Note |
| --------- | ----------- | ---- |
| Novelty framing | 2.5 | Fixable by claim rewrite |
| Technical contribution | 3.0 | Clear MVP controller; shallow detector |
| Experimental design | 3.0 | Good fixed baselines; missing key ablations/adaptive attacker |
| Statistical rigor | 2.5 | Formal CI present; determinism limits meaning |
| Reproducibility | 3.0 | Artifacts strong; docs/corpus incomplete |
| Claim–evidence alignment | 2.0 → 4.0 if P0 applied | Currently overclaim risk |
| **Overall Q1 readiness** | **2.7 / 5** | **Not submission-ready** until P0 claim hygiene; rises to ~3.5 with P0+P1 ablations/docs |

**Bottom line:** Keep the system; tighten claims; add minimal ablations; do not redesign core.
