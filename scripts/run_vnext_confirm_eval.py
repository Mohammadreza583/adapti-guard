#!/usr/bin/env python3
"""VNEXT confirmation LIVE eval runner.

STEP 0 (request file) must already exist. LLM/API = 0 until then.

Gates:
  - missing docs/experiments/VNEXT_CONFIRM_EXPERIMENT_REQUEST.md → INVALID_MISSING_REQUEST
  - pack SHA-256 mismatch → INVALID_HASH_MISMATCH (S3)
  - OPENROUTER_API_KEY missing (with --require-key, default) → INVALID_MISSING_KEYS

Does not retune Layer A TEST, modify frozen packs, or edit LAYER_A_* results.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.adapti_guard.experiments.env_loader import load_project_env, validate_openrouter_key
from src.adapti_guard.experiments.vnext_confirm import (
    CONFIRMATION_JSONL,
    CONTROL_BASELINE,
    EXPERIMENT_ID,
    JUDGE_CONFIG_KEY,
    JUDGE_MODEL_ID,
    LOCKED_N_ATTACK,
    LOCKED_N_BENIGN,
    LOCKED_PACK_SHA256,
    PACK_ID,
    REQUEST_REL,
    STATUS_BLOCKED,
    STATUS_COMPLETED,
    STATUS_HASH_MISMATCH,
    STATUS_MISSING_KEYS,
    STATUS_NO_REQUEST,
    TARGET_CONFIG_KEY,
    TARGET_MODEL_ID,
    TREATMENT_BASELINE,
    TREATMENT_NAME,
    load_predictions,
    render_audit,
    request_file_exists,
    score_confirmation,
    sha256_file,
    verify_confirmation_pack,
    write_json,
    write_text,
)
from src.adapti_guard.evaluation.experiment_logging import git_commit
from src.adapti_guard.evaluation.target_model import load_model_config


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def _preflight_dir(output_root: Path) -> Path:
    path = output_root
    if path.name == "VNEXT_CONFIRM" or not path.exists():
        path = output_root / _utc_stamp() if path.name == "VNEXT_CONFIRM" else output_root
    path.mkdir(parents=True, exist_ok=True)
    return path


def _write_stop(
    out_dir: Path,
    *,
    status: str,
    reason: str,
    pack: dict,
    git_sha: str,
    seed: int,
    cache_enabled: bool,
    run_id: str,
    models: dict,
) -> int:
    write_text(out_dir / "STATUS.txt", f"{status}\n{reason}\n")
    write_text(out_dir / "git_commit.txt", git_sha + "\n")
    write_text(out_dir / "pack_hash.txt", LOCKED_PACK_SHA256 + "\n")
    write_json(out_dir / "pack_verify.json", pack)
    write_json(
        out_dir / "models_observed.json",
        {
            **models,
            "target_neq_judge": models.get("target_model_id") != models.get("judge_model_id"),
            "cache_enabled_yaml": cache_enabled,
            "pack_id": PACK_ID,
            "confirmation_sha256": LOCKED_PACK_SHA256,
            "git_commit": git_sha,
            "status": status,
        },
    )
    audit = render_audit(
        status=status,
        git_commit=git_sha,
        run_id=run_id,
        pack_hash=pack,
        models=models,
        seed=seed,
        cache_enabled=cache_enabled,
        score=None,
        llm_spend_usd=0.0,
        extra_notes=[reason, "LLM/API calls: 0"],
    )
    write_text(out_dir / "AUDIT.md", audit)
    write_json(
        out_dir / "metrics.json",
        {"status": status, "reason": reason, "llm_spend_usd": 0.0},
    )
    code = {
        STATUS_MISSING_KEYS: 2,
        STATUS_HASH_MISMATCH: 3,
        STATUS_NO_REQUEST: 4,
        STATUS_BLOCKED: 1,
    }.get(status, 1)
    print(f"STATUS={status} reason={reason} out={out_dir}", file=sys.stderr)
    return code


def _arm_cost_usd(metrics: dict) -> float:
    est = metrics.get("api_cost_estimate") or {}
    if isinstance(est, dict) and "estimated_usd" in est:
        return float(est["estimated_usd"])
    return 0.0


def _postprocess(out_dir: Path, *, git_sha: str, seed: int, cache_enabled: bool, run_id: str) -> dict:
    b0_path = out_dir / CONTROL_BASELINE / f"{CONTROL_BASELINE}_predictions.jsonl"
    t_path = out_dir / TREATMENT_BASELINE / f"{TREATMENT_BASELINE}_predictions.jsonl"
    b0_rows = load_predictions(b0_path)
    t_rows = load_predictions(t_path)
    score = score_confirmation(b0_rows, t_rows)
    b0_metrics = json.loads((out_dir / CONTROL_BASELINE / f"{CONTROL_BASELINE}_metrics.json").read_text())
    t_metrics = json.loads((out_dir / TREATMENT_BASELINE / f"{TREATMENT_BASELINE}_metrics.json").read_text())
    spend = _arm_cost_usd(b0_metrics) + _arm_cost_usd(t_metrics)
    judge_ids = {
        r.get("judge_model")
        for r in (b0_rows + t_rows)
        if r.get("judge_model")
    }
    target_ids = {
        r.get("model_id")
        for r in (b0_rows + t_rows)
        if r.get("model_id")
    }
    n_cache = sum(1 for r in (b0_rows + t_rows) if r.get("target_cache_hit"))
    models = {
        "target_config_key": TARGET_CONFIG_KEY,
        "target_model_id": next(iter(target_ids), TARGET_MODEL_ID),
        "judge_config_key": JUDGE_CONFIG_KEY,
        "judge_model_id": next(iter(judge_ids), JUDGE_MODEL_ID),
        "observed_target_ids": sorted(str(x) for x in target_ids),
        "observed_judge_ids": sorted(str(x) for x in judge_ids),
        "n_target_cache_hits": n_cache,
    }
    pack = verify_confirmation_pack(ROOT)
    comparison = {
        "protocol": "VNEXT-PROTOCOL-0.1",
        "treatment_name": TREATMENT_NAME,
        "treatment_factory": TREATMENT_BASELINE,
        "control": CONTROL_BASELINE,
        "n_attack_paired": score["n_attack_paired_scorable"],
        "delta_attributed": score["delta_attributed"],
        "msid": score["msid"],
        "msid_gate": score["msid_gate"],
        "utility_gate": score["utility_gate"],
        "qualified_win": score["qualified_win"],
        "mcnemar_intervention": score["mcnemar_intervention"],
        "mcnemar_mixed_asr": score["mcnemar_mixed_asr"],
        "fail_reasons": score["fail_reasons"],
        "llm_spend_usd": spend,
    }
    write_json(out_dir / "comparison.json", comparison)
    write_json(out_dir / "score.json", score)
    if score["qualified_win"]:
        status = f"{STATUS_COMPLETED} / MSID_GATE=PASS / QUALIFIED_WIN=true"
    else:
        gate = score["msid_gate"]
        status = f"{STATUS_COMPLETED} / MSID_GATE={gate} / QUALIFIED_WIN=false"
    write_text(out_dir / "STATUS.txt", status + "\n")
    audit = render_audit(
        status=status,
        git_commit=git_sha,
        run_id=run_id,
        pack_hash=pack,
        models=models,
        seed=seed,
        cache_enabled=cache_enabled,
        score=score,
        llm_spend_usd=spend,
        extra_notes=[
            "Primary confirmatory test is intervention-mediated McNemar, not mixed ASR.",
            "Do not count model_refusal as an intervention win.",
        ],
    )
    write_text(out_dir / "AUDIT.md", audit)
    write_json(
        out_dir / "models_observed.json",
        {
            **models,
            "target_neq_judge": models.get("target_model_id") != models.get("judge_model_id"),
            "cache_enabled_yaml": cache_enabled,
            "pack_id": PACK_ID,
            "confirmation_sha256": LOCKED_PACK_SHA256,
            "git_commit": git_sha,
            "run_id": run_id,
            "n_target_cache_hits": n_cache,
            "llm_spend_usd": spend,
            "msid_gate": score["msid_gate"],
            "qualified_win": score["qualified_win"],
        },
    )
    return {"status": status, "score": score, "spend": spend, "run_id": run_id}


def main() -> int:
    parser = argparse.ArgumentParser(description="VNEXT confirmation LIVE eval (B0 vs VNEXT-ADAPT).")
    parser.add_argument("--backend", default="openrouter")
    parser.add_argument("--target", default=TARGET_CONFIG_KEY)
    parser.add_argument("--judge", default=JUDGE_CONFIG_KEY)
    parser.add_argument("--baselines", nargs="*", default=[CONTROL_BASELINE, TREATMENT_BASELINE])
    parser.add_argument("--attack-n", type=int, default=LOCKED_N_ATTACK)
    parser.add_argument("--benign-n", type=int, default=LOCKED_N_BENIGN)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--split", default="confirmation")
    parser.add_argument("--benchmark-dir", default=str(CONFIRMATION_JSONL.parent))
    parser.add_argument("--output", default="experiments/real_llm_eval/VNEXT_CONFIRM")
    parser.add_argument("--experiment-id", default=EXPERIMENT_ID)
    parser.add_argument("--require-key", action="store_true", default=True)
    parser.add_argument("--allow-missing-key", action="store_true", help="Skip key gate (tests only).")
    parser.add_argument("--skip-live", action="store_true", help="Preflight only; no LLM.")
    args, extra = parser.parse_known_args()

    load_project_env()
    git_sha = git_commit() or "UNKNOWN"
    models_cfg = load_model_config(ROOT / "configs" / "models.yaml")
    cache_enabled = bool(models_cfg.get("cache", {}).get("enabled", False))
    models = {
        "target_config_key": args.target,
        "target_model_id": TARGET_MODEL_ID,
        "judge_config_key": args.judge,
        "judge_model_id": JUDGE_MODEL_ID,
    }

    output_root = Path(args.output)
    if not output_root.is_absolute():
        output_root = ROOT / output_root
    out_dir = _preflight_dir(output_root)
    run_id = f"VNEXT-CONFIRM-{out_dir.name}"
    write_text(
        out_dir / "command.txt",
        " ".join(["python3", "scripts/run_vnext_confirm_eval.py", *sys.argv[1:]]) + "\n",
    )
    write_text(out_dir / "git_commit.txt", git_sha + "\n")

    if not request_file_exists(ROOT):
        pack = verify_confirmation_pack(ROOT)
        return _write_stop(
            out_dir,
            status=STATUS_NO_REQUEST,
            reason=f"LLM=0 until {REQUEST_REL} exists",
            pack=pack,
            git_sha=git_sha,
            seed=args.seed,
            cache_enabled=cache_enabled,
            run_id=run_id,
            models=models,
        )

    pack = verify_confirmation_pack(ROOT)
    write_json(out_dir / "pack_verify.json", pack)
    write_text(out_dir / "pack_hash.txt", LOCKED_PACK_SHA256 + "\n")
    if not pack.get("ok"):
        return _write_stop(
            out_dir,
            status=STATUS_HASH_MISMATCH,
            reason=str(pack.get("reason")),
            pack=pack,
            git_sha=git_sha,
            seed=args.seed,
            cache_enabled=cache_enabled,
            run_id=run_id,
            models=models,
        )

    observed = sha256_file(ROOT / CONFIRMATION_JSONL)
    if observed != LOCKED_PACK_SHA256:
        return _write_stop(
            out_dir,
            status=STATUS_HASH_MISMATCH,
            reason=f"hash {observed} != lock {LOCKED_PACK_SHA256}",
            pack=pack,
            git_sha=git_sha,
            seed=args.seed,
            cache_enabled=cache_enabled,
            run_id=run_id,
            models=models,
        )

    require_key = args.require_key and not args.allow_missing_key
    key_ok, key_reason = validate_openrouter_key()
    if require_key and not key_ok:
        return _write_stop(
            out_dir,
            status=STATUS_MISSING_KEYS,
            reason=key_reason,
            pack=pack,
            git_sha=git_sha,
            seed=args.seed,
            cache_enabled=cache_enabled,
            run_id=run_id,
            models=models,
        )

    if args.attack_n != LOCKED_N_ATTACK or args.benign_n != LOCKED_N_BENIGN:
        return _write_stop(
            out_dir,
            status=STATUS_BLOCKED,
            reason=(
                f"N must be locked {LOCKED_N_ATTACK}+{LOCKED_N_BENIGN}; "
                f"got {args.attack_n}+{args.benign_n}"
            ),
            pack=pack,
            git_sha=git_sha,
            seed=args.seed,
            cache_enabled=cache_enabled,
            run_id=run_id,
            models=models,
        )

    if args.skip_live:
        write_text(out_dir / "STATUS.txt", "PREFLIGHT_OK\n")
        print(f"PREFLIGHT_OK out={out_dir}")
        return 0

    if cache_enabled:
        return _write_stop(
            out_dir,
            status=STATUS_BLOCKED,
            reason="cache.enabled must be false for VNEXT confirmation",
            pack=pack,
            git_sha=git_sha,
            seed=args.seed,
            cache_enabled=cache_enabled,
            run_id=run_id,
            models=models,
        )

    from src.adapti_guard.experiments.real_llm_pipeline import (
        EvaluationBackend,
        PipelineConfig,
        run_real_llm_pipeline,
    )

    config = PipelineConfig(
        experiment_id=args.experiment_id,
        output_dir=out_dir,
        target_config_key=args.target,
        judge_config_key=args.judge,
        backend=EvaluationBackend(args.backend),
        baselines=list(args.baselines),
        split=args.split,
        attack_n=args.attack_n,
        benign_n=args.benign_n,
        seed=args.seed,
        benchmark_dir=str(ROOT / args.benchmark_dir)
        if not Path(args.benchmark_dir).is_absolute()
        else args.benchmark_dir,
    )
    print("VNEXT confirmation LIVE eval")
    print(f"  out: {out_dir}")
    print(f"  pack: {LOCKED_PACK_SHA256}")
    print(f"  arms: {config.baselines} (treatment name {TREATMENT_NAME})")
    result = run_real_llm_pipeline(config)
    write_json(out_dir / "pipeline_result.json", result if isinstance(result, dict) else {"result": str(result)})
    if not isinstance(result, dict) or result.get("status") != "COMPLETED":
        reason = str((result or {}).get("reason") if isinstance(result, dict) else result)
        return _write_stop(
            out_dir,
            status=STATUS_BLOCKED,
            reason=reason or "pipeline did not COMPLETED",
            pack=pack,
            git_sha=git_sha,
            seed=args.seed,
            cache_enabled=cache_enabled,
            run_id=result.get("run_dir", run_id) if isinstance(result, dict) else run_id,
            models=models,
        )

    provenance_run = str(result.get("run_dir") or run_id)
    posted = _postprocess(
        out_dir,
        git_sha=git_sha,
        seed=args.seed,
        cache_enabled=cache_enabled,
        run_id=provenance_run,
    )
    print(json.dumps({
        "status": posted["status"],
        "msid_gate": posted["score"]["msid_gate"],
        "qualified_win": posted["score"]["qualified_win"],
        "delta_attributed": posted["score"]["delta_attributed"],
        "llm_spend_usd": posted["spend"],
        "out": str(out_dir),
    }, indent=2))
    del extra
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
