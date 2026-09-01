"""ML classifier detector — TF-IDF + LogisticRegression with optional transformers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from src.adapti_guard.core.models import DetectionResult
from src.adapti_guard.detectors.regex_detector import Detector


class MLDetector(Detector):
    """
    Lightweight ML detector using TF-IDF features.
    Optional HuggingFace transformers (DeBERTa/RoBERTa) when model_name is set
    and transformers/torch are installed.
    """

    def __init__(
        self,
        *,
        model_name: str | None = None,
        model_path: str | Path | None = None,
        threshold: float = 0.5,
    ):
        self.model_name = model_name
        self.model_path = Path(model_path) if model_path else None
        self.threshold = threshold
        self._vectorizer = None
        self._classifier = None
        self._hf_pipeline = None
        self._backend = "untrained"

        if model_name and self._try_load_transformers(model_name):
            self._backend = f"transformers:{model_name}"
        elif self.model_path and self.model_path.exists():
            self._load_sklearn(self.model_path)
            self._backend = f"sklearn:{self.model_path.name}"
        else:
            self._init_sklearn()

    def _try_load_transformers(self, model_name: str) -> bool:
        try:
            from transformers import pipeline

            self._hf_pipeline = pipeline(
                "text-classification",
                model=model_name,
                truncation=True,
                max_length=512,
            )
            return True
        except Exception:
            self._hf_pipeline = None
            return False

    def _init_sklearn(self) -> None:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression

        self._vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        self._classifier = LogisticRegression(max_iter=500)
        self._backend = "sklearn:untrained"

    def _load_sklearn(self, path: Path) -> None:
        import joblib

        bundle = joblib.load(path)
        self._vectorizer = bundle["vectorizer"]
        self._classifier = bundle["classifier"]

    def save_sklearn(self, path: str | Path) -> None:
        import joblib

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"vectorizer": self._vectorizer, "classifier": self._classifier}, path)

    def fit(self, texts: list[str], labels: list[int]) -> dict[str, Any]:
        if self._hf_pipeline is not None:
            return {"status": "SKIP", "reason": "transformers_pipeline_is_pretrained"}
        if self._vectorizer is None or self._classifier is None:
            self._init_sklearn()
        X = self._vectorizer.fit_transform(texts)
        self._classifier.fit(X, labels)
        self._backend = "sklearn:trained"
        return {"status": "DONE", "n_samples": len(texts)}

    def predict_proba(self, text: str) -> float:
        if self._hf_pipeline is not None:
            out = self._hf_pipeline(text)[0]
            label = str(out.get("label", "")).lower()
            score = float(out.get("score", 0.5))
            if label in {"label_1", "toxic", "injection", "unsafe", "1"}:
                return score
            return 1.0 - score

        if self._vectorizer is None or self._classifier is None:
            return 0.0
        if not hasattr(self._classifier, "classes_"):
            return 0.0
        X = self._vectorizer.transform([text])
        proba = self._classifier.predict_proba(X)[0]
        classes = list(self._classifier.classes_)
        idx = classes.index(1) if 1 in classes else -1
        return float(proba[idx]) if idx >= 0 else float(proba.max())

    def detect(self, text: str) -> DetectionResult:
        score = self.predict_proba(text)
        return DetectionResult(
            injection_probability=score,
            indicators=[f"ml:{self._backend}"],
        )

    @property
    def version(self) -> str:
        return f"ml_{self._backend}"

    def evaluate_classifier(
        self,
        texts: list[str],
        labels: list[int],
    ) -> dict[str, float]:
        from sklearn.metrics import (
            accuracy_score,
            average_precision_score,
            f1_score,
            precision_score,
            recall_score,
            roc_auc_score,
        )

        y_true = np.asarray(labels, dtype=int)
        y_score = np.array([self.predict_proba(t) for t in texts], dtype=float)
        y_pred = (y_score >= self.threshold).astype(int)

        metrics: dict[str, float] = {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred, zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        }
        if len(set(labels)) > 1:
            metrics["auroc"] = float(roc_auc_score(y_true, y_score))
            metrics["auprc"] = float(average_precision_score(y_true, y_score))
        else:
            metrics["auroc"] = 0.0
            metrics["auprc"] = 0.0
        return metrics


def train_ml_detector_from_benchmark(
    benchmark_dir: str | Path = "datasets/benchmark_v4",
    output_path: str | Path = "models/ml_detector_sklearn.joblib",
) -> dict[str, Any]:
    benchmark_dir = Path(benchmark_dir)
    train_path = benchmark_dir / "train.jsonl"
    val_path = benchmark_dir / "validation.jsonl"

    def load_rows(path: Path) -> list[dict]:
        if not path.exists():
            return []
        rows = []
        with path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
        return rows

    train_rows = load_rows(train_path)
    val_rows = load_rows(val_path)
    if not train_rows:
        return {"status": "BLOCKED", "reason": "no_train_data"}

    detector = MLDetector()
    fit_info = detector.fit(
        [r["prompt"] for r in train_rows],
        [int(r["label"]) for r in train_rows],
    )
    metrics = {}
    if val_rows:
        metrics = detector.evaluate_classifier(
            [r["prompt"] for r in val_rows],
            [int(r["label"]) for r in val_rows],
        )
    detector.save_sklearn(output_path)
    return {"status": "DONE", "fit": fit_info, "validation_metrics": metrics, "model_path": str(output_path)}
