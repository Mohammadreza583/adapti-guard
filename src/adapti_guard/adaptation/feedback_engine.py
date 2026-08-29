from dataclasses import dataclass

from src.adapti_guard.evaluation.outcome_evaluator import OutcomeResult


@dataclass
class FeedbackSignal:
    reward: float
    security_feedback: float
    utility_feedback: float
    cost_penalty: float
    adaptation_signal: str


class FeedbackEngine:
    """
    Converts evaluation outcomes into adaptive feedback.

    The feedback balances:

        Security
        Utility
        Defense Cost

    A legitimate task blocked by strong defense is treated
    as evidence that the policy is too restrictive.
    """

    def __init__(
        self,
        security_weight: float = 0.5,
        utility_weight: float = 0.4,
        cost_weight: float = 0.1,
    ):
        self.security_weight = security_weight
        self.utility_weight = utility_weight
        self.cost_weight = cost_weight

    def generate(
        self,
        outcome: OutcomeResult,
    ) -> FeedbackSignal:

        security_feedback = outcome.security_score
        utility_feedback = outcome.utility_score
        cost_penalty = outcome.defense_cost

        reward = (
            self.security_weight * security_feedback
            + self.utility_weight * utility_feedback
            - self.cost_weight * cost_penalty
        )

        # -------------------------------------------------
        # Adaptive signals
        # -------------------------------------------------

        if outcome.attack_success:

            adaptation_signal = "INCREASE_DEFENSE"

        elif (
            outcome.legitimate_task
            and outcome.legitimate_success
            and outcome.defense_cost >= 0.25
        ):

            # Legitimate request succeeded despite
            # unnecessarily expensive defense.
            adaptation_signal = "REDUCE_DEFENSE"

        elif (
            outcome.legitimate_task
            and not outcome.legitimate_success
            and outcome.defense_cost >= 0.50
        ):

            # Strong defense blocked a legitimate task.
            adaptation_signal = "REDUCE_DEFENSE"

        else:

            adaptation_signal = "MAINTAIN"

        return FeedbackSignal(
            reward=reward,
            security_feedback=security_feedback,
            utility_feedback=utility_feedback,
            cost_penalty=cost_penalty,
            adaptation_signal=adaptation_signal,
        )
