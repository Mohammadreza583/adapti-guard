#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=.

echo "=== ADAPTI-GUARD Experiment Runner ==="

python scripts/build_benchmark_v3.py
python experiments/EXP001_dataset_analysis/run.py

if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
  echo "OPENROUTER_API_KEY not set — EXP000/EXP002 will be BLOCKED"
  python experiments/EXP000_api_smoke/run.py || true
else
  python experiments/EXP000_api_smoke/run.py
  EXP002_MAX_SAMPLES="${EXP002_MAX_SAMPLES:-5}" python experiments/EXP002_real_llm_evaluation/run.py
fi

python scripts/init_experiment_stubs.py
echo "=== Complete. See results/ and experiments/registry.csv ==="
