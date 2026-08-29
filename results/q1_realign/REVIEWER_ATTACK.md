# REVIEWER_ATTACK (post-experiment)

Only objections still material after Q1 repair runs. Format: OBJECTION → EVIDENCE → GAP → MINIMUM FIX

## Reviewer A — Novelty

1. **OBJECTION:** Discrete escalate/de-escalate already in SafeHarness.  
   **EVIDENCE:** Prior audit; AG still uses discrete levels.  
   **GAP:** Uniqueness indefensible.  
   **MINIMUM FIX:** KEEP contribution framing as intervention semantics + mixed SUC protocol; no “unique adaptive levels.”

2. **OBJECTION:** Is the protocol novelty enough for Q1?  
   **EVIDENCE:** New fixed-vs-adaptive + ablation package under 75/25.  
   **GAP:** Still methodological/narrow.  
   **MINIMUM FIX:** Honest positioning; emphasize cost-aware de-esc + fixed comparison evidence.

3. **OBJECTION:** Historical memory looked adaptive like AgentAntibody.  
   **EVIDENCE:** `no_historical` identical to `full` (ASR 0.373).  
   **GAP:** None if removed from claims.  
   **MINIMUM FIX:** REMOVE C6 (done in STEP2).

4. **OBJECTION:** AdaptiveAttacker experiment still not AutoDojo.  
   **EVIDENCE:** `adaptive_attacker/summary.json` flags `auto_dojo_class=false`.  
   **GAP:** Overclaim risk if wording sloppy.  
   **MINIMUM FIX:** Say “evaluated under AdaptiveAttacker conditions.”

5. **OBJECTION:** Policy blend means adaptive L3 ≠ fixed L3.  
   **EVIDENCE:** Fixed L3 util=0; adaptive high-level util=1 via LOW-risk→A2 path.  
   **GAP:** Fairness of “same levels” comparison.  
   **MINIMUM FIX:** Disclose isomorphism gap in paper methods.

## Reviewer B — Experiments

1. **OBJECTION:** Missing escalate/de-escalate ablations.  
   **EVIDENCE:** Now present — no_escalation ASR 0.72; no_deescalation ASR 0.08.  
   **GAP:** Closed for minimum Q1.  
   **MINIMUM FIX:** Report table; interpret SUC carefully.

2. **OBJECTION:** No external baselines (SafeHarness/Task Shield/…).  
   **EVIDENCE:** Still absent.  
   **GAP:** Relative ranking limited.  
   **MINIMUM FIX:** Do not fake; optional Spotlighting later only if reproducible.

3. **OBJECTION:** Attack-heavy 75/25 skews utility narrative.  
   **EVIDENCE:** Protocol explicit.  
   **GAP:** Sensitivity unknown.  
   **MINIMUM FIX:** Disclose; optional legitimate-heavy as P2.

4. **OBJECTION:** MVP detector weakens security claims.  
   **EVIDENCE:** Regex detector / marker sanitize.  
   **GAP:** External validity.  
   **MINIMUM FIX:** Scope claims to controlled MVP protocol.

5. **OBJECTION:** Intervention rate ~0.99 looks extreme.  
   **EVIDENCE:** Adaptive intervenes on nearly all episodes once elevated / risk triggers.  
   **GAP:** Over-defense optics.  
   **MINIMUM FIX:** Report false_intervention_rate; discuss policy blend.

## Reviewer C — Reproducibility / stats

1. **OBJECTION:** std=0 sold as robustness.  
   **EVIDENCE:** Deterministic pipeline; seeds 1–3 identical.  
   **GAP:** Statistical narrative.  
   **MINIMUM FIX:** Disclose determinism in REPRODUCIBILITY.md (done).

2. **OBJECTION:** Missing repro doc.  
   **EVIDENCE:** `REPRODUCIBILITY.md` added.  
   **GAP:** Closed.  
   **MINIMUM FIX:** Keep commands/configs synced.

3. **OBJECTION:** Provenance of new vs old results unclear.  
   **EVIDENCE:** Separate `results/q1_realign/` + manifest.  
   **GAP:** Closed if paper cites paths.  
   **MINIMUM FIX:** Cite manifest IDs.

4. **OBJECTION:** TOTAL-- TXT still not in VM.  
   **EVIDENCE:** Absent.  
   **GAP:** Camera-ready lit completeness.  
   **MINIMUM FIX:** Mount corpus before submission.

5. **OBJECTION:** Code version for new runs vs frozen Phase7.  
   **EVIDENCE:** Manifest stores `code_version` hash; Phase7 untouched.  
   **GAP:** Minor.  
   **MINIMUM FIX:** State both hashes in paper appendix.
