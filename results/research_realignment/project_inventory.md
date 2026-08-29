# Project Inventory — Phase 1 Forensic Audit

Generated: 2026-08-29T15:36:31.416191+00:00

CODE CHANGES: NO (audit-only).

| Component | File | Purpose | Status | Scientific Role |
| --------- | ---- | ------- | ------ | --------------- |
| Architecture / Pipeline | `src/adapti_guard/core/pipeline.py` | Episode orchestration glue | PRESENT | System scaffold |
| Core models | `src/adapti_guard/core/models.py` | Enums/dataclasses (RiskLevel, DefenseAction) | PRESENT | Shared types |
| Detector | `src/adapti_guard/detector/prompt_injection_detector.py` | Regex/rule PI detector | PRESENT (MVP) | Security signal source; limits external validity |
| Risk engine | `src/adapti_guard/risk/risk_engine.py` | Weighted risk incl. historical 0.05 | PRESENT; hist empirically inert | Risk → policy input |
| Policy engine | `src/adapti_guard/policy/policy_engine.py` | Maps risk+level → DefenseAction | PRESENT | Decision layer |
| Defense action layer | `src/adapti_guard/defense/action_layer.py` | A0–A3 execute sanitize/restrict/block | PRESENT (MVP heuristics) | Intervention semantics L0–L3 |
| Feedback engine | `src/adapti_guard/adaptation/feedback_engine.py` | SUC reward + INCREASE/REDUCE/MAINTAIN | PRESENT | Cost-aware adaptation signals |
| Policy update engine | `src/adapti_guard/adaptation/policy_update_engine.py` | Discrete L0–L3 escalate/de-escalate | PRESENT | Core adaptive algorithm |
| Adaptive attacker | `src/adapti_guard/attacker/adaptive_attacker.py` | Family switch + sophistication after failures | PRESENT but NOT primary Phase7 protocol | Threat model component (secondary mode) |
| Outcome evaluator | `src/adapti_guard/evaluation/outcome_evaluator.py` | ASR/utility/cost from deterministic rules | PRESENT | Metric ground truth (MVP) |
| Experiment runner | `src/adapti_guard/experiments/experiment_runner.py` | Controlled stream+schedule OR live AdaptiveAttacker | PRESENT | Primary eval harness |
| Phase7 schedule | `src/adapti_guard/experiments/phase7_schedule.py (+ results/phase7/phase7_schedule.json)` | 75 attack / 25 legitimate pattern | PRESENT | Mixed-workload protocol |
| Baselines | `src/adapti_guard/baselines/baseline_runner.py` | Fixed L0–L3 runners | PRESENT on phase branches | Fixed-level comparison |
| Phase8A multiseed | `scripts/run_phase8a_multiseed.py + experiments/phase8_*` | Seeds 1–5, mean±CI | PRESENT (artifacts frozen) | Repro/stats |
| Phase8B analyses | `scripts/run_phase8b.py` | Ablation/temporal/family | PRESENT | Ablation evidence |
| Phase8C robustness | `scripts/run_phase8c.py` | Novel/evolving/SUC/stats | PRESENT | Robustness package |
| Phase9 evidence audit | `results/phase9/evidence_audit_v1.json` | Evidence integrity audit | FROZEN | Claim hygiene |
| Phase10 claim matrix | `results/phase10/claim_evidence_matrix_v1.json` | C1–C10 statuses | FROZEN | Claim–evidence map |
| Phase11 novelty audit | `results/phase11/final_novelty_audit_v1.json` | 55-paper novelty audit | FROZEN | Literature positioning |
| Frozen attack stream | `results/common_attack_stream.json` | Known attack payloads | FROZEN | Controlled eval input |
| Phase7 results | `results/phase7/*_v2.json` | Adaptive + fixed baselines | IMMUTABLE | Primary empirical table |
| Phase8 results | `results/phase8/*.json` | Multiseed/ablation/SUC/stats | IMMUTABLE | Extended evidence |
| Unit tests | `tests/test_*.py` | Component unit tests | PARTIAL on main; fuller on phase branches | Engineering QA |
| Integrations | `garak_adapter.py, promptfoo-test/, inspect-test/` | External eval adapters | PRESENT stubs/adapters | Engineering, not Q1 core |
| Paper stubs | `Agent, Defense, Policy, Risk, assert (0-byte)` | Placeholder files | EMPTY | No scientific content |
| Paper corpus TOTAL-- | `TOTAL--/{01..08}` | 55 TXT/PDF literature | ABSENT in this VM | Blocking for camera-ready lit cert |
| REPRODUCIBILITY.md | `(missing)` | End-to-end repro guide | ABSENT | Reproducibility gap |
| Manuscript | `(no paper .tex/.md body in repo)` | Paper narrative | ABSENT/minimal | Claim surface unmanaged in-repo |

## Critical forensic findings
1. Primary Phase7/8 protocol uses **frozen attack stream**, not live `AdaptiveAttacker` optimization (`attacker.observe` only when `attack_stream is None`).
2. Mixed schedule is **75% attack / 25% legitimate** (`phase7_schedule.json`), not 75% legitimate.
3. Historical signal weight 0.05 is implemented; Phase8 ablation `historical_signal_changed_aggregates=false` → contribution unsupported.
4. External baselines (SafeHarness/Task Shield/Spotlighting/PIGuard/MELON/VIGIL) are **not** in current eval suite.
5. Local `TOTAL--` TXT corpus is **not mounted** in this environment; Phase2 uses Phase11 audited paper profiles + available full-text extracts.
