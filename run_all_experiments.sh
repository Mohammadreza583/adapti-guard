#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=.

echo "=== ADAPTI-GUARD Q1 Experiment Runner ==="
echo "Git commit: $(git rev-parse HEAD 2>/dev/null || echo UNKNOWN)"
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Phase 2: Build benchmark_v4
python3 scripts/build_benchmark_v4.py
python3 scripts/build_benchmark_v3.py  # legacy compatibility

# Dataset analysis
python3 experiments/EXP001_dataset_analysis/run.py

# Train ML detector on benchmark_v4 (if train split exists)
python3 -c "
from src.adapti_guard.detectors.ml_detector import train_ml_detector_from_benchmark
import json
print(json.dumps(train_ml_detector_from_benchmark(), indent=2))
" || true

# API-dependent experiments
if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
  echo "OPENROUTER_API_KEY not set — EXP000/EXP002/EXP003 will be BLOCKED"
  python3 experiments/EXP000_api_smoke/run.py || true
  python3 experiments/EXP002_real_llm_evaluation/run.py || true
  python3 experiments/EXP003_baseline_comparison/run.py || true
else
  python3 experiments/EXP000_api_smoke/run.py
  EXP002_MAX_SAMPLES="${EXP002_MAX_SAMPLES:-5}" python3 experiments/EXP002_real_llm_evaluation/run.py
  EXP003_MAX_SAMPLES="${EXP003_MAX_SAMPLES:-5}" python3 experiments/EXP003_baseline_comparison/run.py
fi

# Offline-capable experiments
python3 experiments/EXP004_adaptive_controller/run.py
python3 experiments/EXP005_rag_security/run.py
python3 experiments/EXP006_agent_security/run.py
python3 experiments/EXP007_ablation/run.py

echo "=== Complete. See results/ and experiments/registry.csv ==="
