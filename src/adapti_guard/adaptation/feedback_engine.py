from dataclasses import dataclass

from src.adapti_guard.evaluation.outcome_evaluator import (
    OutcomeResult,
)


@dataclass
class FeedbackSignal:
    reward: float
    security_feedback: float
    utility_feedback: float
    cost_penalty: float
    adaptation_signal: str


class FeedbackEngine:

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

        # ---------------------------------------------------------
        # UTILITY-AWARE ADAPTATION
        # ---------------------------------------------------------

        # 1. Legitimate request was blocked/rejected.
        #    This is a utility failure and should reduce defense.
        if (
            outcome.legitimate_success
            and cost_penalty >= 0.50
        ):
            signal = "REDUCE_DEFENSE"

        elif (
            not outcome.legitimate_success
            and utility_feedback == 0.0
            and cost_penalty >= 0.50
        ):
            signal = "REDUCE_DEFENSE"

        # 2. Attack successfully bypassed the defense.
        elif outcome.attack_success:
            signal = "INCREASE_DEFENSE"

        # 3. Attack was contained.
        #    Continued attack pressure is evidence for stronger defense.
        elif (
            security_feedback >= 1.0
            and utility_feedback == 0.0
            and cost_penalty < 0.50
        ):
            signal = "INCREASE_DEFENSE"

        # 4. Legitimate task succeeded with acceptable cost.
        elif outcome.legitimate_success:
            signal = "MAINTAIN"

        else:
            signal = "MAINTAIN"

        return FeedbackSignal(
            reward=round(reward, 4),
            security_feedback=security_feedback,
            utility_feedback=utility_feedback,
            cost_penalty=cost_penalty,
            adaptation_signal=signal,
        )
