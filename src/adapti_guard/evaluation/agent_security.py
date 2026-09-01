"""Agent security evaluation — requires real agent loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentEvaluationResult:
    attack_success_rate: float | None = None
    unsafe_tool_call_rate: float | None = None
    policy_violation_rate: float | None = None
    task_utility: float | None = None
    status: str = "NOT_RUN"
    notes: str = ""
    details: dict[str, Any] = field(default_factory=dict)


class AgentSecurityEvaluator:
    """
    Architecture: User → Agent Planner → LLM → Tools → Memory

    STATUS: NOT_IMPLEMENTED — no agent environment (AgentDojo/InjecAgent) integrated.
    """

    def __init__(self):
        self.status = "NOT_IMPLEMENTED"

    def evaluate(self, scenarios: list[dict]) -> AgentEvaluationResult:
        return AgentEvaluationResult(
            status="BLOCKED",
            notes="Agent evaluation environment not implemented. Integrate AgentDojo or InjecAgent.",
        )
