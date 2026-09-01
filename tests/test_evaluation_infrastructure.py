"""Tests for evaluation infrastructure."""

import pytest

from src.adapti_guard.evaluation.experiment_logging import ExperimentRunContext, redact_env
from src.adapti_guard.evaluation.statistics import bootstrap_ci, mcnemar_test
from src.adapti_guard.evaluation.target_model import GenerationRequest, MockTargetModel


def test_redact_env_no_secret():
    env = redact_env()
    assert "key_present" in env
    assert env.get("openrouter_api_key") in (None, "***REDACTED***")


def test_mock_target():
    m = MockTargetModel("ok")
    r = m.generate(GenerationRequest(prompt="hi"))
    assert r.text == "ok"


def test_bootstrap_ci():
    point, low, high = bootstrap_ci([0.0, 1.0, 0.0, 1.0], n_bootstrap=200, seed=1)
    assert low <= point <= high


def test_mcnemar_identical():
    a = [True, False, True]
    assert mcnemar_test(a, a)["p_value"] == 1.0


def test_experiment_context(tmp_path):
    with ExperimentRunContext.create("EXP-T", runs_root=tmp_path) as ctx:
        ctx.write_metrics({"status": "PASS"})
        assert (ctx.run_dir / "metrics.json").exists()
