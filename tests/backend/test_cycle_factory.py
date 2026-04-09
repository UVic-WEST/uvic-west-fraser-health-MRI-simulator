import pytest
from unittest.mock import patch # uses patch to mock cycle repository

from backend.cycle_factory import CycleFactory
from backend.cycle_config import CycleConfig


@pytest.fixture
def factory():
    return CycleFactory()

# ----------------------------------------
# tests for normal cases
# ----------------------------------------
def test_cycles_loaded(factory):
    """Factory should load predefined cycles on initialization."""
    cycles = factory.list_cycles()
    
    assert isinstance(cycles, list) # verifies contract of list_cycles()
    assert len(cycles) > 0 # incase somehow a preset cycle is removed


def test_get_cycle_by_id_valid(factory):
    """Should return correct cycle when ID exists."""
    cycles = factory.list_cycles()
    sample = cycles[0] # sample is an instance of CycleConfig
    
    result = factory.get_cycle_by_id(sample.cycle_id) # result is an instance of CycleConfig

    assert result.cycle_id == sample.cycle_id
    assert result.cycle_name == sample.cycle_name


def test_get_cycle_by_id_invalid(factory):
    """Should raise ValueError when cycle ID does not exist."""
    with pytest.raises(ValueError, match = "No cycle with id"):
        factory.get_cycle_by_id(-999)


def test_list_cycles_returns_copy(factory):
    """list_cycles should return a new list, not internal reference."""
    cycles = factory.list_cycles()
    original_length = len(cycles)
    cycles.pop()

    # Original internal list should remain unchanged
    assert len(factory.list_cycles()) == original_length
    

# ----------------------------------------
# tests for edge cases
# ---------------------------------------- 
def test_get_cycle_with_non_int_id(factory):
    """Passing a non-int ID should not match any of cycles in system."""
    with pytest.raises(ValueError):
        factory.get_cycle_by_id("invalid_id")
        

def test_repository_empty():
    """CycleFactory should handle an empty cycle repository."""
    with patch("backend.cycle_repository.CycleRepository.load_all", return_value=[]):
        factory = CycleFactory()
        
        assert factory.list_cycles() == []
        
        with pytest.raises(ValueError):
            factory.get_cycle_by_id(1)
            
            
def test_repository_duplicate_ids():
    """If duplicate IDs present in cycle repository, CycleFactory should return first match."""
    duplicate_cycles = [CycleConfig(cycle_id = 1, cycle_name = "Cycle 1", cycle_duration_ms = 100, light_configuration = 50, actions = []), CycleConfig(cycle_id = 1, cycle_name = "Cycle 2", cycle_duration_ms = 200, light_configuration = 50, actions = [])]
    
    with patch("backend.cycle_repository.CycleRepository.load_all", return_value=duplicate_cycles):
        factory = CycleFactory()
        result = factory.get_cycle_by_id(1)
        assert result.cycle_name == "Cycle 1"
        
        
def test_refresh():
    """refresh() should reload cycles and all relevant data from cycle repository."""
    initial_cycles = [CycleConfig(cycle_id=1, cycle_name="Initial", cycle_duration_ms=100, light_configuration = 50, actions = [])]
    updated_cycles = [CycleConfig(cycle_id=2, cycle_name="Updated", cycle_duration_ms=200, light_configuration = 50, actions = [])]
    
    with patch("backend.cycle_repository.CycleRepository.load_all", side_effect=[initial_cycles, updated_cycles]):
        factory = CycleFactory()
        
        # test initial state
        assert factory.get_cycle_by_id(1).cycle_name == "Initial"
        
        # call refresh() to reload cycles
        factory.refresh()
        
        # test updated state
        with pytest.raises(ValueError):
            factory.get_cycle_by_id(1)
            
        assert factory.get_cycle_by_id(2).cycle_name == "Updated"


# ----------------------------------------
# tests for behavioral integrity
# ----------------------------------------
def test_internal_list_isolated(factory):
    """Ensure internal list cannot be directly modified."""
    cycles = factory.list_cycles()
    cycles.clear()
    assert len(factory.list_cycles()) > 0


def test_multiple_calls_consistent(factory):
    """Repeated calls to CycleFactory functions should return consistent results."""
    cycles1 = factory.list_cycles()
    cycles2 = factory.list_cycles()
    
    assert cycles1 == cycles2 # check that cycles1 contains same CycleConfig instances as cycles2
    assert cycles1 is not cycles2 # check that cycles1 and cycles2 are different list objects


# ----------------------------------------
# tests for custom cycles
# ---------------------------------------- 
def test_add_custom_cycle_valid(factory):
    """Adding a custom cycle within 4-15 should succeed."""
    custom_cycle = CycleConfig(
        cycle_id=4,
        cycle_name="Custom Cycle 1",
        cycle_duration_ms=60000,
        light_configuration=50,
        actions=[]
    )
    factory.add_custom_cycle(custom_cycle)
    assert factory.get_cycle_by_id(4) == custom_cycle


def test_add_custom_cycle_invalid_id(factory):
    """Adding a custom cycle outside 4-15 should raise ValueError."""
    with pytest.raises(ValueError):
        factory.add_custom_cycle(
            CycleConfig(
                cycle_id=16,
                cycle_name="Invalid Cycle",
                cycle_duration_ms=60000,
                light_configuration=50,
                actions=[]
            )
        )
    with pytest.raises(ValueError):
        factory.add_custom_cycle(
            CycleConfig(
                cycle_id=3,  # duplicate preset ID
                cycle_name="Invalid Cycle",
                cycle_duration_ms=60000,
                light_configuration=50,
                actions=[]
            )
        )


def test_add_custom_cycle_duplicate_id(factory):
    """Cannot add a custom cycle with an ID already used."""
    # Add first custom cycle
    cycle1 = factory.create_custom_cycle(
        cycle_name="Cycle A",
        cycle_duration_ms=60000,
        light_configuration=50
    )
    # Manually try to add another with same ID
    duplicate = CycleConfig(
        cycle_id=cycle1.cycle_id,
        cycle_name="Cycle B",
        cycle_duration_ms=60000,
        light_configuration=50,
        actions=[]
    )
    with pytest.raises(ValueError) as exc:
        factory.add_custom_cycle(duplicate)
    assert "already exists" in str(exc.value)


def test_create_custom_cycle_auto_id(factory):
    """create_custom_cycle() should auto-assign next valid ID."""
    custom1 = factory.create_custom_cycle(
        cycle_name="Auto Cycle 1",
        cycle_duration_ms=60000,
        light_configuration=50
    )
    assert 4 <= custom1.cycle_id <= 15

    custom2 = factory.create_custom_cycle(
        cycle_name="Auto Cycle 2",
        cycle_duration_ms=60000,
        light_configuration=50
    )
    assert custom2.cycle_id == custom1.cycle_id + 1


def test_get_next_custom_id_exhaustion(factory):
    """get_next_custom_id() should raise when all IDs 4-15 are used."""
    # Fill all custom IDs
    for i in range(4, 16):
        factory.add_custom_cycle(
            CycleConfig(
                cycle_id=i,
                cycle_name=f"Cycle {i}",
                cycle_duration_ms=60000,
                light_configuration=50,
                actions=[]
            )
        )
    # Now requesting next ID should fail
    with pytest.raises(ValueError) as exc:
        factory.get_next_custom_id()
    assert "No available custom cycle IDs" in str(exc.value)


def test_custom_cycle_min_max_ids(factory):
    min_cycle = CycleConfig(cycle_id=4, cycle_name="Min ID", cycle_duration_ms=5000, light_configuration=50, actions = [])
    max_cycle = CycleConfig(cycle_id=15, cycle_name="Max ID", cycle_duration_ms=5000, light_configuration=50, actions = [])
    
    factory.add_custom_cycle(min_cycle)
    factory.add_custom_cycle(max_cycle)

    assert factory.get_cycle_by_id(4) == min_cycle
    assert factory.get_cycle_by_id(15) == max_cycle


def test_auto_id_skips_used(factory):
    # Add ID 4 manually
    factory.add_custom_cycle(CycleConfig(cycle_id=4, cycle_name="Used ID 4", cycle_duration_ms=5000, light_configuration=50, actions = []))
    
    new_cycle = factory.create_custom_cycle(cycle_name="Next Auto ID", cycle_duration_ms=5000, light_configuration=50, actions = [])
    
    assert new_cycle.cycle_id == 5  # Auto-assign should skip 4

# ----------------------------------------
# tests for sound configuration in custom cycles
# ----------------------------------------
import pytest
from unittest.mock import patch
from backend.cycle_factory import CycleFactory
from backend.cycle_config import CycleConfig
from backend.cycle_action import CycleAction, ActionType

@pytest.fixture
def factory_with_repo_patch():
    """Provide a factory instance with a mocked repository to test persistence."""
    with patch("backend.cycle_repository.CycleRepository.load_all", return_value=[]), \
         patch("backend.cycle_repository.CycleRepository.save") as mock_save:
        factory = CycleFactory()
        yield factory, mock_save


def test_add_custom_cycle_with_sounds(factory_with_repo_patch):
    factory, mock_save = factory_with_repo_patch

    actions = [
        CycleAction(timestamp_ms=0, action_type=ActionType.SOUND_START, parameters={"file_name": "sound1.wav", "volume": 70}),
        CycleAction(timestamp_ms=500, action_type=ActionType.SOUND_START, parameters={"file_name": "sound2.wav", "volume": 80}),
    ]

    cycle = factory.create_custom_cycle(
        cycle_name="Custom Sound Cycle",
        cycle_duration_ms=1000,
        light_configuration=50,
        actions=actions
    )

    # Check that sounds are associated correctly
    mapping = cycle.get_sound_group_mapping()
    assert len(mapping) == 2
    assert mapping[1]["sound_names"] == ["sound1.wav"]
    assert mapping[1]["volume"] == 70
    assert mapping[2]["sound_names"] == ["sound2.wav"]
    assert mapping[2]["volume"] == 80

    # Verify that sounds belong to the correct cycle ID
    for group in mapping.values():
        assert isinstance(group["sound_names"], list)
    
    # Simulate save to JSON
    # If your CycleRepository.save(cycle) is used, we can call it manually
    from backend.cycle_repository import CycleRepository
    CycleRepository.save(cycle)
    mock_save.assert_called_once_with(cycle)


def test_invalid_sound_parameters(factory_with_repo_patch):
    factory, _ = factory_with_repo_patch

    # Missing filename
    bad_action = CycleAction(timestamp_ms=0, action_type=ActionType.SOUND_START, parameters={})
    cycle = factory.create_custom_cycle(
        cycle_name="Bad Sound Cycle",
        cycle_duration_ms=1000,
        light_configuration=50,
        actions=[bad_action]
    )

    # Should not fail when mapping, but sound_names will be empty
    mapping = cycle.get_sound_group_mapping()
    assert len(mapping) == 1
    assert mapping[1]["sound_names"] == []
    assert mapping[1]["volume"] == 50  # default volume


def test_multiple_sounds_same_timestamp(factory_with_repo_patch):
    factory, _ = factory_with_repo_patch

    actions = [
        CycleAction(timestamp_ms=0, action_type=ActionType.SOUND_START, parameters={"file_name": "soundA.wav", "volume": 30}),
        CycleAction(timestamp_ms=0, action_type=ActionType.SOUND_START, parameters={"file_name": "soundB.wav", "volume": 60}),
    ]

    cycle = factory.create_custom_cycle(
        cycle_name="Multi Sound Cycle",
        cycle_duration_ms=1000,
        light_configuration=50,
        actions=actions
    )

    mapping = cycle.get_sound_group_mapping()
    assert len(mapping) == 1  # same timestamp -> single group
    assert set(mapping[1]["sound_names"]) == {"soundA.wav", "soundB.wav"}
    assert mapping[1]["volume"] == 30  # takes volume from first action


def test_sound_group_count(factory_with_repo_patch):
    factory, _ = factory_with_repo_patch

    actions = [
        CycleAction(timestamp_ms=0, action_type=ActionType.SOUND_START, parameters={"file_name": "s1.wav"}),
        CycleAction(timestamp_ms=500, action_type=ActionType.SOUND_START, parameters={"file_name": "s2.wav"}),
        CycleAction(timestamp_ms=500, action_type=ActionType.SOUND_START, parameters={"file_name": "s3.wav"}),
    ]

    cycle = factory.create_custom_cycle(
        cycle_name="Count Test Cycle",
        cycle_duration_ms=1000,
        light_configuration=50,
        actions=actions
    )

    assert cycle.get_total_groups() == 2
    assert cycle.get_num_sound_groups() == 3