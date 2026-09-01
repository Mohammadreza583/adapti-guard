#!/usr/bin/env python3
"""EXP002 — Real LLM end-to-end evaluation (judge-based ASR)."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv()

from src.adapti_guard.evaluation.experiment_logging import (
    ExperimentRunContext,
    git_commit,
    sha256_file,
    update_registry_row,
)
from src.adapti_guard.evaluation.llm_judge import LLMJudge
from src.adapti_guard.evaluation.metrics import asr_with_ci, compute_extended_metrics
from src.adapti_guard.evaluation.real_llm_pipeline import RealLLMEvaluationPipeline
from src.adapti_guard.evaluation.target_model import build_target_model, load_model_config

EXPERIMENT_ID = "EXP002"
MAX_SAMPLES = int(os.getenv("EXP002_MAX_SAMPLES", "5"))
TARGET_MODELS = os.getenv("EXP002_TARGET_MODELS", "gpt4o_mini").split(",")
BENCHMARK = ROOT / "datasets" / "benchmark_v4"


def load_test_samples(limit: int) -> list[dict]:
    path = BENCHMARK / "test.jsonl"
    if not path.exists():
        # Fallback to v3
        path = ROOT / "datasets/benchmark_v3/test.jsonl"
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows[:limit]


def pipeline_row(result) -> dict:
    return {
        "sample_id": result.sample_id,
        "label": result.label,
        "category": result.category,
        "attack_present": result.label == 1,
        "attack_success": result.outcome.attack_success,
        "legitimate_task": result.label == 0,
        "legitimate_success": result.outcome.legitimate_success,
        "detection_score": result.detection_score,
        "defense_action": result.defense_action,
        "latency_ms": sum(result.latency_ms.values()) if result.latency_ms else 0,
        "token_usage": result.token_usage,
        "security_score": result.outcome.security_score,
        "utility_score": result.outcome.utility_score,
        "defense_cost": result.outcome.defense_cost,
        "evaluation_mode": result.evaluation_mode,
    }


def main() -> int:
    out = ROOT / "results" / "EXP002"
    out.mkdir(parents=True, exist_ok=True)
    logs: list[dict] = []

    if not os.getenv("OPENROUTER_API_KEY"):
        status = "BLOCKED"
        payload = {
            "status": status,
            "reason": "missing_api_key",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "git_commit": git_commit(),
        }
        (out / "metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
        (out / "config.json").write_text(json.dumps({
            "experiment": EXPERIMENT_ID,
            "max_samples": MAX_SAMPLES,
            "target_models": TARGET_MODELS,
            "benchmark": str(BENCHMARK),
        }, indent=2), encoding="utf-8")
        (out / "logs.json").write_text(json.dumps({"events": [payload]}, indent=2), encoding="utf-8")
        with ExperimentRunContext.create(EXPERIMENT_ID, config={"reason": "missing_api_key"}) as ctx:
            ctx.write_metrics(payload)
            update_registry_row(ROOT / "experiments/registry.csv", {
                "experiment_id": EXPERIMENT_ID, "run_id": ctx.run_id, "status": status,
            })
        print(json.dumps(payload))
        return 2

    samples = load_test_samples(MAX_SAMPLES)
    if not samples:
        status = "BLOCKED"
        payload = {"status": status, "reason": "no_test_samples"}
        (out / "metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(json.dumps(payload))
        return 2

    cfg = load_model_config()
    dataset_hash = sha256_file(BENCHMARK / "test.jsonl") if (BENCHMARK / "test.jsonl").exists() else ""
    all_metrics: dict[str, dict] = {}

    for model_key in TARGET_MODELS:
        model_key = model_key.strip()
        logs.append({"event": "start_model", "model_key": model_key})
        target = build_target_model(model_key)
        judge = LLMJudge(build_target_model("judge"))
        pipeline = RealLLMEvaluationPipeline(target, judge, defense_level=1)

        results = []
        predictions = []
        for row in samples:
            r = pipeline.run_sample(
                sample_id=row["id"],
                prompt=row["prompt"],
                label=int(row["label"]),
                category=row["category"],
                attack_type=row.get("attack_type", row["category"]),
            )
            results.append(pipeline_row(r))
            predictions.append({
                "sample_id": r.sample_id,
                "model_key": model_key,
                "prompt": r.prompt[:500],
                "target_response": r.target_response[:2000],
                "judge": r.judge_verdict.to_dict() if r.judge_verdict else None,
                "attack_success": r.outcome.attack_success,
            })
            logs.append({"event": "sample_done", "sample_id": row["id"], "model": model_key})

        metrics = compute_extended_metrics(results)
        metrics.update(asr_with_ci(results))
        metrics["status"] = "DONE"
        metrics["n_samples"] = len(samples)
        metrics["target_model"] = cfg["models"][model_key]["model"]
        metrics["judge_model"] = cfg["models"]["judge"]["model"]
        all_metrics[model_key] = metrics

        model_out = out / model_key
        model_out.mkdir(parents=True, exist_ok=True)
        with (model_out / "predictions.jsonl").open("w", encoding="utf-8") as f:
            for p in predictions:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
        (model_out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    combined = {
        "status": "DONE",
        "models": all_metrics,
        "n_samples": len(samples),
        "dataset_hash": dataset_hash,
        "git_commit": git_commit(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    (out / "metrics.json").write_text(json.dumps(combined, indent=2), encoding="utf-8")
    (out / "config.json").write_text(json.dumps({
        "experiment": EXPERIMENT_ID,
        "max_samples": MAX_SAMPLES,
        "target_models": TARGET_MODELS,
        "benchmark": str(BENCHMARK),
        "dataset_hash": dataset_hash,
        "git_commit": git_commit(),
        "random_seed": int(os.getenv("EXP002_SEED", "42")),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, indent=2), encoding="utf-8")
    (out / "logs.json").write_text(json.dumps({"events": logs}, indent=2), encoding="utf-8")

    with ExperimentRunContext.create(EXPERIMENT_ID, config={"max_samples": MAX_SAMPLES}) as ctx:
        ctx.write_metrics(combined)
        ctx.write_model_config(cfg)
        update_registry_row(ROOT / "experiments/registry.csv", {
            "experiment_id": EXPERIMENT_ID,
            "run_id": ctx.run_id,
            "status": "DONE",
            "n_samples": str(len(samples)),
            "dataset_hash": dataset_hash,
            "run_dir": str(ctx.run_dir),
        })

    print(json.dumps(combined, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
