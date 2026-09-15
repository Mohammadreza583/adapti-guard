# Dual-track claims (allowed / forbidden)

**Role:** Exact wording guardrails for Track A (VNEXT FAIL) and Track B (Phase-1 confirm).  
**Authority:** Frozen AUDIT folders win over this file. Companion: [`DUAL_TRACK_STATUS.md`](DUAL_TRACK_STATUS.md), [`PHASE1_SCIENTIFIC_REPORT.md`](PHASE1_SCIENTIFIC_REPORT.md), [`PHASE1_INDEPENDENCE_AUDIT.md`](PHASE1_INDEPENDENCE_AUDIT.md).  
**Not for venue submission author lists / citation formatting.**

---

## Shared non-claims (both tracks)

Do **not** claim:

- State-of-the-art or “prompt injection is solved”
- Production readiness or deployment safety
- That either result generalizes beyond its own pack, target, and judge
- That `target_refusal` / incidental refusal is a defense win
- That a detector hit alone is a defense win
- That Track B reverses Track A, or that Track A invalidates Track B
- That Phase-2 / multi-turn live evaluation has been run (it has not)
- Any external baseline / SOTA comparison (none was run)

---

## Track A — VNEXT (`VNEXT-ADAPT` on `vnext_confirm_v1.0`)

### Allowed

- State that the official confirmation is **FAIL** / qualified win **NO**.
- Quote frozen numbers: B0 ASR 0.9508, treatment ASR 0.8689, δ̂=0.0820, McNemar p=0.0625, U=0.9344, MSID 0.20 not met.
- Call it an **honest negative result** (MSID, significance, and utility gates all failed).
- Note intervention wins used taxonomy `{correct_block, correct_tool_deny}` only; refusals are ties.

### Forbidden

- “VNEXT-ADAPT works / beats B0 / is a useful confirmed defense”
- Relabeling FAIL as PARTIAL, “near miss,” or “marginally significant therefore confirmed”
- Changing MSID or α after unblinding
- Mixing Layer A TEST ASR with VNEXT confirmatory ASR as one unlabeled table

---

## Track B — Phase-1 confirm (`PHASE1-CORE` on `phase1_confirm_v1`)

### Allowed

- State classification **SUPPORTED_IMPROVEMENT** **scoped to** this pack, treatment, target, and judge.
- Quote frozen numbers: B0 harmful-action success 1.000, CORE 0.5574, δ̂=0.4426, b10/b01=27/0, p≈1.49e-08, U≈0.967, MSID PASS, utility ELIGIBLE.
- Note all 27 b10 events are `correct_tool_deny` (not refusals).
- Cite the independence audit: “separate confirmatory pack; episode audit found **no prompt/seed/marker overlap with VNEXT confirm**” (`PHASE1_INDEPENDENCE_AUDIT.md`, verdict **INDEPENDENT** scoped to VNEXT pack text).
- Keep holdout caveat when claiming threat-surface novelty: residual template paraphrase kinship with pilot `phase1_holdout_v1` (exact copies 0; near-pairs >0); episode creation dates UNKNOWN.

### Forbidden

- “VNEXT now works” / “Track A is reversed”
- Claiming **unbounded** independence (e.g. “independent confirmation that VNEXT works,” or ignoring holdout kinship / UNKNOWN dates)
- Claiming generalization beyond `phase1_confirm_v1`
- Counting detector hits or refusals as the primary win mechanism
- Presenting ablations/generalization as primary confirmatory results (they were excluded from the live primary run)

---

## Preferred short dual-track sentence

> Track A (`VNEXT-ADAPT` / `vnext_confirm_v1.0`) is an official FAIL. Track B (`PHASE1-CORE` / `phase1_confirm_v1`) is a separate confirmatory run classified SUPPORTED_IMPROVEMENT on its own pack; an episode-level audit found no prompt/seed/marker overlap with the VNEXT pack (holdout template kinship and missing creation dates remain caveats).
