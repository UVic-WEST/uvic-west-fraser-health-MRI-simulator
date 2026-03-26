"""
Unit tests for verifying that sound actions are correctly saved, loaded,
and associated with cycles in the CycleRepository.

Tests cover:
- Writing sound actions to JSON
- Preserving sound actions per cycle
- Round-trip save/load integrity
- Preservation of action parameters
- Handling cycles with no sound actions
"""

def test_sound_actions_written_to_repository(tmp_path, monkeypatch):
    """
    Verify that a SOUND_START action is correctly serialized to the cycles.json file.
    """
    from backend.cycle_repository import CycleRepository
    from backend.cycle_config import CycleConfig
    from backend.cycle_action import CycleAction, ActionType

    test_file = tmp_path / "cycles.json"
    monkeypatch.setattr("backend.cycle_repository.CYCLE_FILE", test_file)

    cycle = CycleConfig(
        cycle_id=1,
        cycle_name="Test",
        cycle_duration_ms=1000,
        actions=[
            CycleAction(0, ActionType.SOUND_START, {"volume": 50})
        ]
    )

    CycleRepository.save_all([cycle])
    data = json.loads(test_file.read_text())

    assert data[0]["actions"][0]["type"] == ActionType.SOUND_START.value

def test_sound_actions_associated_with_correct_cycle(tmp_path, monkeypatch):
    """
    Verify that sound actions are associated only with the intended cycle.
    """
    from backend.cycle_repository import CycleRepository
    from backend.cycle_config import CycleConfig
    from backend.cycle_action import CycleAction, ActionType

    test_file = tmp_path / "cycles.json"
    monkeypatch.setattr("backend.cycle_repository.CYCLE_FILE", test_file)

    cycle1 = CycleConfig(
        cycle_id=1,
        cycle_name="Cycle 1",
        cycle_duration_ms=1000,
        actions=[CycleAction(0, ActionType.SOUND_START, {})]
    )

    cycle2 = CycleConfig(
        cycle_id=2,
        cycle_name="Cycle 2",
        cycle_duration_ms=1000,
        actions=[]
    )

    CycleRepository.save_all([cycle1, cycle2])
    loaded = CycleRepository.load_all()

    c1 = next(c for c in loaded if c.cycle_id == 1)
    c2 = next(c for c in loaded if c.cycle_id == 2)

    assert any(a.action_type == ActionType.SOUND_START for a in c1.actions)
    assert not any(a.action_type == ActionType.SOUND_START for a in c2.actions)

def test_sound_actions_round_trip(tmp_path, monkeypatch):
    """
    Verify that sound actions survive a save/load round-trip without changes.
    """
    from backend.cycle_repository import CycleRepository
    from backend.cycle_config import CycleConfig
    from backend.cycle_action import CycleAction, ActionType

    test_file = tmp_path / "cycles.json"
    monkeypatch.setattr("backend.cycle_repository.CYCLE_FILE", test_file)

    cycle = CycleConfig(
        cycle_id=1,
        cycle_name="Test",
        cycle_duration_ms=1000,
        actions=[
            CycleAction(0, ActionType.SOUND_START, {"volume": 50}),
            CycleAction(500, ActionType.SOUND_STOP, {})
        ]
    )

    CycleRepository.save_all([cycle])
    loaded = CycleRepository.load_all()

    loaded_actions = loaded[0].actions

    assert len(loaded_actions) == 2
    assert loaded_actions[0].action_type == ActionType.SOUND_START
    assert loaded_actions[1].action_type == ActionType.SOUND_STOP

def test_sound_action_parameters_preserved(tmp_path, monkeypatch):
    """
    Verify that parameters of sound actions (e.g., volume) are preserved during save/load.
    """
    from backend.cycle_repository import CycleRepository
    from backend.cycle_config import CycleConfig
    from backend.cycle_action import CycleAction, ActionType

    test_file = tmp_path / "cycles.json"
    monkeypatch.setattr("backend.cycle_repository.CYCLE_FILE", test_file)

    cycle = CycleConfig(
        cycle_id=1,
        cycle_name="Test",
        cycle_duration_ms=1000,
        actions=[
            CycleAction(0, ActionType.SOUND_START, {"volume": 75})
        ]
    )

    CycleRepository.save_all([cycle])
    loaded = CycleRepository.load_all()

    action = loaded[0].actions[0]

    assert action.parameters["volume"] == 75

def test_cycle_with_no_sound_actions(tmp_path, monkeypatch):
    """
    Verify that cycles with no sound actions are correctly handled.
    """
    from backend.cycle_repository import CycleRepository
    from backend.cycle_config import CycleConfig

    test_file = tmp_path / "cycles.json"
    monkeypatch.setattr("backend.cycle_repository.CYCLE_FILE", test_file)

    cycle = CycleConfig(
        cycle_id=1,
        cycle_name="No Sound",
        cycle_duration_ms=1000,
        actions=[]
    )

    CycleRepository.save_all([cycle])
    loaded = CycleRepository.load_all()

    assert loaded[0].actions == []