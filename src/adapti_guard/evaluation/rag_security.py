"""RAG security evaluation — requires real retrieval pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RAGEvaluationResult:
    attack_success_rate: float | None = None
    answer_manipulation_rate: float | None = None
    retrieval_failure_rate: float | None = None
    status: str = "NOT_RUN"
    notes: str = ""
    details: dict[str, Any] = field(default_factory=dict)


class RAGSecurityEvaluator:
    """
    Architecture: Documents → Embedding → Vector DB → Retriever → LLM

    STATUS: NOT_IMPLEMENTED — no vector database or embedding pipeline in repo.
    """

    def __init__(self):
        self.status = "NOT_IMPLEMENTED"

    def evaluate(self, samples: list[dict]) -> RAGEvaluationResult:
        return RAGEvaluationResult(
            status="BLOCKED",
            notes="RAG pipeline not implemented. Requires embedding model, vector store, and retriever.",
        )
