"""Adaptive defense controllers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.adapti_guard.adaptation.feedback_engine import FeedbackEngine, FeedbackSignal
from src.adapti_guard.adaptation.policy_update_engine import PolicyState, PolicyUpdateEngine
from src.adapti_guard.evaluation.outcome_evaluator import OutcomeResult


@dataclass
class ControllerDecision:
    defense_level: int
    reason: str
    controller_type: str


class AdaptiveController(ABC):
    @abstractmethod
    def step(self, feedback: FeedbackSignal, state: PolicyState) -> PolicyState:
        raise NotImplementedError


class RuleBasedController(AdaptiveController):
    """Current threshold-based PolicyUpdateEngine (non-learning)."""

    def __init__(self, attack_threshold: int = 2, legitimate_threshold: int = 2):
        self.engine = PolicyUpdateEngine(
            attack_threshold=attack_threshold,
            legitimate_threshold=legitimate_threshold,
        )

    def step(self, feedback: FeedbackSignal, state: PolicyState) -> PolicyState:
        return self.engine.update(state, feedback)

    @property
    def controller_type(self) -> str:
        return "rule_based_threshold"


class BayesianRiskController(AdaptiveController):
    """
    Bayesian-inspired risk controller: maintains Beta prior on attack success rate.
    Escalates when posterior mean exceeds threshold.
    """

    def __init__(
        self,
        alpha_prior: float = 1.0,
        beta_prior: float = 9.0,
        escalate_threshold: float = 0.35,
        deescalate_threshold: float = 0.10,
    ):
        self.alpha = alpha_prior
        self.beta = beta_prior
        self.escalate_threshold = escalate_threshold
        self.deescalate_threshold = deescalate_threshold

    def step(self, feedback: FeedbackSignal, state: PolicyState) -> PolicyState:
        if feedback.attack_success:
            self.alpha += 1.0
        elif feedback.adaptation_signal == "INCREASE_DEFENSE":
            self.beta += 0.5

        posterior_mean = self.alpha / (self.alpha + self.beta)

        if posterior_mean >= self.escalate_threshold and state.defense_level < 3:
            prev = state.defense_level
            state.defense_level += 1
            state.transition_history.append((prev, state.defense_level))
            state.total_updates += 1
        elif posterior_mean <= self.deescalate_threshold and state.defense_level > 0:
            prev = state.defense_level
            state.defense_level -= 1
            state.transition_history.append((prev, state.defense_level))
            state.total_updates += 1

        return state

    @property
    def controller_type(self) -> str:
        return "bayesian_risk"


class ContextAwarePolicyController(AdaptiveController):
    """
    Context-aware controller: weights escalation by observed defense cost and utility.
    Objective (heuristic): maximize security - gamma*cost - delta*utility_loss
    """

    def __init__(self, gamma: float = 0.3, delta: float = 0.4, base: RuleBasedController | None = None):
        self.gamma = gamma
        self.delta = delta
        self.base = base or RuleBasedController()

    def step(self, feedback: FeedbackSignal, state: PolicyState) -> PolicyState:
        security_gain = 1.0 if feedback.adaptation_signal == "INCREASE_DEFENSE" else 0.0
        utility_loss = 1.0 if feedback.adaptation_signal == "REDUCE_DEFENSE" else 0.0
        objective = security_gain - self.gamma * feedback.cost_penalty - self.delta * utility_loss

        if objective > 0.2 and feedback.adaptation_signal == "INCREASE_DEFENSE":
            return self.base.step(feedback, state)
        if objective < -0.1 and feedback.adaptation_signal == "REDUCE_DEFENSE":
            return self.base.step(feedback, state)
        return state

    @property
    def controller_type(self) -> str:
        return "context_aware_policy"
