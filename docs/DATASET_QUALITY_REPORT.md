# Dataset Quality Report — benchmark_v4

**Date:** 2026-09-01  
**Dataset version:** benchmark_v4  
**Builder:** `scripts/build_benchmark_v4.py`

---

## Executive summary

| Property | Value |
|----------|-------|
| publication_ready | false (smoke data) |
| balanced_categories | true |
| train/val/test split | yes |
| deduplication | exact normalized prompt |
| SHA256 hashes | `datasets/benchmark_v4/hashes.json` |
| provenance per row | yes |

---

## Category coverage

benchmark_v4 requires all seven categories:

1. Direct Prompt Injection
2. Indirect Prompt Injection
3. Jailbreak
4. RAG Injection
5. Agent Attacks
6. Tool Attacks
7. Benign Tasks

When external datasets (NotInject, BIPIA, InjecAgent, TensorTrust, PIArena) are unavailable, the builder generates **smoke templates** plus internal attack-stream samples. These are explicitly labeled `SMOKE_ONLY_NOT_PUBLICATION_EVIDENCE`.

---

## Data quality checks

| Check | Status |
|-------|--------|
| Duplicate removal | PASS |
| Category balance (smoke) | PASS (≥3 per category) |
| Train/test separation | PASS (stratified by category) |
| Label consistency | PASS (label 0/1 aligned with category) |
| Provenance metadata | PASS |
| File integrity hashes | PASS |

---

## Limitations

1. **No external benchmark integration** in current clone — cannot claim NotInject/BIPIA-scale evaluation
2. **Smoke samples are templated** — not representative of real-world attack diversity
3. **No human annotation audit** — labels are rule-based from source metadata
4. **Test set size** is insufficient for publication (target: ≥500 test samples)

---

## Integration instructions

Place external datasets at paths referenced in `scripts/build_benchmark_v4.py`:

```
dataset/processed/NotInject/train_final.json
dataset/raw/NotInject/datasets/valid.json
BIPIA/
dataset/raw/InjecAgent/
dataset/raw/TensorTrust/
dataset/raw/PIArena/
```

Then rebuild:

```bash
python scripts/build_benchmark_v4.py
```

Verify `publication_ready: true` in `datasets/benchmark_v4/statistics.json`.

---

## Honest claim policy

Do **not** cite benchmark_v4 as a publication dataset until `publication_ready` is true and sample counts meet the protocol in `docs/Q1_IMPROVEMENT_TRACKER.md`.
