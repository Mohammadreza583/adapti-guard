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

    Ablation flags (defaults preserve Phase7 behavior):
        enable_escalation — emit INCREASE_DEFENSE on attack success
        enable_deescalation — emit REDUCE_DEFENSE on legitimate/cost evidence
        use_cost_gate — require defense_cost thresholds for de-escalation
    """

    def __init__(
        self,
        security_weight: float = 0.5,
        utility_weight: float = 0.4,
        cost_weight: float = 0.1,
        enable_escalation: bool = True,
        enable_deescalation: bool = True,
        use_cost_gate: bool = True,
    ):
        self.security_weight = security_weight
        self.utility_weight = utility_weight
        self.cost_weight = cost_weight
        self.enable_escalation = enable_escalation
        self.enable_deescalation = enable_deescalation
        self.use_cost_gate = use_cost_gate

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

        success_cost_threshold = 0.25 if self.use_cost_gate else 0.0
        block_cost_threshold = 0.50 if self.use_cost_gate else 0.0

        if outcome.attack_success and self.enable_escalation:

            adaptation_signal = "INCREASE_DEFENSE"

        elif (
            self.enable_deescalation
            and outcome.legitimate_task
            and outcome.legitimate_success
            and outcome.defense_cost >= success_cost_threshold
        ):

            # Legitimate request succeeded despite
            # unnecessarily expensive defense.
            adaptation_signal = "REDUCE_DEFENSE"

        elif (
            self.enable_deescalation
            and outcome.legitimate_task
            and not outcome.legitimate_success
            and outcome.defense_cost >= block_cost_threshold
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
