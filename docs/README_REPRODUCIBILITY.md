# Reproducibility Guide

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-core.txt
cp .env.example .env   # set OPENROUTER_API_KEY
export PYTHONPATH=.
```

## Run all experiments

```bash
./run_all_experiments.sh
```

Or individually:

```bash
python scripts/build_benchmark_v3.py
python experiments/EXP001_dataset_analysis/run.py
python experiments/EXP000_api_smoke/run.py
EXP002_MAX_SAMPLES=10 python experiments/EXP002_real_llm_evaluation/run.py
```

## Docker

```bash
docker build -t adapti-guard .
docker run --env-file .env adapti-guard
```

## Provenance per run

`results/experiment_runs/<EXP>/<RUN>/` contains: config.json, environment.json, git_commit.txt, metrics.json, logs.

## Seeds

42, 123, 2024, 31415, 271828 — document statistical unit per `docs/STATISTICAL_PROTOCOL.md` (to add).

## Caching

`.llm_cache/` — report cache_hit in predictions.
