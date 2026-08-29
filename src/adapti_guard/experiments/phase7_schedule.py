"""
Phase 7 controlled evaluation schedule.

Deterministic workload (True = legitimate, False = attack):

    pattern = [attack, attack, attack, legitimate] x 25

Totals:
    100 episodes
    75 attack
    25 legitimate

This list is the single authoritative episode classification
for all Phase 7 methods (Fixed-L0..L3 and Adaptive).
Controlled runners must not re-derive class via episode_id % 4.
"""

PHASE7_EPISODES = 100
PHASE7_ATTACK_COUNT = 75
PHASE7_LEGITIMATE_COUNT = 25

# True = legitimate task, False = attack episode
PHASE7_EPISODE_SCHEDULE: list[bool] = (
    [False, False, False, True] * 25
)

# Attack-stream mapping for Phase 7:
# use the first 75 records of results/common_attack_stream.json
# in sequential order for the 75 attack slots.
PHASE7_ATTACK_STREAM_SLICE = (0, 75)
PHASE7_ATTACK_STREAM_NAME = "common_attack_stream_v1_first_75"


def validate_phase7_schedule(schedule=None) -> list[bool]:
    schedule = list(schedule or PHASE7_EPISODE_SCHEDULE)

    if len(schedule) != PHASE7_EPISODES:
        raise ValueError(
            f"Phase 7 schedule must have {PHASE7_EPISODES} entries, "
            f"got {len(schedule)}"
        )

    legitimate = sum(1 for x in schedule if x)
    attack = len(schedule) - legitimate

    if attack != PHASE7_ATTACK_COUNT or legitimate != PHASE7_LEGITIMATE_COUNT:
        raise ValueError(
            "Phase 7 schedule must contain "
            f"{PHASE7_ATTACK_COUNT} attacks and "
            f"{PHASE7_LEGITIMATE_COUNT} legitimate episodes; "
            f"got attack={attack}, legitimate={legitimate}"
        )

    return schedule
