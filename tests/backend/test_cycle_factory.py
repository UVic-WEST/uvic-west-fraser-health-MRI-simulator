import pytest

from backend.cycle_factory import CycleFactory
from backend.cycle_action import ActionType


@pytest.fixture
def factory():
    return CycleFactory()


def test_cycles_loaded(factory):
    """Factory should load predefined cycles on initialization."""
    cycles = factory.list_cycles()
    assert len(cycles) >= 2


def test_get_cycle_by_id_valid(factory):
    """Should return correct cycle when ID exists."""
    cycle = factory.get_cycle_by_id("scan_1")

    assert cycle.cycle_id == "scan_1"
    assert cycle.cycle_name == "Standard MRI"
    assert cycle.cycle_duration_ms == 10000
    assert len(cycle.actions) == 4


def test_get_cycle_by_id_invalid(factory):
    """Should raise ValueError when cycle ID does not exist."""
    with pytest.raises(ValueError) as exc:
        factory.get_cycle_by_id("invalid_id")

    assert "No cycle with id" in str(exc.value)


def test_get_cycle_by_index_valid(factory):
    """Should return correct cycle when index exists."""
    cycle = factory.get_cycle_by_index(0)

    assert cycle.cycle_id == "scan_1"


def test_get_cycle_by_index_invalid(factory):
    """Should raise ValueError when index is out of range."""
    with pytest.raises(ValueError) as exc:
        factory.get_cycle_by_index(999)

    assert "No cycle at index" in str(exc.value)


def test_list_cycles_returns_copy(factory):
    """list_cycles should return a new list, not internal reference."""
    cycles = factory.list_cycles()
    cycles.pop()

    # Original internal list should remain unchanged
    assert len(factory.list_cycles()) >= 2


def test_cycle1_actions(factory):
    """Verify structure of actions in cycle1."""
    cycle = factory.get_cycle_by_id("scan_1")

    assert cycle.actions[0].timestamp_ms == 0
    assert cycle.actions[0].action_type == ActionType.LIGHT_ON

    assert cycle.actions[1].action_type == ActionType.SOUND_START
    assert cycle.actions[2].action_type == ActionType.LIGHT_OFF
    assert cycle.actions[3].action_type == ActionType.SOUND_STOP


def test_cycle2_actions(factory):
    """Verify structure of actions in cycle2."""
    cycle = factory.get_cycle_by_id("scan_2")

    assert cycle.cycle_duration_ms == 5000
    assert len(cycle.actions) == 3
    assert cycle.actions[0].action_type == ActionType.LIGHT_ON
    assert cycle.actions[1].action_type == ActionType.SOUND_START
    assert cycle.actions[2].action_type == ActionType.SOUND_STOP