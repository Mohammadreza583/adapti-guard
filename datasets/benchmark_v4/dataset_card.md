# benchmark_v4 Dataset Card

## Status
- version: benchmark_v4
- publication_ready: **False**
- balanced_categories: **True**
- total samples: 29

## Splits
| Split | Count |
|-------|------:|
| train | 18 |
| validation | 7 |
| test | 4 |

## Required category coverage
{
  "direct_prompt_injection": 5,
  "indirect_prompt_injection": 5,
  "jailbreak": 3,
  "rag_injection": 5,
  "agent_attacks": 3,
  "tool_attacks": 5,
  "benign_tasks": 3
}

## Sources
{
  "NotInject_train": "DATASET_UNAVAILABLE",
  "NotInject_valid": "DATASET_UNAVAILABLE",
  "BIPIA": "DATASET_UNAVAILABLE",
  "InjecAgent": "DATASET_UNAVAILABLE",
  "TensorTrust": "DATASET_UNAVAILABLE",
  "PIArena": "DATASET_UNAVAILABLE",
  "internal_smoke_v4": "GENERATED_SMOKE_ONLY (81)"
}

## Provenance
Each row includes a `provenance` field. File-level SHA256 in `hashes.json`.

## Warning
If `publication_ready` is false, this bundle is infrastructure/smoke only.
Do not cite as a publication benchmark without external dataset integration.
