import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC))

from adapti_guard.core import (
    AttackerType,
    DefenseAction,
    DetectionResult,
    Interaction,
    RiskAssessment,
    RiskLevel,
)


def test_detection_probability_is_bounded():
    result = DetectionResult(1.5)

    assert result.injection_probability == 1.0


def test_risk_score_is_bounded():
    result = RiskAssessment(
        score=-0.5,
        level=RiskLevel.LOW,
    )

    assert result.score == 0.0


def test_interaction_creation():
    interaction = Interaction(
        interaction_id="i-001",
        task_id="task-001",
        user_input="Hello",
        attacker_type=AttackerType.STATIC,
    )

    assert interaction.task_id == "task-001"
    assert interaction.attacker_type == AttackerType.STATIC


def test_defense_actions():
    assert DefenseAction.NO_INTERVENTION.value == "A0"
    assert DefenseAction.SANITIZE.value == "A1"
    assert DefenseAction.TOOL_RESTRICTION.value == "A2"
    assert DefenseAction.BLOCK.value == "A3"
