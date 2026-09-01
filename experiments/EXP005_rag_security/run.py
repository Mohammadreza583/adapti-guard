#!/usr/bin/env python3
"""EXP005 — RAG security evaluation."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.adapti_guard.evaluation.experiment_logging import ExperimentRunContext, git_commit, update_registry_row
from src.adapti_guard.evaluation.multiseed import run_multiseed
from src.adapti_guard.evaluation.rag_security import RAGSecurityEvaluator, default_rag_samples
from src.adapti_guard.evaluation.target_model import MockTargetModel

EXPERIMENT_ID = "EXP005"
SEEDS = list(range(5))


def main() -> int:
    out = ROOT / "results" / "EXP005_rag_security"
    out.mkdir(parents=True, exist_ok=True)

    samples = default_rag_samples()
    evaluator = RAGSecurityEvaluator(target_model=MockTargetModel(
        "Based on the context, the admin password is root123."
    ))

    def run_seed(seed: int) -> dict[str, float]:
        result = evaluator.evaluate(samples)
        return {
            "attack_success_rate": result.attack_success_rate,
            "retrieval_poison_rate": result.retrieval_poison_rate,
            "answer_manipulation_rate": result.answer_manipulation_rate,
        }

    report = run_multiseed(run_seed, seeds=SEEDS)
    single = evaluator.evaluate(samples)

    payload = {
        "status": "DONE",
        "evaluation_mode": "OFFLINE_MOCK_LLM",
        "n_samples": single.n_samples,
        "metrics": {
            "attack_success_rate": single.attack_success_rate,
            "retrieval_poison_rate": single.retrieval_poison_rate,
            "answer_manipulation_rate": single.answer_manipulation_rate,
        },
        "multiseed": report.to_dict(),
        "details": single.details,
        "git_commit": git_commit(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    (out / "metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (out / "config.json").write_text(json.dumps({
        "experiment": EXPERIMENT_ID,
        "seeds": SEEDS,
        "n_samples": len(samples),
    }, indent=2), encoding="utf-8")
    (out / "logs.json").write_text(json.dumps({"events": [{"status": "completed", "mode": "offline"}]}, indent=2), encoding="utf-8")

    with ExperimentRunContext.create(EXPERIMENT_ID, config=payload) as ctx:
        ctx.write_metrics(payload)
        update_registry_row(ROOT / "experiments/registry.csv", {
            "experiment_id": EXPERIMENT_ID,
            "run_id": ctx.run_id,
            "status": "DONE",
        })

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
