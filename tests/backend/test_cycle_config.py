import pytest
from backend.cycle_config import CycleConfig
from backend.cycle_action import CycleAction, ActionType

def test_invalid_cycle_duration():
    with pytest.raises(ValueError):
        CycleConfig(
            cycle_id="bad",
            cycle_name="Invalid",
            cycle_duration_ms=0,
            actions=[]
        )

def test_action_exceeds_duration():
    from backend.cycle_action import CycleAction, ActionType

    with pytest.raises(ValueError):
        CycleConfig(
            cycle_id="bad",
            cycle_name="Invalid",
            cycle_duration_ms=1000,
            actions=[
                CycleAction(2000, ActionType.LIGHT_ON, {})
            ]
        )

def test_to_json_writes_file(tmp_path):
    from backend.cycle_action import CycleAction, ActionType

    cycle = CycleConfig(
        cycle_id="test",
        cycle_name="Test Cycle",
        cycle_duration_ms=1000,
        actions=[
            CycleAction(0, ActionType.LIGHT_ON, {"intensity": 50})
        ]
    )

    file_path = tmp_path / "cycle.json"
    cycle.to_json(file_path)

    assert file_path.exists()

import json

def test_to_json_format(tmp_path):
    from backend.cycle_action import CycleAction, ActionType

    cycle = CycleConfig(
        cycle_id="test",
        cycle_name="Test Cycle",
        cycle_duration_ms=1000,
        actions=[
            CycleAction(0, ActionType.LIGHT_ON, {"intensity": 50})
        ]
    )

    file_path = tmp_path / "cycle.json"
    cycle.to_json(file_path)

    data = json.loads(file_path.read_text())

    assert data == {
        "id": "test",
        "name": "Test Cycle",
        "duration_ms": 1000,
        "actions": [
            {
                "timestamp_ms": 0,
                "type": ActionType.LIGHT_ON.value,
                "params": {"intensity": 50}
            }
        ]
    }

def test_from_json_round_trip(tmp_path):
    from backend.cycle_action import CycleAction, ActionType

    cycle = CycleConfig(
        cycle_id="test",
        cycle_name="Test Cycle",
        cycle_duration_ms=1000,
        actions=[
            CycleAction(0, ActionType.LIGHT_ON, {"intensity": 50})
        ]
    )

    file_path = tmp_path / "cycle.json"
    cycle.to_json(file_path)

    loaded = CycleConfig.from_json(file_path)

    assert loaded.cycle_id == cycle.cycle_id
    assert loaded.cycle_name == cycle.cycle_name
    assert loaded.cycle_duration_ms == cycle.cycle_duration_ms
    assert len(loaded.actions) == 1

def test_actions_are_sorted():
    from backend.cycle_action import CycleAction, ActionType

    cycle = CycleConfig(
        cycle_id="test",
        cycle_name="Test",
        cycle_duration_ms=1000,
        actions=[
            CycleAction(500, ActionType.LIGHT_ON, {}),
            CycleAction(100, ActionType.LIGHT_OFF, {})
        ]
    )

    assert cycle.actions[0].timestamp_ms == 100

def test_add_action_invalid():
    from backend.cycle_action import CycleAction, ActionType

    cycle = CycleConfig("id", "name", 1000)

    with pytest.raises(ValueError):
        cycle.add_action(CycleAction(2000, ActionType.LIGHT_ON, {}))