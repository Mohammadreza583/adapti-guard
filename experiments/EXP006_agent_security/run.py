#!/usr/bin/env python3
"""EXP006 — Agent security evaluation."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.adapti_guard.evaluation.agent_security import AgentSecurityEvaluator, default_agent_scenarios
from src.adapti_guard.evaluation.experiment_logging import ExperimentRunContext, git_commit, update_registry_row
from src.adapti_guard.evaluation.multiseed import run_multiseed
from src.adapti_guard.evaluation.target_model import MockTargetModel

EXPERIMENT_ID = "EXP006"
SEEDS = list(range(5))


def main() -> int:
    out = ROOT / "results" / "EXP006_agent_security"
    out.mkdir(parents=True, exist_ok=True)

    scenarios = default_agent_scenarios()
    evaluator = AgentSecurityEvaluator(llm=MockTargetModel(
        'PLAN: call shell with "cat ~/.ssh/id_rsa"\nTOOL: shell'
    ))

    def run_seed(seed: int) -> dict[str, float]:
        result = evaluator.evaluate(scenarios)
        return {
            "attack_success_rate": result.attack_success_rate,
            "unsafe_tool_call_rate": result.unsafe_tool_call_rate,
            "policy_violation_rate": result.policy_violation_rate,
            "task_utility": result.task_utility,
        }

    report = run_multiseed(run_seed, seeds=SEEDS)
    single = evaluator.evaluate(scenarios)

    payload = {
        "status": "DONE",
        "evaluation_mode": "OFFLINE_MOCK_LLM",
        "n_samples": single.n_samples,
        "metrics": {
            "attack_success_rate": single.attack_success_rate,
            "unsafe_tool_call_rate": single.unsafe_tool_call_rate,
            "policy_violation_rate": single.policy_violation_rate,
            "task_utility": single.task_utility,
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
        "n_scenarios": len(scenarios),
    }, indent=2), encoding="utf-8")
    (out / "logs.json").write_text(json.dumps({"events": [{"status": "completed"}]}, indent=2), encoding="utf-8")

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
