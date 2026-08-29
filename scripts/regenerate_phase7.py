"""
Regenerate Phase 7 controlled artifacts.

Protocol:
    100 episodes
    75 attack / 25 legitimate  (PHASE7_EPISODE_SCHEDULE)
    attack payloads = first 75 records of common_attack_stream.json

Methods:
    Fixed-L0, Fixed-L1, Fixed-L2, Fixed-L3, Adaptive
"""

from __future__ import annotations

import json
import shutil
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from src.adapti_guard.baselines.baseline_runner import BaselineRunner
from src.adapti_guard.experiments.experiment_runner import ExperimentRunner
from src.adapti_guard.experiments.phase7_schedule import (
    PHASE7_ATTACK_STREAM_NAME,
    PHASE7_ATTACK_STREAM_SLICE,
    PHASE7_EPISODE_SCHEDULE,
    PHASE7_EPISODES,
    validate_phase7_schedule,
)


def archive_existing(phase7: Path) -> None:
    archive = phase7 / "archive"
    archive.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for name in (
        "fixed_baselines_100.json",
        "adaptive_100.json",
        "fixed_baselines_100_v2.json",
        "adaptive_100_v2.json",
        "phase7_schedule.json",
        "phase7_manifest.json",
    ):
        src = phase7 / name
        if src.exists():
            dst = archive / f"{src.stem}_{stamp}{src.suffix}"
            shutil.copy2(src, dst)
            print("archived", src, "->", dst)


def load_phase7_stream() -> list[dict]:
    stream_path = Path("results/common_attack_stream.json")
    if not stream_path.exists():
        raise FileNotFoundError(
            "Missing results/common_attack_stream.json. "
            "Run scripts/generate_attack_stream.py first."
        )

    stream = json.loads(stream_path.read_text(encoding="utf-8"))
    start, end = PHASE7_ATTACK_STREAM_SLICE
    slice_ = stream[start:end]
    if len(slice_) != 75:
        raise ValueError(
            f"Expected 75 attack-stream records for Phase 7, got {len(slice_)}"
        )
    return slice_


def main():
    schedule = validate_phase7_schedule(PHASE7_EPISODE_SCHEDULE)
    stream_slice = load_phase7_stream()

    phase7 = Path("results/phase7")
    phase7.mkdir(parents=True, exist_ok=True)
    archive_existing(phase7)

    # Persist schedule documentation
    schedule_doc = {
        "name": "phase7_v2_75_25",
        "episodes": PHASE7_EPISODES,
        "attack": sum(1 for x in schedule if not x),
        "legitimate": sum(1 for x in schedule if x),
        "pattern": "[attack, attack, attack, legitimate] x 25",
        "encoding": "True=legitimate, False=attack",
        "attack_stream": PHASE7_ATTACK_STREAM_NAME,
        "attack_stream_slice": list(PHASE7_ATTACK_STREAM_SLICE),
        "schedule": schedule,
    }
    (phase7 / "phase7_schedule.json").write_text(
        json.dumps(schedule_doc, indent=2),
        encoding="utf-8",
    )

    # Fixed baselines
    br = BaselineRunner()
    baseline_rows = []
    for level in range(4):
        row = br.run_fixed(
            method=f"fixed_level_{level}",
            defense_level=level,
            episodes=PHASE7_EPISODES,
            episode_schedule=schedule,
            attack_stream=stream_slice,
        )
        baseline_rows.append(asdict(row))
        print(
            row.method,
            "asr=", row.asr,
            "utility=", row.utility,
            "att=", row.attack_episodes,
            "leg=", row.legitimate_episodes,
        )

    baselines_path = phase7 / "fixed_baselines_100_v2.json"
    baselines_path.write_text(
        json.dumps(baseline_rows, indent=2),
        encoding="utf-8",
    )
    # Also write canonical name used by gate tooling.
    (phase7 / "fixed_baselines_100.json").write_text(
        json.dumps(baseline_rows, indent=2),
        encoding="utf-8",
    )

    # Adaptive
    runner = ExperimentRunner(
        attack_stream=stream_slice,
        episode_schedule=schedule,
    )
    results = runner.run(PHASE7_EPISODES)
    ExperimentRunner.save_results(
        results,
        phase7 / "adaptive_100_v2.json",
    )
    ExperimentRunner.save_results(
        results,
        phase7 / "adaptive_100.json",
    )

    levels = [r.defense_level for r in results]
    transitions = sum(1 for a, b in zip(levels, levels[1:]) if a != b)
    increases = sum(1 for a, b in zip(levels, levels[1:]) if b > a)
    decreases = sum(1 for a, b in zip(levels, levels[1:]) if b < a)
    attack_eps = sum(1 for r in results if r.attack_present)
    legit_eps = sum(1 for r in results if not r.attack_present)
    utility = (
        sum(1 for r in results if r.legitimate_success) / legit_eps
        if legit_eps
        else 0.0
    )

    manifest = {
        "experiment": "phase7",
        "version": "v2_75_25",
        "seed": 42,
        "episodes": PHASE7_EPISODES,
        "attack_stream": PHASE7_ATTACK_STREAM_NAME,
        "attack_stream_slice": list(PHASE7_ATTACK_STREAM_SLICE),
        "defense_levels": [0, 1, 2, 3],
        "adaptive": True,
        "schedule": "phase7_v2_75_25",
        "adaptive_summary": {
            "attack_episodes": attack_eps,
            "legitimate_episodes": legit_eps,
            "utility": utility,
            "levels": sorted(set(levels)),
            "actions": sorted({r.defense_action for r in results}),
            "transitions": transitions,
            "increases": increases,
            "decreases": decreases,
        },
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    (phase7 / "phase7_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print("wrote", baselines_path)
    print("wrote", phase7 / "adaptive_100_v2.json")
    print("summary", manifest["adaptive_summary"])


if __name__ == "__main__":
    main()
