from typing import List
from backend.cycle_config import CycleConfig
from backend.cycle_repository import CycleRepository

class CycleFactory:
    """Provides MRI simulation cycle configurations loaded from JSON."""
    
    # Preset and custom cycle ID constraints
    PRESET_IDS = {1, 2, 3}
    CUSTOM_ID_MIN = 4
    CUSTOM_ID_MAX = 15

    def __init__(self):
        self._cycles: List[CycleConfig] = []
        self._load_cycles()

    def _load_cycles(self):
        """Load all cycles from repository."""
        self._cycles = CycleRepository.load_all()
        
        # Ensure existence of preset cycles
        preset_ids = {c.cycle_id for c in self._cycles if c.cycle_id in self.PRESET_IDS}
        missing_ids = self.PRESET_IDS - preset_ids
        if missing_ids:
            raise ValueError(f"Missing preset cycles with IDs: {missing_ids}")

    def get_cycle_by_id(self, cycle_id: int) -> CycleConfig:
        """
        Retrieve a cycle by ID.

        Raises:
            ValueError if not found
        """
        for cycle in self._cycles:
            if cycle.cycle_id == cycle_id:
                return cycle

        raise ValueError(f"No cycle with id {cycle_id}")

    def list_cycles(self) -> List[CycleConfig]:
        """Return all available cycles."""
        return list(self._cycles)

    def refresh(self):
        """Reload cycles from JSON (call after saving a new cycle)."""
        self._load_cycles()
    
    
    # ----------------------------------------
    # Custom cycle methods
    # ----------------------------------------
    def add_custom_cycle(self, cycle: CycleConfig):
        """Add a custom cycle ensuring ID is in valid range and not duplicate."""
        if not (self.CUSTOM_ID_MIN <= cycle.cycle_id <= self.CUSTOM_ID_MAX):
            raise ValueError(
                f"Custom cycle ID {cycle.cycle_id} must be between "
                f"{self.CUSTOM_ID_MIN}-{self.CUSTOM_ID_MAX}"
            )

        if any(c.cycle_id == cycle.cycle_id for c in self._cycles):
            raise ValueError(f"Cycle ID {cycle.cycle_id} already exists")

        self._cycles.append(cycle)
        self._cycles.sort(key=lambda c: c.cycle_id)
    
    
    def get_next_custom_id(self) -> int:
        """Return the next available custom ID in range 4–15."""
        used_ids = {c.cycle_id for c in self._cycles}
        for i in range(self.CUSTOM_ID_MIN, self.CUSTOM_ID_MAX + 1):
            if i not in used_ids:
                return i
        raise ValueError("No available custom cycle IDs")
    
    
    def create_custom_cycle(
        self,
        cycle_name: str,
        cycle_duration_ms: int,
        light_configuration: int,
        actions: list = None
    ) -> CycleConfig:
        """
        Convenience method to create and add a custom cycle with auto-assigned ID.
        """
        actions = actions or []
        next_id = self.get_next_custom_id()

        cycle = CycleConfig(
            cycle_id=next_id,
            cycle_name=cycle_name,
            cycle_duration_ms=cycle_duration_ms,
            light_configuration=light_configuration,
            actions=actions
        )

        self.add_custom_cycle(cycle)
        return cycle
