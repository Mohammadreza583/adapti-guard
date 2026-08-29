# CORPUS ACCESS STOP

| Field | Value |
|-------|-------|
| CORPUS | 0/55 |
| CORPUS STATUS | **FAIL** |
| AUDIT STATUS | **NOT STARTED** (novelty adjudication blocked) |
| WORKSPACE | `/workspace` |
| HOSTNAME | `cursor` (Cursor Cloud Linux VM — **not** user WSL) |
| USER-PROVIDED PATH | `C:\Users\MohammadReza\Desktop\adapti-guard\literature_corpus_55.zip` |
| PROBED EQUIVALENT | `/mnt/c/Users/MohammadReza/Desktop/adapti-guard/literature_corpus_55.zip` → **MISS** |
| `/workspace/literature_corpus_55.zip` | **MISS** |
| `./literature_corpus_55.zip` | **MISS** |
| `/workspace/literature_corpus/` | **MISSING** |
| Canonical TXT COUNT | **0** |
| Workspace `*.txt` (non-corpus) | 2 (`results/q1_realign/STATUS.txt`, `requirements.txt`) |
| EXPECTED | **55** readable canonical TXT papers |

## Why this path cannot work here

This agent runs on a **remote Cursor Cloud VM**. It does **not** have Windows `C:\` or WSL `/mnt/c` mounted. A Desktop path on your machine is invisible until the file is uploaded into `/workspace`.

## Required action (pick one)

1. **Upload the zip into the cloud workspace** as:
   - `/workspace/literature_corpus_55.zip`
2. Or extract locally and sync/upload the folder as:
   - `/workspace/literature_corpus/` containing exactly **55** `.txt` files (expected group layout 15/6/5/9/9/5/6 if that is your canonical structure)

Then re-trigger this audit. Gate:

```
TXT COUNT == 55 AND READABLE == 55  →  proceed with one-shot final audit
else                                 →  STOP again; no novelty claims
```

## Hard rules (unchanged)

- Do **not** invent Direct/Partial competitor counts from memory, Phase11 proxy corpus, filenames, or prior markdown audits.
- Do **not** change code, experiments, or existing `results/q1_realign/` for this literature step.
- If `FINAL_SUMMARY.md` already exists and is valid after a real 55-TXT pass, write `REUSE_STATUS.md` and do not re-analyze.

## Status line

```
CORPUS = 0/55
CORPUS STATUS = FAIL
AUDIT STATUS = NOT STARTED
ZIP FOUND = NO
REQUIRED ACTION = Place literature_corpus_55.zip at /workspace/literature_corpus_55.zip (or extract 55 TXTs into /workspace/literature_corpus/), then re-run
```
