# Required Changes

Generated: 2026-08-29T15:36:31.416191+00:00
CODE CHANGES = NO in this audit stage (no critical implementation↔claim mismatch requiring code edit beyond claim/docs).

| Priority | Problem | Why Q1 reviewer cares | Required change | Code change? | Experiment? |
| -------- | ------- | --------------------- | --------------- | ------------ | ----------- |
| P0 | Uniqueness / first / SOTA adaptive-level claims | Novelty fatal | Rewrite claims; position vs SafeHarness/SCOUT | NO | NO |
| P0 | C6 historical contribution | Evidence contradiction | REMOVE / limitation only | NO | NO |
| P0 | “Robust to adaptive attackers” wording | Threat-model mismatch | Weaken to evaluated conditions; frozen≠AutoDojo | NO | NO |
| P0 | Possible 75% legitimate misstatement | Protocol integrity | State **75% attack / 25% legitimate** everywhere | NO | NO |
| P1 | Missing escalate-only / de-esc-only ablation | Causal credit for contribution #2 | New experiment file; keep old results | Optional harness flags | YES (new) |
| P1 | No REPRODUCIBILITY.md | Repro standard | Add doc | Docs only | NO |
| P1 | TOTAL-- not in VM | Lit completeness | Mount TXT; refresh matrix | NO | NO |
| P1 | Deterministic std=0 oversold | Stats credibility | Disclose; bind C10 to reproducibility not variance | NO | NO |
| P2 | No external light baseline (Spotlighting) | Relative ranking | Optional if reproducible | Small | Optional |
| P2 | Latency/F1 metrics absent | Completeness | Only if claims need them | Optional | Optional |
| P2 | Reward-weight sensitivity | Robustness of SUC | Optional sweep | Optional | Optional |
| P3 | Full SafeHarness/MELON/VIGIL reimplementation | Nice-to-have | Skip unless resources | Heavy | Heavy |

**Execute now:** P0 claim/docs alignment only.  
**Do not execute P3.**
