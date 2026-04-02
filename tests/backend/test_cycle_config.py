import pytest
from backend.cycle_config import CycleConfig
from backend.cycle_action import CycleAction, ActionType

def test_invalid_cycle_duration():
    with pytest.raises(ValueError):
        CycleConfig(
            cycle_id="bad",
            cycle_name="Invalid",
            cycle_duration_ms=0,
            light_configuration=50,
            actions=[]
        )

def test_action_exceeds_duration():
    from backend.cycle_action import CycleAction, ActionType

    with pytest.raises(ValueError):
        CycleConfig(
            cycle_id="bad",
            cycle_name="Invalid",
            cycle_duration_ms=1000,
            light_configuration=50,
            actions=[
                CycleAction(2000, ActionType.SOUND_START, {})
            ]
        )

def test_actions_are_sorted():
    from backend.cycle_action import CycleAction, ActionType

    cycle = CycleConfig(
        cycle_id="test",
        cycle_name="Test",
        cycle_duration_ms=1000,
        light_configuration=50,
        actions=[
            CycleAction(500, ActionType.SOUND_START, {}),
            CycleAction(100, ActionType.SOUND_START, {})
        ]
    )

    assert cycle.actions[0].timestamp_ms == 100

def test_add_action_invalid():
    from backend.cycle_action import CycleAction, ActionType

    cycle = CycleConfig("id", "name", 1000, 50)

    with pytest.raises(ValueError):
        cycle.add_action(CycleAction(2000, ActionType.SOUND_START, {}))