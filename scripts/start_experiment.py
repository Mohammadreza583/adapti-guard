#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "experiments" / "runs"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "UNKNOWN"


def git_status() -> str:
    try:
        return subprocess.check_output(
            ["git", "status", "--short"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return "UNKNOWN"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--component", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--change", required=True)
    parser.add_argument("--dataset", default="")
    parser.add_argument("--split", default="")
    parser.add_argument("--samples", type=int, default=0)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--dataset-file", default="")
    parser.add_argument("--command", default="")
    args = parser.parse_args()

    timestamp = datetime.now(timezone.utc)
    run_name = f"{args.id}_{args.version}"
    run_dir = RUNS / run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    dataset_hash = ""

    if args.dataset_file:
        dataset_path = ROOT / args.dataset_file
        if not dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {dataset_path}"
            )
        dataset_hash = sha256(dataset_path)

    config = {
        "experiment_id": args.id,
        "version": args.version,
        "status": "RUNNING",
        "component": args.component,
        "objective": args.objective,
        "change": args.change,
        "dataset": args.dataset,
        "split": args.split,
        "samples": args.samples,
        "seed": args.seed,
        "dataset_file": args.dataset_file,
        "dataset_sha256": dataset_hash,
        "command": args.command,
        "created_at_utc": timestamp.isoformat(),
        "git_commit": git_commit(),
        "git_status_at_start": git_status(),
        "python": sys.version,
        "platform": platform.platform(),
        "executable": sys.executable,
        "working_directory": str(ROOT),
    }

    (run_dir / "config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    (run_dir / "git_commit.txt").write_text(
        git_commit() + "\n",
        encoding="utf-8",
    )

    (run_dir / "git_status.txt").write_text(
        git_status() + "\n",
        encoding="utf-8",
    )

    (run_dir / "environment.txt").write_text(
        "\n".join([
            f"Python: {sys.version}",
            f"Executable: {sys.executable}",
            f"Platform: {platform.platform()}",
            f"Working directory: {ROOT}",
        ]) + "\n",
        encoding="utf-8",
    )

    dataset_info = {
        "dataset": args.dataset,
        "path": args.dataset_file,
        "sha256": dataset_hash,
    }

    (run_dir / "dataset_hashes.json").write_text(
        json.dumps(dataset_info, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    (run_dir / "command.txt").write_text(
        args.command + "\n",
        encoding="utf-8",
    )

    (run_dir / "status.txt").write_text(
        "RUNNING\n",
        encoding="utf-8",
    )

    print("=" * 80)
    print("EXPERIMENT INITIALIZED")
    print("=" * 80)
    print(f"ID:        {args.id}")
    print(f"Version:   {args.version}")
    print(f"Run dir:   {run_dir}")
    print(f"Git:       {git_commit()}")
    print(f"Dataset:   {args.dataset}")
    print(f"Split:     {args.split}")
    print(f"Samples:   {args.samples:,}")
    print(f"Seed:      {args.seed}")
    print(f"SHA256:    {dataset_hash or 'N/A'}")
    print("=" * 80)


if __name__ == "__main__":
    main()
