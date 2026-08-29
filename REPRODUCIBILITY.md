# REPRODUCIBILITY.md

## Environment
- OS: Linux (Cursor Cloud VM)
- Python: 3.x (stdlib + project code; no GPU required for MVP)
- Repo root: `/workspace`

## Dependencies
See `requirements.txt`. Core Q1 realign experiments use only the in-repo MVP stack (regex detector, rule-based evaluator). No external LLM API is required for these runs.

## Model
MVP heuristic defender:
- `PromptInjectionDetector` (regex/rule)
- `DefenseActionLayer` sanitize heuristics
- Deterministic `OutcomeEvaluator`

This is **not** a frontier LLM agent harness.

## Dataset / attack stream
- Frozen stream: `results/common_attack_stream.json`
- Slice: first 75 records (`PHASE7_ATTACK_STREAM_SLICE = (0, 75)`)
- Legitimate tasks: `ExperimentRunner.BENIGN_TASKS` (rotating)

## Seed
- Q1 realign seeds: `1, 2, 3`
- Pipeline is deterministic given frozen stream + schedule; cross-seed `std=0` is expected and is **not** stochastic robustness evidence.

## Attack configuration
### Frozen protocol (primary)
- Schedule: `[attack, attack, attack, legitimate] × 25` → **75 attack / 25 legitimate**
- Source: `src/adapti_guard/experiments/phase7_schedule.py`
- Attack payloads from frozen stream in order

### Live AdaptiveAttacker protocol (secondary, new)
- Same schedule
- Attack payloads from `AdaptiveAttacker.generate()`
- On failure: family round-robin + sophistication index
- Observes success/fail only (not full defense action text)
- **Not** AutoDojo-class multi-turn optimization

## Defense configuration
- Levels L0–L3 → A0–A3 (NO_INTERVENTION / SANITIZE / TOOL_RESTRICTION / BLOCK)
- Escalation threshold: 2 attack successes (`PolicyUpdateEngine.attack_threshold`)
- De-escalation threshold: 2 legitimate/cost signals (`legitimate_threshold`)
- Cost gates (default): reduce if legitimate success & cost≥0.25, or legitimate fail & cost≥0.50
- Ablation flags: `enable_escalation`, `enable_deescalation`, `use_cost_gate`, `use_historical_signal`

## Experiment configuration
Runner: `scripts/run_q1_realign_experiments.py`

| Experiment | Output dir |
| ---------- | ---------- |
| Fixed L0–L3 vs Adaptive | `results/q1_realign/fixed_vs_adaptive/` |
| Ablations | `results/q1_realign/ablation/` |
| Frozen vs AdaptiveAttacker | `results/q1_realign/adaptive_attacker/` |
| Raw episodes | `results/q1_realign/raw/` |
| Manifest | `results/q1_realign/EXPERIMENT_MANIFEST.json` |

## Metrics
ASR, legitimate task success, intervention rate, false intervention rate, defense cost mean, escalation/de-escalation/transition counts, reward mean.

## Exact commands
```bash
cd /workspace
export PYTHONPATH=/workspace
python3 scripts/run_q1_realign_experiments.py
```

## Output structure
Each condition writes:
1. per-seed metrics JSON
2. raw episode JSON under `raw/`
3. `summary.json` aggregation
4. manifest entry with config, seed, code hash, paths

## Immutable prior results
Do **not** modify:
`results/phase7`, `results/phase8`, `results/phase9`, `results/phase10`, `results/phase11`
