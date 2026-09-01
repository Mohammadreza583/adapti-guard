"""Baseline comparison framework — fair protocol, no fabricated results."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import csv


class BaselineType(str, Enum):
    NO_DEFENSE = "no_defense"
    REGEX_DEFENSE = "regex_defense"
    ADAPTI_GUARD = "adapti_guard"
    LLAMA_GUARD = "llama_guard"
    PROMPT_GUARD = "prompt_guard"
    NEMO_GUARDRAILS = "nemo_guardrails"


@dataclass
class BaselineSpec:
    baseline_type: BaselineType
    name: str
    implemented: bool
    executed: bool = False
    status: str = "NOT_EXECUTED"
    notes: str = ""


BASELINE_REGISTRY: list[BaselineSpec] = [
    BaselineSpec(BaselineType.NO_DEFENSE, "No Defense", implemented=True),
    BaselineSpec(BaselineType.REGEX_DEFENSE, "Regex Defense", implemented=True),
    BaselineSpec(BaselineType.ADAPTI_GUARD, "ADAPTI-GUARD Adaptive", implemented=True),
    BaselineSpec(BaselineType.LLAMA_GUARD, "Llama Guard", implemented=False, notes="Requires ML model integration"),
    BaselineSpec(BaselineType.PROMPT_GUARD, "Prompt Guard", implemented=False, notes="Requires Meta Prompt Guard API/model"),
    BaselineSpec(BaselineType.NEMO_GUARDRAILS, "NeMo Guardrails", implemented=False, notes="Requires NeMo installation"),
]


def write_baseline_comparison_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write results/baseline_comparison.csv — only with actually executed rows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        fieldnames = [
            "baseline", "dataset", "target_model", "judge_model", "n_samples",
            "asr", "asr_ci_lower", "asr_ci_upper", "utility", "fpr", "mean_latency_ms",
            "status", "run_dir",
        ]
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
        return

    fieldnames = sorted({k for row in rows for k in row.keys()})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
