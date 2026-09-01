"""Run baseline comparison with shared dataset, target, and judge."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from src.adapti_guard.baselines.adapti_guard_baseline import AdaptiGuardBaseline
from src.adapti_guard.baselines.comparison_framework import (
    BaselineType,
    write_baseline_comparison_csv,
)
from src.adapti_guard.baselines.llama_guard_baseline import LlamaGuardBaseline
from src.adapti_guard.baselines.nemo_baseline import NeMoGuardrailsBaseline
from src.adapti_guard.baselines.no_defense import NoDefenseBaseline
from src.adapti_guard.baselines.prompt_guard_baseline import PromptGuardBaseline
from src.adapti_guard.baselines.regex_baseline import RegexDefenseBaseline
from src.adapti_guard.evaluation.experiment_logging import ExperimentRunContext, git_commit, sha256_file
from src.adapti_guard.evaluation.llm_judge import LLMJudge
from src.adapti_guard.evaluation.metrics import asr_with_ci, compute_extended_metrics
from src.adapti_guard.evaluation.target_model import build_target_model, load_model_config


def load_test_samples(benchmark_dir: Path, limit: int | None = None) -> list[dict]:
    path = benchmark_dir / "test.jsonl"
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows[:limit] if limit else rows


def _result_to_metric_row(r, sample_id: str, label: int) -> dict:
    attack_present = label == 1
    v = r.judge_verdict
    if hasattr(r, "outcome"):
        return {
            "sample_id": sample_id,
            "attack_present": attack_present,
            "attack_success": r.outcome.attack_success if attack_present else False,
            "legitimate_task": not attack_present,
            "legitimate_success": r.outcome.legitimate_success if not attack_present else False,
            "latency_ms": sum(r.latency_ms.values()) if isinstance(r.latency_ms, dict) else getattr(r, "latency_ms", 0),
            "defense_cost": r.outcome.defense_cost,
        }
    return {
        "sample_id": sample_id,
        "attack_present": attack_present,
        "attack_success": bool(v and v.attack_success and attack_present),
        "legitimate_task": not attack_present,
        "legitimate_success": bool(v and v.utility_success and not attack_present),
        "latency_ms": getattr(r, "latency_ms", 0),
        "defense_cost": 0.0 if not getattr(r, "blocked", False) else 0.1,
    }


def run_baseline(
    baseline_name: str,
    baseline,
    samples: list[dict],
    ctx: ExperimentRunContext | None = None,
) -> dict[str, Any]:
    metric_rows = []
    for row in samples:
        r = baseline.run_sample(
            sample_id=row["id"],
            prompt=row["prompt"],
            label=int(row["label"]),
            category=row["category"],
            attack_type=row.get("attack_type", row["category"]),
        )
        metric_rows.append(_result_to_metric_row(r, row["id"], int(row["label"])))
        if ctx:
            ctx.append_log("INFO", f"sample {row['id']}", baseline=baseline_name)

    metrics = compute_extended_metrics(metric_rows)
    metrics.update(asr_with_ci(metric_rows))
    latencies = [m["latency_ms"] for m in metric_rows if m.get("latency_ms")]
    metrics["mean_latency_ms"] = sum(latencies) / len(latencies) if latencies else 0.0
    metrics["n_samples"] = len(samples)
    return metrics


def run_comparison(
    *,
    benchmark_dir: Path,
    output_csv: Path,
    max_samples: int | None = None,
    target_key: str = "gpt4o_mini",
    experiment_id: str = "EXP003",
) -> dict[str, Any]:
    if not os.getenv("OPENROUTER_API_KEY"):
        write_baseline_comparison_csv(output_csv, [])
        return {"status": "BLOCKED", "reason": "missing_api_key"}

    samples = load_test_samples(benchmark_dir, max_samples)
    if not samples:
        write_baseline_comparison_csv(output_csv, [])
        return {"status": "BLOCKED", "reason": "no_test_samples"}

    cfg = load_model_config()
    target = build_target_model(target_key)
    judge = LLMJudge(build_target_model("judge"))

    baselines = {
        BaselineType.NO_DEFENSE.value: NoDefenseBaseline(target, judge),
        BaselineType.REGEX_DEFENSE.value: RegexDefenseBaseline(target, judge),
        BaselineType.ADAPTI_GUARD.value: AdaptiGuardBaseline(target, judge),
        BaselineType.LLAMA_GUARD.value: LlamaGuardBaseline(target, judge),
        BaselineType.PROMPT_GUARD.value: PromptGuardBaseline(target, judge),
        BaselineType.NEMO_GUARDRAILS.value: NeMoGuardrailsBaseline(target, judge),
    }

    csv_rows: list[dict[str, Any]] = []
    dataset_hash = sha256_file(benchmark_dir / "test.jsonl") if (benchmark_dir / "test.jsonl").exists() else ""

    with ExperimentRunContext.create(experiment_id, config={
        "benchmark": str(benchmark_dir),
        "target_key": target_key,
        "n_samples": len(samples),
    }) as ctx:
        for name, baseline in baselines.items():
            ctx.append_log("INFO", f"running baseline {name}")
            metrics = run_baseline(name, baseline, samples, ctx)
            status = "DONE" if name != BaselineType.NEMO_GUARDRAILS.value else metrics.get("status", "PARTIAL")
            if name == BaselineType.NEMO_GUARDRAILS.value and not getattr(baseline, "_nemo_available", False):
                status = "BLOCKED"

            row = {
                "baseline": name,
                "dataset": str(benchmark_dir),
                "dataset_hash": dataset_hash,
                "target_model": cfg["models"][target_key]["model"],
                "judge_model": cfg["models"]["judge"]["model"],
                "n_samples": len(samples),
                "asr": metrics.get("asr", 0),
                "asr_ci_lower": metrics.get("asr_ci_lower", 0),
                "asr_ci_upper": metrics.get("asr_ci_upper", 0),
                "utility": metrics.get("utility", 0),
                "fpr": metrics.get("fpr", 0),
                "defense_rate": metrics.get("defense_rate", 0),
                "mean_latency_ms": metrics.get("mean_latency_ms", 0),
                "status": status if status != "BLOCKED" else "BLOCKED",
                "run_dir": str(ctx.run_dir),
                "git_commit": git_commit(),
            }
            csv_rows.append(row)
            ctx.append_log("INFO", f"completed {name}", asr=metrics.get("asr"))

        ctx.write_metrics({"baselines": csv_rows, "status": "DONE"})

    write_baseline_comparison_csv(output_csv, csv_rows)
    return {"status": "DONE", "n_baselines": len(csv_rows), "output": str(output_csv)}
