# STEP 1 — Forensic Check (new findings only)

Generated for Q1 experiment repair. Does **not** repeat prior Phase11 / research_realignment audits.

## New findings

1. **Workspace `experiment_runner.py` was syntax-corrupted** (leading markdown fence `` ```python ``). Controlled Phase7 harness (attack_stream + schedule) was missing on this branch tip until restored from `phase10` sources. Prior frozen JSON results remain valid; local runnable harness was not.

2. **Defense level ≠ forced action.** `DefensePolicyEngine.decide` blends current risk baseline with `defense_level`. HIGH risk can BLOCK even at low adaptive level; LOW risk never permanently stays at full BLOCK via level alone. Fixed-level baselines bypass this blend (level→action mapping in BaselineRunner). Adaptive vs Fixed are therefore not perfectly isomorphic controllers—report this when comparing.

3. **Intervention rate is not a first-class frozen metric.** Phase7/8 report ASR/utility/cost/reward/levels/transitions, but not explicit `intervention_rate` / `false_intervention_rate`. Derive in new q1_realign runs.

4. **Cost gate lives only in `FeedbackEngine` signal emission**, not in `PolicyUpdateEngine`. Disabling cost awareness requires changing feedback thresholds/signals; policy counters alone cannot express “no cost gate.”

5. **`AdaptiveAttacker` adaptation is family-round-robin on failure**, not defense-aware optimization (no defense-action conditioning beyond success/fail bit). Multi-turn prompt optimization (AutoDojo-class) is absent.

6. **Empty root stubs** (`Agent`, `Defense`, `Policy`, `Risk`, `assert`) remain 0-byte and are not scientific artifacts.

## Non-findings (already established — not re-argued)

SafeHarness overlap; C6 null historical; 75/25 attack/legitimate; frozen-stream primary protocol; std=0 determinism.

7. **Confirmed by new runs:** Adaptive high levels can keep legitimate utility=1.0 while Fixed-L3 has utility=0.0, because adaptive decisions blend risk with level (LOW-risk legitimate often executes as A2, not A3). Fixed baselines force level→action. Comparisons must disclose this non-isomorphism.

## Critical claim↔implementation mismatch?

No architecture redesign required. Harness restore + ablation flags are sufficient for Q1 repair experiments.
