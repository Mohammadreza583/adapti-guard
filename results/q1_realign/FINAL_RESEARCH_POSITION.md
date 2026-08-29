# FINAL_RESEARCH_POSITION

1. **Problem:** Agent defenses must trade security, utility, and intervention cost as attack pressure and legitimate traffic mix.
2. **Existing limitation:** Static levels over-defend (Fixed-L3 util collapse) or under-defend (Fixed-L0/L1); prior adaptive systems adapt different objects (memory, detectors, privileges, weights).
3. **Research gap:** Controlled evaluation of discrete sanitize/restrict/block intervention levels with attack escalation and legitimate-cost-aware de-escalation versus fixed levels under mixed workloads — without claiming unique adaptive levels or AutoDojo-class robustness.
4. **ADAPTI-GUARD contribution:** MVP L0–L3 controller + cost-aware escalate/de-escalate + mixed 75/25 fixed-vs-adaptive SUC evaluation, now with escalate/de-escalate/cost-gate ablations and a separate AdaptiveAttacker-condition run.
5. **Genuine novelty:** Methodological/protocol package and cost-aware de-escalation under mixed workload (partial vs SafeHarness semantics). Not absolute algorithmic uniqueness.
6. **Non-novel aspects:** Discrete escalate/de-escalate idea; SUC axes; runtime adaptive defenses elsewhere; adaptive attackers as eval concept.
7. **Evaluation hypothesis:** Under 75/25, full adaptive yields a SUC point with util=1.0 and ASR≈0.37 vs Fixed-L3 ASR=0/util=0; removing escalation worsens ASR; removing de-escalation lowers ASR but changes cost dynamics; historical signal remains null.
8. **New evidence required (optional next):** legitimate-heavy sensitivity; reproducible light external baseline; stronger adaptive attacker only if claiming it.
9. **Remaining risks:** Policy-level≠fixed-level action isomorphism; MVP detector validity; SafeHarness novelty pressure; missing TOTAL-- in env; overclaim if AutoDojo wording returns.
