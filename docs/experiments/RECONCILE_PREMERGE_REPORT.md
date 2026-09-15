# Reconcile pre-merge verification report

**Subject branch:** `cursor/reconcile-stacks-1411` @ `c7f88b9`  
**Base (PR #44 tip):** `cursor/phase2-protocol-path-fix-26c9` @ `272a37d`  
**Report date (UTC):** 2026-09-15  
**API calls:** 0  
**Frozen dirs:** read-only; see §4

---

## 1. Ancestor check

Command:

```bash
git merge-base --is-ancestor origin/cursor/phase2-protocol-path-fix-26c9 origin/cursor/reconcile-stacks-1411
```

**Result:** success (exit 0). PR #44 tip `272a37d` **is** an ancestor of reconcile `c7f88b9`.  
PR #44 tip has **not** moved past the cut used by this reconcile branch (fetched tip still `272a37d`). **No rebase flag.**

---

## 2. Audit script re-runs (clean re-execution)

| Script | Observed | Documented expectation | Match? |
|--------|----------|------------------------|--------|
| `scripts/audit_phase1_confirm_independence.py` | VNEXT exact_prompt=**0**, near=**0** | 0 / 0 | **YES** |
| `scripts/audit_phase1_holdout_overlap_origin.py` | near-pairs=**59** | 59 | **YES** |
| `scripts/classify_phase1_holdout_pairs_full59.py` | ENTITY=**35**, WORDING=**24**, GENUINE=**0** | 35 / 24 / 0 | **YES** |

Artifacts refreshed under `docs/paper/dual_track/artifacts/` by the scripts; counts unchanged vs prior documentation.

---

## 3. Full test suite

**Path-depth note:** `tests/test_artifact_standard.py` imports `artifact_standard.py`, which uses `Path(__file__).parents[5]`. Under shallow `/workspace/...` this raises `IndexError: 5` at collection and aborts the suite. Under a deeper worktree path (`/tmp/recwt/...`, `/tmp/pr44wt/...`) collection succeeds. This is an **environment path-depth** issue in existing helper code, not reconcile-introduced content.

Comparable full runs (deep worktrees):

| Tree | Command | Result |
|------|---------|--------|
| PR #44 tip @ `272a37d` (`/tmp/pr44wt`) | `pytest tests/ -q` | **248 passed, 2 failed** |
| Reconcile @ `c7f88b9` (`/tmp/recwt`) | `pytest tests/ -q` | **248 passed, 2 failed** |

**Failing tests (identical on both trees):**

1. `tests/test_gemini_provider.py::test_gemini_generate_uses_interactions_api` — `ModuleNotFoundError: No module named 'google'`
2. `tests/test_gemini_provider.py::test_gemini_retries_429_using_retry_after` — same

**Classification:** pre-existing / environment (missing optional `google` package). **Not introduced by reconciliation.** Out of scope as a merge blocker for this docs/reconcile PR.

Shallow `/workspace` run without ignoring collectors: collection ERROR on `test_artifact_standard.py` (same helper `parents[5]` issue). With `--ignore=tests/test_artifact_standard.py`: same 2 gemini failures + 245 passed (3 artifact tests not run).

---

## 4. Frozen-dir integrity

```bash
git diff --name-only origin/cursor/phase2-protocol-path-fix-26c9...HEAD -- datasets/frozen experiments/real_llm_eval
```

**Result:** empty (0 files). **Zero diff** on `datasets/frozen/**` and `experiments/real_llm_eval/**` vs PR #44 tip.

---

## 5. Dangling internal links (`docs/`)

Scanned all `docs/**/*.md` (and similar) for markdown links to relative paths; resolved against link source and repo root.

**Result:** **none found** (count = 0).

---

## 6. Collision-file spot-check (not one-sided overwrite)

Compared merged files on HEAD to Stack A (`origin/cursor/phase2-protocol-path-fix-26c9`) and Stack B (`origin/cursor/phase1-completeness-statement-1411`) originals.

| File | Distinctive A content still present | Distinctive B content still present |
|------|-------------------------------------|-------------------------------------|
| `CLAIMS_DUAL_TRACK.md` | `A-FAIL-1`, workshop `CLAIMS_MAP.md`, Headline set D | independence/holdout audits, `SHARED_TEMPLATE_FAMILY`, `NOT_USED_IN_TUNING` |
| `DUAL_TRACK_STATUS.md` | workshop map, `PR_STACK.md`, “No merge. No venue submit” | holdout audit pointer, 95% CI |
| `docs/paper/dual_track/README.md` | `RELEASE_NEXT_FA.md`, `START_HERE.md` | completeness + independence links |
| `docs/experiments/MASTER_PROMPT.md` | `.cursor/rules` mirror note, `DUAL_TRACK_STATUS` first-read | 10-rule body (`FROZEN MEANS FROZEN`, label blindness, qualified-win) |

**Result:** additive merge preserved; no silent one-sided overwrite detected.

---

## Verdict

**SAFE TO MERGE** (docs/reconcile PR onto PR #44 tip; gemini/`google` and shallow-path `parents[5]` issues are pre-existing/environment and unchanged vs PR #44 tip).
