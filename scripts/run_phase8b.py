"""Run Phase 8B analyses once and write versioned artifacts."""

from src.adapti_guard.experiments.phase8b_analysis import run_phase8b


def main():
    paths = run_phase8b()
    print("PHASE 8B")
    for name, path in paths.items():
        print(f"{name} = {path}")


if __name__ == "__main__":
    main()
