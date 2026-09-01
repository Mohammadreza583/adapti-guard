# Dataset Analysis — benchmark_v3

**Status:** Run `python scripts/build_benchmark_v3.py` to regenerate.  
**Publication ready:** false until external datasets are present.

See `datasets/benchmark_v3/statistics.json` and `dataset_card.md` after build.

## Required categories

1. Direct Prompt Injection  
2. Indirect Prompt Injection  
3. Jailbreak  
4. RAG Injection  
5. Agent Attacks  
6. Tool Attacks  
7. Benign Tasks  

## Policy

- No fabricated real benchmark samples.
- Internal smoke templates labeled `SMOKE_ONLY_NOT_PUBLICATION_EVIDENCE`.
- Exact normalized-text deduplication applied.
- Stratified splits when external data loaded.
