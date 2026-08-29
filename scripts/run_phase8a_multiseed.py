"""Run Phase 8A multi-seed evaluation once and write artifacts."""

from __future__ import annotations

import json

from src.adapti_guard.experiments.phase8_multiseed import (
    PHASE8_METHODS,
    PHASE8_SEEDS,
    run_matrix,
    save_artifacts,
    summarize,
)


def main():
    raw = run_matrix()
    summary = summarize(raw)
    paths = save_artifacts(raw, summary)

    print("PHASE 8A MULTI-SEED")
    print("methods =", list(PHASE8_METHODS))
    print("seeds   =", list(PHASE8_SEEDS))
    print("runs    =", len(raw))
    print("raw     =", paths["raw"])
    print("summary =", paths["summary"])
    print(
        "determinism =",
        json.dumps(summary["determinism"]["by_method"], indent=2),
    )


if __name__ == "__main__":
    main()
