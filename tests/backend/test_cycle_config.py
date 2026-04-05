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


def test_cycle_config_getters():
    """Getters for name, duration, brightness, sound group mapping."""
    from backend.cycle_action import CycleAction, ActionType

    actions = [
        CycleAction(
            0,
            ActionType.SOUND_START,
            {"file_name": "resources/sounds/foo_1.wav", "volume": 60, "duration_ms": 5000},
        ),
        CycleAction(
            0,
            ActionType.SOUND_START,
            {"file_name": "resources/sounds/bar_2.wav", "volume": 60, "duration_ms": 5000},
        ),
        CycleAction(
            5000,
            ActionType.SOUND_START,
            {"file_name": "buzz.wav", "volume": 40},
        ),
    ]
    cycle = CycleConfig(1, "Morning scan", 10_000, 80, actions=actions)

    assert cycle.get_cycle_name() == "Morning scan"
    assert cycle.get_duration_ms() == 10_000
    assert cycle.get_duration_sec() == 10.0
    assert cycle.get_brightness() == 80

    mapping = cycle.get_sound_group_mapping()
    assert cycle.get_total_groups() == 2
    assert mapping[1]["sound_names"] == ["foo_1.wav", "bar_2.wav"]
    assert mapping[1]["volume"] == 60
    assert mapping[2]["sound_names"] == ["buzz.wav"]
    assert mapping[2]["volume"] == 40


def test_get_sound_group_mapping_empty():
    cycle = CycleConfig(1, "Empty", 1000, 50, actions=[])
    assert cycle.get_sound_group_mapping() == {}
    assert cycle.get_total_groups() == 0


def test_to_dict_includes_lights_and_volume():
    cycle = CycleConfig(
        1,
        "Test",
        1000,
        70,
        lights_on=False,
        volume=60,
        actions=[],
    )
    d = cycle.to_dict()
    assert d["lights"] == {"on": False, "brightness": 70}
    assert d["volume"] == 60
    assert d["light_configuration"] == 70


def test_from_dict_legacy_without_lights_key():
    """Older JSON without ``lights`` / ``volume`` still loads."""
    data = {
        "id": 1,
        "name": "Legacy",
        "duration_ms": 5000,
        "light_configuration": 40,
        "actions": [],
    }
    c = CycleConfig.from_dict(data)
    assert c.lights_on is True
    assert c.light_configuration == 40
    assert c.volume == 50


def test_from_dict_nested_lights():
    data = {
        "id": 2,
        "name": "Nested",
        "duration_ms": 5000,
        "lights": {"on": False, "brightness": 30},
        "volume": 55,
        "actions": [],
    }
    c = CycleConfig.from_dict(data)
    assert c.lights_on is False
    assert c.light_configuration == 30
    assert c.get_brightness() == 30
    assert c.volume == 55