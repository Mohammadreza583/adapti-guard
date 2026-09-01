#!/usr/bin/env python3
"""EXP002 — Real LLM end-to-end evaluation (judge-based ASR)."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv()

from src.adapti_guard.evaluation.experiment_logging import ExperimentRunContext, update_registry_row
from src.adapti_guard.evaluation.llm_judge import LLMJudge
from src.adapti_guard.evaluation.metrics import asr_with_ci, compute_extended_metrics
from src.adapti_guard.evaluation.real_llm_pipeline import RealLLMEvaluationPipeline
from src.adapti_guard.evaluation.target_model import build_target_model, load_model_config

EXPERIMENT_ID = "EXP002"
MAX_SAMPLES = int(os.getenv("EXP002_MAX_SAMPLES", "5"))


def load_test_samples(limit: int) -> list[dict]:
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
        "latency_ms": result.latency_ms,
        "token_usage": result.token_usage,
        "security_score": result.outcome.security_score,
        "utility_score": result.outcome.utility_score,
        "defense_cost": result.outcome.defense_cost,
        "evaluation_mode": result.evaluation_mode,
    }


def main() -> int:
    if not os.getenv("OPENROUTER_API_KEY"):
        status = "BLOCKED"
        with ExperimentRunContext.create(EXPERIMENT_ID, config={"reason": "missing_api_key"}) as ctx:
            ctx.write_metrics({"status": status})
            update_registry_row(ROOT / "experiments/registry.csv", {
                "experiment_id": EXPERIMENT_ID, "run_id": ctx.run_id, "status": status,
            })
        print(json.dumps({"status": status}))
        return 2

    samples = load_test_samples(MAX_SAMPLES)
    if not samples:
        status = "BLOCKED"
        with ExperimentRunContext.create(EXPERIMENT_ID, config={"reason": "no_test_samples"}) as ctx:
            ctx.write_metrics({"status": status})
        print(json.dumps({"status": status, "reason": "no_test_samples"}))
        return 2

    cfg = load_model_config()
    target = build_target_model("gpt4o_mini")
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
            "prompt": r.prompt[:500],
            "target_response": r.target_response[:2000],
            "judge": r.judge_verdict.to_dict() if r.judge_verdict else None,
            "attack_success": r.outcome.attack_success,
        })

    metrics = compute_extended_metrics(results)
    metrics.update(asr_with_ci(results))
    metrics["status"] = "DONE"
    metrics["n_samples"] = len(samples)
    metrics["target_model"] = cfg["models"]["gpt4o_mini"]["model"]
    metrics["judge_model"] = cfg["models"]["judge"]["model"]

    out = ROOT / "results/EXP002_real_llm_evaluation"
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (out / "config.json").write_text(json.dumps({
        "experiment": EXPERIMENT_ID,
        "max_samples": MAX_SAMPLES,
        "target_model": metrics["target_model"],
        "judge_model": metrics["judge_model"],
    }, indent=2), encoding="utf-8")
    with (out / "predictions.jsonl").open("w", encoding="utf-8") as f:
        for p in predictions:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    (out / "README.md").write_text(f"# EXP002\n\nStatus: DONE\nN={len(samples)}\n", encoding="utf-8")

    with ExperimentRunContext.create(EXPERIMENT_ID, config={"max_samples": MAX_SAMPLES}) as ctx:
        ctx.write_metrics(metrics)
        ctx.write_model_config(cfg)
        for p in predictions:
            ctx.append_response(p)
        update_registry_row(ROOT / "experiments/registry.csv", {
            "experiment_id": EXPERIMENT_ID,
            "run_id": ctx.run_id,
            "status": "DONE",
            "target_model": metrics["target_model"],
            "judge_model": metrics["judge_model"],
            "n_samples": str(len(samples)),
            "run_dir": str(ctx.run_dir),
        })

    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
