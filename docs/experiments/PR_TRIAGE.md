# Open PR triage (recommendation only)

**Agents do not close, merge, or comment on PRs via API.** This file is a human action list.

Generated on branch `cursor/pr-triage-1411`. Evidence basis:

| Check | Command / source |
| --- | --- |
| Open PR inventory | `gh pr list --state open --limit 200 --json number,title,headRefName,baseRefName,updatedAt` → 47 PRs (#1–#18, #20–#48); plus #49 pre-merge report opened during this close-out |
| Diff vs `main` | `git diff --name-only origin/main...<head>` and `git rev-list --count origin/main..<head>` |
| Ancestry vs reconcile tip | `git merge-base --is-ancestor <head> origin/cursor/reconcile-stacks-1411` (`c7f88b9`) |
| Ancestry vs Stack B completeness tip | `git merge-base --is-ancestor <head> origin/cursor/phase1-completeness-statement-1411` (`0ab6a56`) |
| Content vs prior CLOSE map | `docs/paper/workshop_vnext_fail/PR_STACK.md` (CLOSE/SKIP for #29, #36) |

**Canonical landing tip (pending human merge):** PR **#48** `cursor/reconcile-stacks-1411` @ `c7f88b9` (Stack B science on PR #44 path-fix). Pre-merge verdict: [`RECONCILE_PREMERGE_REPORT.md`](RECONCILE_PREMERGE_REPORT.md) / PR #49.

**Bucket definitions**

| Bucket | Meaning |
| --- | --- |
| `SUPERSEDED` | Content fully included in a later reconciled tip (#48 / #44 / official live path). Close after tip lands. |
| `STILL_RELEVANT` | Unique work not yet on tip / `main`; keep or merge intentionally. |
| `STALE_EXPERIMENT` | Abandoned exploration; nothing worth recovering into the dual-track story. |
| `UNCLEAR` | Diff alone insufficient; needs human context. |

---

## Classification table

| PR | Branch | Updated | Bucket | One-line reason | Recommended human action |
| ---: | --- | --- | --- | --- | --- |
| 1 | `cursor/phase7-mixed-schedule-787e` | 2026-08-29 | STALE_EXPERIMENT | Offline Phase 7 schedule tweak; `results/phase7/*` not in dual-track tip; last touch Aug 29 | Archive branch and close |
| 2 | `cursor/phase8a-multiseed-787e` | 2026-08-29 | STALE_EXPERIMENT | Phase 8A multi-seed on Phase 7 protocol; pre-VNEXT offline stack | Archive branch and close |
| 3 | `cursor/phase8b-analyses-787e` | 2026-08-29 | STALE_EXPERIMENT | Phase 8B ablation/temporal analyses; not ancestor of #48 | Archive branch and close |
| 4 | `cursor/phase8c-robustness-787e` | 2026-08-29 | STALE_EXPERIMENT | Phase 8C robustness; abandoned vs VNEXT FAIL narrative | Archive branch and close |
| 5 | `cursor/phase9-evidence-audit-787e` | 2026-08-29 | STALE_EXPERIMENT | Phase 9 evidence audit on old offline results | Archive branch and close |
| 6 | `cursor/phase10-claim-evidence-787e` | 2026-08-29 | STALE_EXPERIMENT | Phase 10 claim matrix (`results/phase10/`); not on tip | Archive branch and close |
| 7 | `cursor/phase11-manuscript-evidence-787e` | 2026-08-29 | STALE_EXPERIMENT | Phase 11 manuscript evidence package for old stack | Archive branch and close |
| 8 | `cursor/novelty-audit-787e` | 2026-08-29 | STALE_EXPERIMENT | Early novelty audit JSON under `ANALYSIS/`; superseded by later lit work then VNEXT packet | Archive branch and close |
| 9 | `cursor/deep-novelty-verification-787e` | 2026-08-29 | STALE_EXPERIMENT | Deep novelty matrix; Aug 29 only; not in #48 | Archive branch and close |
| 10 | `cursor/phase11-novelty-contribution-787e` | 2026-08-29 | STALE_EXPERIMENT | Contribution audit on same dead-end novelty chain | Archive branch and close |
| 11 | `cursor/full-q1-novelty-audit-787e` | 2026-08-29 | STALE_EXPERIMENT | Full Q1 novelty corpus artifacts; not folded into dual-track docs | Archive branch and close |
| 12 | `cursor/phase11-final-novelty-audit-787e` | 2026-08-29 | STALE_EXPERIMENT | Single-file `results/phase11/final_novelty_audit_v1.json`; absent from #48 | Archive branch and close |
| 13 | `cursor/q1-research-realignment-787e` | 2026-08-29 | STALE_EXPERIMENT | Analysis-only realignment reports under `results/research_realignment/` | Archive branch and close |
| 14 | `cursor/q1-experiment-repair-787e` | 2026-08-29 | STALE_EXPERIMENT | Ends in STOP (`literature_corpus_55.zip` missing on VM); incomplete | Archive branch and close |
| 15 | `cursor/q1-scientific-upgrade-88b3` | 2026-09-06 | STALE_EXPERIMENT | Early EXP000–005 / `benchmark_v4` scaffolding; 69/70 files diverge from #48; replaced by Layer A / VNEXT harness | Archive branch and close |
| 16 | `cursor/unify-judge-system-prompts-c2cf` | 2026-09-07 | SUPERSEDED | Judge SYSTEM/schema unify; `llm_judge.py` continued evolving on #20→#48 (head blob ≠ tip, but intent absorbed) | Close as superseded after #48 merges |
| 17 | `cursor/align-requirements-docs-e2f3` | 2026-09-11 | STILL_RELEVANT | Unique “External tooling scope” (Garak/Inspect optional; LangChain/PyRIT/promptfoo not integrated) — phrase **absent** on #48 (`git grep`) | Cherry-pick tooling-scope wording into README/limitations (portfolio PR), then close |
| 18 | `cursor/layer-a-openrouter-smoke-67a3` | 2026-09-13 | SUPERSEDED | Layer A smoke / attack-pack precursor; tip lineage continues via #20→#48 (7 leftover path blobs are older revisions) | Close as superseded after #48 merges |
| 20 | `cursor/layer-a-v2-fixed-ablation-f6c7` | 2026-09-13 | SUPERSEDED | Ancestor of #48 (`merge-base --is-ancestor`) | Close as superseded after #48 merges |
| 21 | `cursor/layer-a-v3-scientific-recovery-f6c7` | 2026-09-13 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 22 | `cursor/layer-a-v4-project-completion-f6c7` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 23 | `cursor/layer-a-diagnostic-manuscript-692c` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 24 | `cursor/vnext-protocol-phase1-d8c0` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 25 | `cursor/vnext-harness-repair-phase2-9b3f` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 26 | `cursor/vnext-phase3-power-memo-9b3f` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 27 | `cursor/vnext-msid-lock-phase3a-e51b` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 28 | `cursor/vnext-confirm-pack-4d85` | 2026-09-14 | SUPERSEDED | Frozen pack lock; ancestor of #48 | Close as superseded after #48 merges |
| 29 | `cursor/vnext-confirm-live-eval-8dd8` | 2026-09-14 | STALE_EXPERIMENT | Parallel unused runner (`run_vnext_confirm_eval.py`); **no** `20260914-133147` AUDIT; official FAIL is #31 (matches `PR_STACK.md`) | Archive branch and close (do not merge as FAIL) |
| 30 | `cursor/vnext-prelive-checklist-7aef` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 31 | `cursor/vnext-confirm-live-81ad` | 2026-09-14 | SUPERSEDED | Official Track A FAIL AUDIT; ancestor of #48 | Close as superseded after #48 merges |
| 32 | `cursor/vnext-fail-workshop-manuscript-de91` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 33 | `cursor/vnext-fail-workshop-closeout-ef12` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 34 | `cursor/vnext-fail-submission-packet-1411` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 35 | `cursor/phase1-core-defense-upgrade-1411` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 36 | `cursor/phase2-protocol-lock-1411` | 2026-09-14 | SUPERSEDED | Sibling of #37; `PHASE2_*.md` relocated under `docs/experiments/protocols/` by #44 (3/4 blobs identical; PROTOCOL path-fix only) | Close as superseded after #48 merges |
| 37 | `cursor/phase1-final-hardening-1411` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 38 | `cursor/phase1-scientific-hardening-1411` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 39 | `cursor/phase1-confirm-live-run-1411` | 2026-09-14 | SUPERSEDED | Official Track B LIVE; ancestor of Stack B tip; science + AUDIT on #48 via reconcile port (path diffs are tree-standardization) | Close as superseded after #48 merges |
| 40 | `cursor/dual-track-docs-hygiene-60df` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 41 | `cursor/repo-hygiene-start-here-7699` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 42 | `cursor/project-rules-master-prompt-e00d` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 43 | `cursor/tree-standardization-docs-package-954c` | 2026-09-14 | SUPERSEDED | Ancestor of #48 | Close as superseded after #48 merges |
| 44 | `cursor/phase2-protocol-path-fix-26c9` | 2026-09-14 | SUPERSEDED | PR #44 tip `272a37d` is direct parent base of #48 | Close as superseded after #48 merges |
| 45 | `cursor/phase1-independence-audit-1411` | 2026-09-15 | SUPERSEDED | Stack B independence audit; scripts/metrics present on #48 (`same_comp=True` for audit scripts/JSON) | Close as superseded after #48 merges |
| 46 | `cursor/phase1-holdout-overlap-audit-1411` | 2026-09-15 | SUPERSEDED | Holdout forensics; on #48 | Close as superseded after #48 merges |
| 47 | `cursor/phase1-completeness-statement-1411` | 2026-09-15 | SUPERSEDED | 59/59 classification + completeness statement; ported onto #48 | Close as superseded after #48 merges |
| 48 | `cursor/reconcile-stacks-1411` | 2026-09-15 | STILL_RELEVANT | **Merge candidate** — reconciles Stack B onto #44; pre-merge report says SAFE TO MERGE | Review + merge tip (human only); prefer landing #48 once vs merging every ancestor |
| 49 | `cursor/reconcile-premerge-report-1411` | 2026-09-15 | STILL_RELEVANT | Adds `RECONCILE_PREMERGE_REPORT.md` only; stacks on #48 | Merge after or with #48 (docs-only), or squash into #48 before merge |

---

## Counts

| Bucket | Count |
| --- | ---: |
| SUPERSEDED | 31 (#16, #18, #20–#28, #30–#48 except #29/#36 already counted here; wait — see below) |
| STILL_RELEVANT | 3 (#17, #48, #49) |
| STALE_EXPERIMENT | 16 (#1–#15, #29) |
| UNCLEAR | 0 |

Exact counts from table rows: **STALE_EXPERIMENT 16** (#1–#15, #29); **SUPERSEDED 29** (#16, #18, #20–#28, #30–#47); **STILL_RELEVANT 3** (#17, #48, #49); **UNCLEAR 0**. Total classified = **48** open PRs including #49.

---

## Suggested human workflow (no agent execution)

1. Review and merge **#48** (optionally after merging **#49** docs into it).
2. Cherry-pick #17 tooling-scope wording (or accept portfolio README rewrite covering it), then close #17.
3. Bulk-close **SUPERSEDED** PRs as “superseded by #48” (human UI only).
4. Bulk-close **STALE_EXPERIMENT** PRs as abandoned / out of dual-track scope.
5. Do **not** merge #29 as Track A FAIL. Do **not** merge #36 onto Track B after #44/#48 exist.

Cross-check: prior recommendations for #29 and #36 in `docs/paper/workshop_vnext_fail/PR_STACK.md` match this triage.
