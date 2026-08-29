"""Run Phase 8C once and write versioned artifacts."""

from src.adapti_guard.experiments.phase8c_analysis import run_phase8c


def main():
    paths = run_phase8c()
    print("PHASE 8C")
    for name, path in paths.items():
        print(f"{name} = {path}")


if __name__ == "__main__":
    main()
