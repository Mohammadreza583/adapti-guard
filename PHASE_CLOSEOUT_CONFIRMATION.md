# PHASE_CLOSEOUT_CONFIRMATION

**Report-only.** No merges, closes, comments-to-close, force-pushes, or pushes to `main` were performed by this verification. No LLM evals (API=0). No retune. No Results edits.

- **Repo:** https://github.com/Mohammadreza583/adapti-guard
- **Verified at (UTC):** 2026-09-15
- **Human claim:** merged `#48 → #49 → #51 → #50` and closed 44 triaged PRs (`STALE_EXPERIMENT` + `SUPERSEDED` from `docs/experiments/PR_TRIAGE.md`); `#29` excluded.
- **Triage source:** not on `main`; read from PR **#50** tip `origin/cursor/pr-triage-1411` (`docs/experiments/PR_TRIAGE.md`).

---

## 1) Tip + merge status

### Default branch (`main`) after `git fetch origin main`

| Field | Value |
| --- | --- |
| `git log -1 --oneline` | `5a76848 Revise README for improved clarity and structure` |
| Short SHA | `5a76848` |
| Full SHA | `5a7684835fe57303f7786c51719973ea168c1210` |
| Author date | 2026-09-06 17:10:46 +0330 |
| Working tree vs HEAD | clean (`git status` empty; `git diff` empty) |

`origin/main` did **not** move as a result of the claimed merges. Tip is unchanged from the README-revision commit.

### Merge table (#48 / #49 / #50 / #51)

`gh pr view` + `gh pr list --state merged --limit 20` (only merged PR in repo history: **#19**).

| PR | Title | State | Base → head | Merge commit | Merged at | Merge order on `main` |
| ---: | --- | --- | --- | --- | --- | --- |
| 48 | Reconcile Stack B audits onto PR #44 path-fix base | **OPEN** | `cursor/phase2-protocol-path-fix-26c9` → `cursor/reconcile-stacks-1411` @ `c7f88b9` | none | — | **not merged** |
| 49 | docs: RECONCILE_PREMERGE_REPORT — SAFE TO MERGE verdict | **OPEN** | `cursor/reconcile-stacks-1411` → `cursor/reconcile-premerge-report-1411` @ `2025c14` | none | — | **not merged** |
| 50 | docs: PR_TRIAGE — classify ~48 open PRs for human close/merge | **OPEN** | `cursor/reconcile-stacks-1411` → `cursor/pr-triage-1411` @ `be85756` | none | — | **not merged** |
| 51 | chore: portfolio hygiene — imports, CI, README, staged venv cleanup | **OPEN** | `cursor/reconcile-stacks-1411` → `cursor/portfolio-hygiene-1411` @ `6daa26d` | none | — | **not merged** |

**Merge-order note (stacking vs landing):**

- Claimed linear land onto `main` (`#48→#49→#51→#50`) is **not** visible: zero merge commits for these PRs; `main` does not contain `#48` (`git merge-base --is-ancestor c7f88b9 origin/main` → **NO**).
- GitHub bases: `#49`, `#50`, and `#51` each target `#48`’s branch in **parallel**, not a chain `#49→#51→#50`.
- Git ancestry (unmerged heads only): `#49` / `#50` / `#51` heads **are** descendants of `#48` tip `c7f88b9`. `#48` **is** a descendant of `origin/main` (unmerged work sitting on top of current `main`).
- Mergeability at check time: `#48`/`#49`/`#50` `MERGEABLE`/`CLEAN`; `#51` `MERGEABLE`/`UNSTABLE` (CI failing). Issue comments on all four: **0**.

### `gh pr list --state merged --limit 20`

Only:

| PR | Title | Merged | Merge commit |
| ---: | --- | --- | --- |
| 19 | Layer A attack pack v2: real PI mixed eval + B0 probe wiring | 2026-09-13T20:20:25Z | `cde70eaf0289feeb3ddac0633ecc90f897622921` |

---

## 2) #29 status

| Field | Fact |
| --- | --- |
| Number | 29 |
| Title | VNEXT confirmation LIVE eval (B0 vs VNEXT-ADAPT) |
| State | **OPEN** (not closed, not merged) |
| `closedAt` | `null` |
| `mergedAt` | `null` |
| `mergeCommit` | `null` |
| Base → head | `cursor/vnext-confirm-pack-4d85` → `cursor/vnext-confirm-live-eval-8dd8` |
| Issue comments | **[]** (none) |
| Reviews | **[]** (none) |
| Issue events | one `referenced` by `cursor[bot]` at 2026-09-14T22:20:06Z — **not** a close |
| Closing reason / close comment | **none found** |

No assumption about dossier options. `#29` was **not** closed as part of this closeout.

---

## 3) Closed-count audit

### Expected 44 (`STALE_EXPERIMENT` + `SUPERSEDED`, excluding `#29`)

From `docs/experiments/PR_TRIAGE.md` on `origin/cursor/pr-triage-1411`:

| Bucket | Count in triage | PRs | This audit |
| --- | ---: | --- | --- |
| `STALE_EXPERIMENT` | 16 | `#1`–`#15`, `#29` | exclude `#29` → **15** expected closes |
| `SUPERSEDED` | 29 | `#16`, `#18`, `#20`–`#28`, `#30`–`#47` | **29** expected closes |
| **Expected closes** | | | **44** |
| `STILL_RELEVANT` | 3 | `#17`, `#48`, `#49` | not in the 44 |
| `#50` / `#51` | opened during/after triage | not in the 44 | |

**Expected-44 set:** `#1`–`#15`, `#16`, `#18`, `#20`–`#28`, `#30`–`#47`.

### Actual closed (`gh pr list --state closed --limit 60`)

Closed count = **1**. Open count = **50**.

| PR | State | In expected-44? |
| ---: | --- | --- |
| 19 | MERGED 2026-09-13 | **no** (already merged before triage; not in `PR_TRIAGE.md`) |

### Cross-check

**Of the expected 44, NOT closed (all 44 still OPEN):**

`#1` `#2` `#3` `#4` `#5` `#6` `#7` `#8` `#9` `#10` `#11` `#12` `#13` `#14` `#15` `#16` `#18` `#20` `#21` `#22` `#23` `#24` `#25` `#26` `#27` `#28` `#30` `#31` `#32` `#33` `#34` `#35` `#36` `#37` `#38` `#39` `#40` `#41` `#42` `#43` `#44` `#45` `#46` `#47`

**Closed PRs outside the expected-44 list:** `#19` only. Note only — **not reopened**. This is a **pre-closeout** merge (2026-09-13), not an extra close from this claimed bulk-close.

**`#29`:** excluded from expected-44; remains **OPEN** (see §2).

| Metric | Claimed | Actual |
| --- | ---: | ---: |
| Expected-44 closed | 44 | **0** |
| `#29` closed | no (excluded / handled separately) | still OPEN (matches “do not assume closed”) |

---

## 4) FINAL VERIFICATION CHECKLIST

Verification target = **default-branch tip** `5a76848` (`origin/main`), because the claimed merge tip does not exist on `main`. Unmerged `#48`/`#51` facts are quoted only where needed to compare known AUDIT/lock numbers; they are **not** on `main`.

### 4.1 Fresh venv + `pip install -e .` + import — **FAIL**

Commands:

```text
python -m venv /tmp/ag_closeout
/tmp/ag_closeout/bin/pip install -e /workspace
```

| Step | Result |
| --- | --- |
| First `python -m venv` | failed (`ensurepip` missing); remediated with `python3.12-venv` **in the VM only**, then venv created |
| `pip install -e .` | **FAIL:** `file:///workspace does not appear to be a Python project: neither 'setup.py' nor 'pyproject.toml' found.` |
| `from adapti_guard.runtime import AdaptiGuard` after failed install | **FAIL:** `ModuleNotFoundError: No module named 'adapti_guard'` |
| Same import with `PYTHONPATH=/workspace/src` (not the requested install path) | succeeds (`<class 'adapti_guard.runtime.AdaptiGuard'>`) — **not** a pass for the checklist item |

`pyproject.toml` exists on unmerged `#48`/`#51` (`package-dir = {"" = "src"}`) but **not** on `main`.

### 4.2 `pytest -q` full suite vs prior ~250 — **FAIL**

Full suite on `main` (`/tmp/ag_closeout/bin/pytest -q`, after installing `requirements-core.txt` into the venv so pytest could run at all):

```text
ERROR tests/test_artifact_standard.py - IndexError: 5
Interrupted: 1 error during collection
1 error in 0.28s
```

Cause: `src/adapti_guard/experiments/artifact_standard.py` uses `Path(__file__).resolve().parents[5]` which raises `IndexError: 5` at this checkout depth.

| Run | passed | failed | skipped | errors | vs ~250 |
| --- | ---: | ---: | ---: | ---: | --- |
| Full suite (`pytest -q`) | 0 collected | — | — | **1** (collection) | **FAIL** (not ~250 green) |
| Extra (not checklist): `--ignore=tests/test_artifact_standard.py` | **120** | 0 | 0 | 0 | still far below ~250 |

No live LLM tests were enabled (`RUN_LLM_TESTS` unset; API=0).

### 4.3 AUDIT freeze (`datasets/frozen`, `experiments/real_llm_eval`) — **PASS** (tree vs HEAD) / **FAIL** (Track A/B artifacts on `main`)

| Check | Result |
| --- | --- |
| `git status --porcelain datasets/frozen experiments/real_llm_eval` | empty |
| `git diff origin/main -- datasets/frozen experiments/real_llm_eval` | empty |
| `datasets/frozen/eval_v1/dataset.jsonl` sha256 | `27b1733cb6678e6144687b60387b564bd248c89871042eef0ffb0e2ce4c54c24` — **matches** README lock on `main` |
| Track A/B frozen packs + AUDIT.md on `main` | **absent** (`datasets/frozen/` on `main` is only `eval_v1`; no `VNEXT_CONFIRM/` or `PHASE1_CONFIRM/` under `experiments/real_llm_eval/`) |

Working tree is unmodified vs HEAD (**no freeze drift introduced by this agent**). The dual-track freeze corpus is **not present on `main`**, so a post-merge freeze confirmation against VNEXT/Phase-1 locks **cannot pass on the default branch**.

On unmerged `#48` (not landed): `eval_v1` blob SHA matches `main` (`2227110f…`); VNEXT pack `523c8818…721518`; Phase-1 confirm pack `c789811a…536d01`. Those files were **not** mutated here (API=0; no Results edits).

### 4.4 Track A / Track B AUDIT.md key numbers — **FAIL** on `main`; numbers **match known** on unmerged `#48`

On `main`: Track A and Track B `AUDIT.md` paths **do not exist** → cannot confirm unchanged vs known on the merge tip.

Quoted from unmerged `#48` (`origin/cursor/reconcile-stacks-1411`) — **not rewritten**:

**Track A** `experiments/real_llm_eval/VNEXT_CONFIRM/20260914-133147/AUDIT.md`

- `STATUS: FAIL`; Qualified win (H1): NO
- B0 ASR **0.9508** (≈0.951); VNEXT-ADAPT ASR **0.8689** (≈0.869)
- McNemar exact two-sided **p = 0.0625**
- b10/b01 = 5/0; δ̂ = 0.0820 vs MSID 0.20 NOT MET; U = 0.9344

**Track B** `experiments/real_llm_eval/PHASE1_CONFIRM/phase1_confirm_20260914T213022Z_a2681e92/AUDIT.md`

- Classification: **`SUPPORTED_IMPROVEMENT`**
- B0 harmful-action success: 1.0000; PHASE1-CORE: 0.5574; rate effect 0.4426
- b10/b01: 27/0; McNemar p = 1.49012e-08; MSID **PASS**; utility CORE ELIGIBLE (0.9672…)

These match the known values. They are **not on `main`**.

### 4.5 Detector lock sha256 — **FAIL** on `main` (files absent)

On `main`: no `configs/phase1_detector_lock.json`, no `prompt_injection_detector_phase1.py`.

On unmerged `#48` (pre-hygiene), file sha256 **matches** lock JSON (no `prior_sha256` fields):

| File | Computed sha256 | Lock `sha256` |
| --- | --- | --- |
| `src/adapti_guard/detector/prompt_injection_detector_phase1.py` | `e02f3c64aa563bccc815444f672bbced753d4685e7fbc16dc31a93bd41b189a3` | same |
| `src/adapti_guard/risk/risk_engine_core.py` | `0f447ee23c4d3106e57baefa11869a4c43913264b5efa451c6c5a2ea3723b1b2` | same |
| `src/adapti_guard/policy/core_policy.py` | `763d9ce7ff9f48c9c5fc4a6352638b037a2b768b9ea6fc86601dc5da8a155b82` | same |

On unmerged `#51` (import-rename hygiene; **not merged**), computed hashes match **new** `sha256` fields; `prior_sha256` retains the `#48` / Track B AUDIT hashes above. That lock is **not** on `main`.

### 4.6 CI status on merge tip commit — **FAIL** (no checks on `main` tip)

| Target | Result |
| --- | --- |
| `gh run list --branch main` | **empty** |
| Checks on `5a7684835fe57303f7786c51719973ea168c1210` | `total_count=0` statuses; `total=0` check-runs |
| Combined status API | `state=pending` with **no** statuses (no CI attached) |

Latest Actions runs (all on unmerged `#51` branch `cursor/portfolio-hygiene-1411`, **not** `main`):

| Run | Event | Head | Conclusion |
| --- | --- | --- | --- |
| [34953839328](https://github.com/Mohammadreza583/adapti-guard/actions/runs/34953839328) | pull_request | `6daa26d7` | **failure** |
| [34953836142](https://github.com/Mohammadreza583/adapti-guard/actions/runs/34953836142) | push | `6daa26d7` | **failure** |
| [34953536171](https://github.com/Mohammadreza583/adapti-guard/actions/runs/34953536171) | pull_request | `52307f02` | **failure** |
| [34953520403](https://github.com/Mohammadreza583/adapti-guard/actions/runs/34953520403) | push | `52307f02` | **failure** |

Install step error on latest: `No matching distribution found for numpy>=2.5.2` on GitHub-hosted Python **3.11** (`numpy>=2.5.2` requires Python ≥3.12).

### 4.7 README badge + workflow — **FAIL** on `main`

| Check | `main` (`5a76848`) | Unmerged `#51` (not landed) |
| --- | --- | --- |
| CI badge markdown in README | **absent** | present: `[![Tests](https://github.com/Mohammadreza583/adapti-guard/actions/workflows/tests.yml/badge.svg)](...)` |
| `.github/workflows/tests.yml` in tree | **absent** (no `.github/`) | present (`name: tests`) |
| Workflow registered on GitHub | `tests` **active** (because `#51` PR introduced it) | same |
| Latest run green? | no runs on `main` | **no** — latest `#51` runs **red** |

---

## 5) Checklist scoreboard

| # | Item | Pass/Fail |
| ---: | --- | --- |
| 1 | `#48/#49/#50/#51` merged to `main` in claimed order | **FAIL** (all OPEN; `main` still `5a76848`) |
| 2 | `#29` handled/closed separately as claimed context | **OPEN**; no close comment (fact only) |
| 3 | 44 STALE+SUPERSEDED (excl. `#29`) closed | **FAIL** (0/44 closed) |
| 4.1 | Fresh venv + `pip install -e .` + import | **FAIL** |
| 4.2 | `pytest -q` full suite ~250 | **FAIL** (collection error; 0 collected) |
| 4.3 | AUDIT freeze dirs clean vs HEAD | **PASS** (clean); dual-track freeze **missing on main** |
| 4.4 | Track A/B AUDIT numbers on tip | **FAIL** (files absent on `main`; match known on unmerged `#48`) |
| 4.5 | Detector lock hashes on tip | **FAIL** (absent on `main`) |
| 4.6 | CI green on merge tip | **FAIL** (no checks on `5a76848`; `#51` CI red) |
| 4.7 | README CI badge + green workflow | **FAIL** (no badge/workflow on `main`; latest workflow run red) |

---

## 6) Final verdict

# **BLOCKING ITEMS**

1. **Claimed merges did not happen.** `#48`, `#49`, `#50`, `#51` are all **OPEN**. `main` tip remains `5a76848`. No merge commits; claimed order `#48→#49→#51→#50` is not visible on the default branch.
2. **Claimed 44 closes did not happen.** All 44 `STALE_EXPERIMENT`+`SUPERSEDED` PRs (excluding `#29`) remain **OPEN**. Only closed PR is historical **#19** (merged 2026-09-13, outside the 44).
3. **`#29` is still OPEN** with no closing comment/reason.
4. **Default-branch packaging/tests/CI/badge/AUDIT locks from the dual-track stack are not on `main`.** `pip install -e .` fails; full `pytest -q` collection-errors; no Track A/B AUDIT.md; no detector lock files; no README badge; no CI on tip `5a76848`.
5. **Even the unmerged hygiene PR `#51` does not have green CI** (`numpy>=2.5.2` vs Python 3.11). Landing it as-is would not satisfy “latest run green.”

This verification did not merge, close, comment, force-push, or push to `main`.
)
