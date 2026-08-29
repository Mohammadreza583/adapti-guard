# ADAPTI-GUARD — Paper Realignment Draft (Evidence-Bound)

**Status:** Draft for claim alignment with `results/q1_realign/` only.  
**Not a claim of novelty uniqueness or SOTA.**  
**Evidence sources:** `STEP2_CLAIMS.md`, `fixed_vs_adaptive/`, `ablation/`, `adaptive_attacker/`, `EXPERIMENT_MANIFEST.md`, `REPRODUCIBILITY.md`.

Framing used throughout:

> ADAPTI-GUARD is a runtime discrete intervention policy that dynamically escalates protection under attack pressure and manages protection levels with legitimate-task cost considerations.

Central evaluation story: **Security ↔ Utility ↔ Intervention Cost**.

---

## 1. Research Gap

Existing agent defenses often select a **fixed** intervention intensity (e.g., always allow, always sanitize, always restrict tools, or always block). Under a mixed attack/legitimate workload this creates a hard trade-off:

- Low fixed intensity yields high attack success (Fixed-L0 ASR = 1.00; Fixed-L1 ASR = 0.72).
- Maximum fixed intensity eliminates attacks but collapses legitimate-task success (Fixed-L3 ASR = 0.00, utility = 0.00) at maximum defense cost (0.50).

What remains under-specified in our evaluation setting is not “whether adaptation exists somewhere in the literature,” but whether a **discrete runtime intervention-level controller**—escalating under attack pressure and adjusting levels with legitimate-task cost signals—can occupy a **different security–utility–cost operating point** than fixed levels under a controlled mixed protocol.

This draft does **not** claim that discrete escalate/de-escalate levels are unique to ADAPTI-GUARD, nor that the system is AutoDojo-robust or open-world general.

---

## 2. Contributions

Supported by implementation + `results/q1_realign` experiments:

1. **Adaptive discrete intervention policy.** Levels L0–L3 map to interventions {no intervention, sanitize, tool restriction, block}, with runtime level updates.
2. **Attack-pressure escalation with legitimate-cost-aware de-escalation.** Levels increase after repeated attack successes and may decrease when legitimate-task outcomes indicate costly over-protection (cost gates in the default configuration).
3. **Controlled evaluation of adaptive vs fixed intervention levels under a mixed workload**, with ablations of escalation, de-escalation, and cost gating, plus a separate AdaptiveAttacker-condition evaluation.

**Not contributions (explicitly removed):**

- Historical attack-feedback as a beneficial module (`no_historical` identical to `full`).
- First / SOTA / uniquely adaptive defense.
- Guaranteed security or open-world generalization.
- AutoDojo-class adaptive-attacker robustness.

---

## 3. Methods

### 3.1 Intervention levels

| Level | Action | Nominal cost |
| ----- | ------ | ------------ |
| L0 | A0 no intervention | 0.00 |
| L1 | A1 sanitize | 0.10 |
| L2 | A2 tool restriction | 0.25 |
| L3 | A3 block | 0.50 |

### 3.2 Adaptation rule (default / “full”)

- **Escalate:** on attack success → accumulate; after threshold, `defense_level ← min(3, level+1)`.
- **De-escalate:** on legitimate-task evidence with cost gates (success & cost≥0.25, or failed legitimate & cost≥0.50) → after threshold, `defense_level ← max(0, level−1)`.
- **Maintain:** otherwise.

### 3.3 Important method detail (fairness)

The adaptive policy **blends current risk with `defense_level`** when selecting an action. Fixed baselines force a level→action mapping. Therefore **adaptive L3 is not action-identical to Fixed-L3**: low-risk legitimate episodes under adaptive control often execute as A2 (utility preserved), whereas Fixed-L3 always blocks (utility = 0). This non-isomorphism is reported as a methodological property, not hidden.

### 3.4 Historical signal

A historical attack term exists in risk scoring but is **not** treated as a contribution: ablation `no_historical` matches `full` on primary aggregates.

---

## 4. Experimental Protocol

Protocol (authoritative): **75% attack / 25% legitimate**.

- Schedule: `[attack, attack, attack, legitimate] × 25` (100 episodes).
- Primary attack source: frozen stream slice `common_attack_stream` first 75 records.
- Comparisons: Fixed L0–L3 vs Adaptive (full).
- Ablations (frozen stream): full, no escalation, no de-escalation, no cost gate, no historical.
- Separate AdaptiveAttacker condition: live family-switch attacker under the same schedule (not mixed into frozen primary tables).
- Seeds: 1–3. Pipeline is deterministic given frozen stream+schedule (`std = 0`); this documents reproducibility, **not** stochastic robustness.

Details: `REPRODUCIBILITY.md`, `EXPERIMENT_MANIFEST.md`.

---

## 5. Metrics

Reported jointly (SUC framing):

| Axis | Metrics |
| ---- | ------- |
| Security | ASR |
| Utility | Legitimate-task success |
| Cost / intervention | Mean defense cost; intervention rate; false-intervention rate |
| Adaptivity | Escalation count; de-escalation count; transition count; mean/final defense level |

No latency/token claims are made (not measured in these runs).

---

## 6. Results — Fixed vs Adaptive (frozen stream)

Source: `results/q1_realign/fixed_vs_adaptive/summary.json`

| Method | ASR ↓ | Legit. success ↑ | Mean cost ↓ | Esc. | De-esc. |
| ------ | ----- | ---------------- | ----------- | ---- | ------- |
| Fixed L0 | 1.00 | 1.00 | 0.00 | 0 | 0 |
| Fixed L1 | 0.72 | 1.00 | 0.10 | 0 | 0 |
| Fixed L2 | 0.76 | 1.00 | 0.25 | 0 | 0 |
| Fixed L3 | **0.00** | **0.00** | 0.50 | 0 | 0 |
| Adaptive (full) | **0.373** | **1.00** | 0.329 | 14 | 11 |

**Interpretation (SUC, not domination):**

- Adaptive does **not** beat Fixed-L3 on ASR (0.373 > 0.00).
- Adaptive preserves utility (1.00) while Fixed-L3 destroys utility (0.00).
- Adaptive occupies an intermediate cost (0.329) between Fixed-L2 (0.25) and Fixed-L3 (0.50).
- Observed transitions (↑14 / ↓11) show the policy moves under the mixed workload.

Claim allowed: *under this protocol, adaptive achieves a distinct security–utility–cost operating point versus fixed levels.*  
Claim forbidden: *adaptive is strictly best on security.*

---

## 7. Ablation Analysis

Source: `results/q1_realign/ablation/summary.json` + raw trajectories.

| Condition | ASR | Utility | Mean cost | Esc. | De-esc. | Mean level |
| --------- | --- | ------- | --------- | ---- | ------- | ---------- |
| Full | 0.373 | 1.00 | 0.329 | 14 | 11 | 2.43 |
| No escalation | 0.720 | 1.00 | 0.075 | 0 | 0 | 0.00 |
| No de-escalation | **0.080** | 1.00 | **0.396** | 3 | 0 | **2.70** |
| No cost gate | 0.400 | 1.00 | 0.304 | 15 | 12 | 2.26 |
| No historical | 0.373 | 1.00 | 0.329 | 14 | 11 | 2.43 |

### 7.1 Escalation is necessary for security under this protocol

Without escalation, level stays at 0 (mean level 0.00); ASR rises to **0.72**, matching Fixed-L1-scale under-defense. Utility remains 1.00 at low cost. Escalation is therefore supported as a security-relevant component.

### 7.2 Historical signal is not supported

`no_historical` is identical to `full` on primary metrics. Historical attack feedback is **removed** as a contribution.

### 7.3 Cost gate

Removing the cost gate yields ASR 0.40 (slightly worse than full) with more transitions (27 vs 25). Effect is small under this protocol; we report it as a measured sensitivity, not a large standalone win.

### 7.4 Surprising result: No de-escalation (must not be hidden)

**Observation:** No de-escalation achieves **lower ASR (0.08)** than full (0.373), with utility still 1.00, but **higher mean cost (0.396 vs 0.329)**.

**Trajectory-grounded explanation (measured, not speculative mechanism beyond logs):**

From `raw/ablation_full_seed1_episodes.json` vs `raw/ablation_no_deescalation_seed1_episodes.json`:

| Quantity | Full | No de-escalation |
| -------- | ---- | ---------------- |
| First reach L3 | episode 14 | episode 14 |
| Final level | 3 | 3 |
| Mean level | 2.43 | 2.70 |
| Attack episodes at L3 | 38 | **65** |
| Attack ASR at L3 | 0.00 | 0.00 |
| Attack episodes at L2 | 29 | 2 |
| Attack ASR at L2 | ≈0.83 | 1.00 (n=2) |
| A3 actions (all eps) | 38 | **65** |
| Legitimate actions | mostly A2 (23/25) | mostly A2 (23/25) |

**What the measurements support:**

1. Full adaptive **oscillates** (de-escalations = 11), spending substantial attack time at L2 where attack success is high → overall ASR 0.373.
2. No de-escalation **locks high** after early escalations (only 3 escalations total, then stays), concentrating attack episodes at L3 where attack success is 0 → overall ASR 0.08.
3. Utility remains 1.00 in both because legitimate episodes still predominantly receive **A2**, not A3—consistent with risk–level blending (unlike Fixed-L3, which forces block and yields utility 0).

**What we do *not* claim:**

- That “no de-escalation is better.” It wins on ASR but pays higher mean cost and forgoes the intended cost-management behavior.
- A deeper causal story beyond the logged level/action trajectories.

**SUC reading:** Full vs no-de-escalation is an **observed trade-off**—lower ASR with sustained high level vs higher ASR with cost-reducing oscillation—not a paradox to suppress. De-escalation is justified as a **cost/level-management** mechanism, not as an ASR maximizer.

---

## 8. Adaptive Attacker Evaluation

Source: `results/q1_realign/adaptive_attacker/summary.json`

### 8.1 What AdaptiveAttacker is

- Observes success/fail only.
- On failure: switches attack family (round-robin) and may increase payload sophistication.
- **Not** a multi-turn AutoDojo-style optimizer.

### 8.2 Results (same 75/25 schedule)

| Method | ASR | Utility | Mean cost |
| ------ | --- | ------- | --------- |
| Adaptive (live attacker) | 0.373 | 1.00 | 0.329 |
| Fixed L0 (live) | 1.00 | 1.00 | 0.00 |
| Fixed L1 (live) | 0.987 | 1.00 | 0.10 |
| Fixed L2 (live) | 1.00 | 1.00 | 0.25 |
| Fixed L3 (live) | 0.00 | 0.00 | 0.50 |

Allowed claim: *evaluated under AdaptiveAttacker (family-switch) conditions.*  
Forbidden claim: *robust against AutoDojo / adaptive attackers in general.*

---

## 9. Limitations

1. **MVP heuristics:** regex detector and marker sanitize; results are protocol-internal, not production agent security guarantees.
2. **Fixed vs adaptive action non-isomorphism** due to risk–level blending (Section 3.3).
3. **Attack-heavy mix (75/25)** may favor security-oriented readings; legitimate-heavy sensitivity not claimed here.
4. **Deterministic pipeline (`std=0`)** → reproducibility, not stochastic robustness.
5. **De-escalation does not improve ASR** in the ablation; it manages cost/level occupancy. Papers must not market it as a pure security booster.
6. **AdaptiveAttacker ≠ AutoDojo.**
7. **No unreproducible external baselines** added in this draft.
8. High intervention / false-intervention rates under adaptive (≈0.99 / 0.96) indicate frequent non-A0 actions; discuss as cost/over-intervention axis.

---

## 10. Conclusion

Under a controlled **75% attack / 25% legitimate** protocol, ADAPTI-GUARD’s discrete runtime intervention policy produces a **measurable security–utility–cost operating point**: ASR 0.373 with utility 1.00 and mean cost 0.329, versus Fixed-L3’s ASR 0.00 with utility 0.00. Escalation is necessary to leave the under-defense regime. De-escalation reduces time spent at the highest level and lowers mean cost relative to a no-de-escalation lock-high policy, at the expense of higher ASR—an explicit SUC trade-off evidenced by level trajectories. Historical feedback is unsupported. Evaluation under a family-switch AdaptiveAttacker is reported separately without AutoDojo-robustness claims.

ADAPTI-GUARD should be positioned as a **cost-aware discrete intervention-level controller studied under mixed workloads**, not as a universally superior or uniquely adaptive defense.
