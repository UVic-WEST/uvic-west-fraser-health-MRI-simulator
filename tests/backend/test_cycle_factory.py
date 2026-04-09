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
    duplicate_cycles = [
        CycleConfig(cycle_id=1, cycle_name="Cycle 1", cycle_duration_ms=100, light_configuration=50, actions=[]),
        CycleConfig(cycle_id=1, cycle_name="Cycle 2", cycle_duration_ms=100, light_configuration=50, actions=[]),
        CycleConfig(cycle_id=2, cycle_name="Cycle 2", cycle_duration_ms=100, light_configuration=50, actions=[]),
        CycleConfig(cycle_id=3, cycle_name="Cycle 3", cycle_duration_ms=100, light_configuration=50, actions=[])
    ]
    
    with patch("backend.cycle_repository.CycleRepository.load_all", return_value=duplicate_cycles):
        factory = CycleFactory()
        result = factory.get_cycle_by_id(1)
        assert result.cycle_name == "Cycle 1"
        
        
def test_refresh():
    """refresh() should reload cycles and all relevant data from cycle repository."""
    initial_cycles = [
        CycleConfig(cycle_id=1, cycle_name="Initial", cycle_duration_ms=100, light_configuration=50, actions=[]),
        CycleConfig(cycle_id=2, cycle_name="Cycle 2", cycle_duration_ms=100, light_configuration=50, actions=[]),
        CycleConfig(cycle_id=3, cycle_name="Cycle 3", cycle_duration_ms=100, light_configuration=50, actions=[])
    ]
    updated_cycles = [
        CycleConfig(cycle_id=2, cycle_name="Updated", cycle_duration_ms=200, light_configuration=50, actions=[]),
        CycleConfig(cycle_id=1, cycle_name="Cycle 1", cycle_duration_ms=100, light_configuration=50, actions=[]),
        CycleConfig(cycle_id=3, cycle_name="Cycle 3", cycle_duration_ms=100, light_configuration=50, actions=[])
    ]
    
    with patch("backend.cycle_repository.CycleRepository.load_all", side_effect=[initial_cycles, updated_cycles]):
        factory = CycleFactory()
        
        # test initial state
        assert factory.get_cycle_by_id(1).cycle_name == "Initial"
        
        # call refresh() to reload cycles
        factory.refresh()
        
        # test updated state - cycle 1 still exists, cycle 2 is updated
        assert factory.get_cycle_by_id(1).cycle_name == "Cycle 1"
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
