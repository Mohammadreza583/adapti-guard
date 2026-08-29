# ADAPTI_GUARD_ACTUAL_SPEC

Source of truth for this audit: `/workspace/src/adapti_guard/` + frozen `results/phase7|8|9|10`  
(`15_BASE_Q1/adapti_guard/` not present.)

Generated: 2026-08-29T12:40:28.345608+00:00

## Architecture (implemented)

Pipeline (episode):
1. Schedule selects attack vs legitimate (`phase7_schedule`: `[False,False,False,True]×25` → 75/25)
2. Attack payloads from frozen `common_attack_stream` first-75 slice
3. `PromptInjectionDetector` (rule-based regex families)
4. `RiskAssessmentEngine` (detection + tool_sensitive + contextual + **historical_attack weight 0.05**)
5. `DefensePolicyEngine.decide(risk, tool_sensitive, defense_level)`
6. `DefenseActionLayer.execute` (A0–A3)
7. `OutcomeEvaluator` → security/utility/defense_cost
8. `FeedbackEngine` → reward + INCREASE/REDUCE/MAINTAIN
9. `PolicyUpdateEngine.update` → discrete `defense_level` 0–3 transitions

## L0–L3 semantics (code)

| Level | DefenseAction | Effect (action_layer) | Cost |
|------|---------------|------------------------|------|
| 0 | A0 NO_INTERVENTION | allow content + tools | 0.00 |
| 1 | A1 SANITIZE | strip known instruction markers | 0.10 |
| 2 | A2 TOOL_RESTRICTION | allow content, tools off | 0.25 |
| 3 | A3 BLOCK | deny interaction | 0.50 |

Policy also blends **risk baseline** with level (policy_engine): level can strengthen LOW/MEDIUM; HIGH uses risk baseline; avoids permanent L3 block of LOW risk.

## Policy state

`PolicyState`: `defense_level`, `attack_failures`, `legitimate_failures`, `successful_attacks`, `total_updates`.

## Escalation rule

If `attack_success` → `INCREASE_DEFENSE` → increment `attack_failures`; when ≥ `attack_threshold` (default 2): `defense_level = min(3, level+1)`, reset counter.

## De-escalation rule

`REDUCE_DEFENSE` when:
- legitimate_task ∧ legitimate_success ∧ defense_cost ≥ 0.25, OR
- legitimate_task ∧ ¬legitimate_success ∧ defense_cost ≥ 0.50  
Then increment `legitimate_failures`; when ≥ `legitimate_threshold` (default 2): `defense_level = max(0, level-1)`.

## Signals

- Attack detection: regex detector score/is_injection
- Legitimate-task: schedule flag + outcome utility 1/0
- Reward: `0.5*security + 0.4*utility − 0.1*cost` (FeedbackEngine defaults)
- Defense cost: ACTION_COST table
- Utility: 1 iff legitimate success; 0 otherwise (attack episodes utility 0 by construction for attack strata)
- Historical: running attack success rate into risk (weight 0.05); **ablation: no aggregate change**

## Attack model / datasets

- Primary eval: frozen known stream slice + synthetic novel/evolving sets (Phase 8C)
- `AdaptiveAttacker` class exists (family switch after failures) — **Phase 7/8 primary results use frozen stream schedule, not live AdaptiveAttacker optimization**
- Families: direct/indirect/context/tool_output

## Workload

- 100 episodes, 75 attack / 25 legitimate, deterministic pattern
- Seeds 1–5 Phase 8A: **std=0** (deterministic pipeline)

## Baselines

Fixed-L0..L3 via BaselineRunner; Adaptive with/without historical (ablation)

## Key frozen results (do not alter)

- Adaptive ASR ≈ 0.373, utility 1.0, defense_cost 0.329, reward 0.4271
- Transitions 25 (↑14 / ↓11)
- `historical_signal_changed_aggregates = false`
- Generalization: LIMITED (Phase 9/10)
- Phase10 C6: NOT SUPPORTED

## Limitations (factual)

- MVP regex detector + marker sanitize + deterministic outcomes
- Not AgentDojo/AutoDojo interactive agent suite as primary protocol
- Historical signal implemented but empirically null
- Evolving eval is constructed stream, not black-box adaptive optimizer
