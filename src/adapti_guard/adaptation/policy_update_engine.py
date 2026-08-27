from dataclasses import dataclass

from src.adapti_guard.adaptation.feedback_engine import FeedbackSignal
from src.adapti_guard.core.models import DefenseAction


@dataclass
class PolicyState:
    defense_level: int = 0
    attack_failures: int = 0
    legitimate_failures: int = 0
    successful_attacks: int = 0
    total_updates: int = 0


class PolicyUpdateEngine:
    """
    Evidence-based adaptive policy update.

    Defense increases after repeated successful attacks.
    Defense decreases after repeated evidence that the current
    defense is unnecessarily restrictive.
    """

    def __init__(
        self,
        attack_threshold: int = 2,
        legitimate_threshold: int = 2,
    ):
        self.attack_threshold = attack_threshold
        self.legitimate_threshold = legitimate_threshold

    def update(
        self,
        state: PolicyState,
        feedback: FeedbackSignal,
    ) -> PolicyState:

        if feedback.adaptation_signal == "INCREASE_DEFENSE":
            state.attack_failures += 1
            state.successful_attacks += 1

        elif feedback.adaptation_signal == "REDUCE_DEFENSE":
            state.legitimate_failures += 1

        if state.attack_failures >= self.attack_threshold:
            if state.defense_level < 3:
                state.defense_level += 1
                state.total_updates += 1

            state.attack_failures = 0

        if state.legitimate_failures >= self.legitimate_threshold:
            if state.defense_level > 0:
                state.defense_level -= 1
                state.total_updates += 1

            state.legitimate_failures = 0

        return state

    @staticmethod
    def action_for_level(level: int) -> DefenseAction:

        mapping = {
            0: DefenseAction.NO_INTERVENTION,
            1: DefenseAction.SANITIZE,
            2: DefenseAction.TOOL_RESTRICTION,
            3: DefenseAction.BLOCK,
        }

        if level not in mapping:
            raise ValueError(
                f"Unsupported defense level: {level}"
            )

        return mapping[level]
