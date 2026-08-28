#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--status", required=True)
    args = parser.parse_args()

    run_dir = ROOT / "experiments" / "runs" / f"{args.id}_{args.version}"

    if not run_dir.exists():
        raise FileNotFoundError(run_dir)

    status = {
        "experiment_id": args.id,
        "version": args.version,
        "status": args.status,
        "finalized_at_utc": datetime.now(timezone.utc).isoformat(),
    }

    (run_dir / "status.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Experiment finalized: {args.id} / {args.version}")
    print(f"Status: {args.status}")
    print(f"Run:    {run_dir}")


if __name__ == "__main__":
    main()
