# Core Contributions, Experiments, Metrics, Ablations, Attacker, Stats, Repro

Generated: 2026-08-29T15:36:31.416191+00:00

## Phase 5 — Core contributions (max 3; evidence-backed)

| # | Contribution | Implementation | Experiments | Status |
| - | ------------ | -------------- | ----------- | ------ |
| 1 | Adaptive discrete intervention policy L0–L3 (A0–A3) | PolicyUpdateEngine + ActionLayer | Phase7 transitions; Fixed vs Adaptive | KEEP (non-uniqueness of levels disclosed) |
| 2 | Cost-aware escalation/de-escalation under changing attack/legitimate pressure | FeedbackEngine cost gates + thresholds | Phase7 ↑14/↓11; temporal analysis | KEEP; escalate-only ablation MISSING |
| 3 | Evaluation protocol: adaptive vs fixed under mixed workload (+ adaptive attacks) | Schedule 75/25 + SUC metrics | Phase7/8 Fixed L0–L3 vs Adaptive | PARTIAL mismatch: adaptive-attacker primary eval MISSING |

### Mismatch report
- Contribution #3 text includes adaptive attacks, but primary results use **frozen stream**.
- **Minimum fix:** weaken contribution #3 wording now; optionally add AutoDojo-style/live AdaptiveAttacker eval as **new** experiment later (do not overwrite frozen results).

## Phase 6 — Baselines

| Baseline | Present? | Notes |
| -------- | -------- | ----- |
| No defense | YES as Fixed L0 | ASR=1.0 |
| Fixed L1/L2/L3 | YES | Phase7/8 |
| Adaptive AG | YES | Phase7/8 |
| SafeHarness | NO | High-value but non-trivial reimplementation — do not fake |
| Task Shield | NO | Not reproducibly integrated |
| Spotlighting | NO | Could be light prompt baseline later |
| PIGuard | NO | External model dependency |
| MELON | NO | Re-exec agent stack required |
| VIGIL | NO | Not in repo |

**Rule:** do not add unreproducible baselines.

## Phase 7 — Metrics checklist

| Metric | Present? | Needed for claims? |
| ------ | -------- | ------------------ |
| ASR | YES | YES |
| Defense rate | YES | YES |
| FPR/FNR/Precision/Recall/F1 | NO | Optional if detector claims rise; not needed for current SUC policy claims |
| Task success / utility | YES | YES |
| Legitimate degradation | YES (via utility under L3) | YES |
| Intervention rate | PARTIAL (levels/actions logged) | Useful; derive from episodes |
| False intervention rate | NO | Useful for over-defense; optional P1 |
| Escalation/de-escalation frequency | YES (manifest ↑↓) | YES |
| Transition count | YES | YES |
| Time-to-escalation/recovery | PARTIAL (temporal windows) | Optional strengthen |
| Latency/token/compute overhead | NO | Only if efficiency claims made — currently avoid |

## Phase 8 — Ablations

| Ablation | Present? | Note |
| -------- | -------- | ---- |
| Adaptive ON/OFF (vs fixed) | YES | |
| Escalation ON/OFF | NO | **P0/P1 gap** for contribution #2 |
| De-escalation ON/OFF | NO | **P0/P1 gap** |
| Cost-aware ON/OFF | NO | Related to de-esc gates |
| Fixed vs adaptive | YES | |
| Attack/historical feedback ON/OFF | YES | Null — **not** a contribution |

## Phase 9 — Mixed workload truth

- Documented & encoded: **attack=75, legitimate=25** (`phase7_v2_75_25`).
- Pattern: `[attack,attack,attack,legitimate] × 25`.
- If any narrative says 75% legitimate, that is **incorrect** and must be fixed in claims/paper (claims hygiene; not a result rewrite).

Comparisons available: Fixed L0–L3 + Adaptive on ASR/utility/cost/reward. Latency not measured.

## Phase 10 — Adaptive attacker truth

| Question | Answer |
| -------- | ------ |
| Feedback? | Yes in live mode (`observe`) |
| Changes with defense? | Yes — family rotate + sophistication on failures |
| Multi-step/multi-turn? | Episode-level family switch; not AutoDojo multi-turn optimizer |
| Pressure change? | Via family/sophistication, not continuous optimizer |
| Used in primary Phase7/8? | **NO** — frozen stream path |

**Banned claim:** robust against adaptive attackers.  
**Allowed:** evaluated under controlled/frozen and constructed evolving streams; AdaptiveAttacker available in non-stream mode.

## Phase 11 — Statistical validity

- Seeds: 1–5 present.
- mean ± std + 95% t-CI present.
- Holm-Bonferroni episode tests present in Phase8C.
- **Gap:** std=0 (deterministic pipeline) → seed CI uninformative for stochastic robustness.
- **Minimum fix:** disclose determinism; optional stochastic detector/LLM judge later for informative variance.

## Phase 12 — Reproducibility

| Item | Status |
| ---- | ------ |
| dependencies | requirements.txt present |
| environment | cloud VM; no REPRODUCIBILITY.md |
| model | MVP heuristics (no frontier LLM defender in core loop) |
| dataset/stream | common_attack_stream + schedule frozen |
| seeds | documented in Phase8A |
| attack/defense/experiment configs | partially in JSON manifests |
| output format | JSON artifacts |

**Proposal:** add `REPRODUCIBILITY.md` (P1). Do not invent missing hardware/model details.

## Phase 13 — Result integrity

- Phase7–10 artifacts treated **immutable**.
- Any new experiment must write new files (e.g. `results/realignment_exp/*`) with provenance: experiment→config→seed→raw→aggregate→metric.
- Do not delete or overwrite prior JSON.
