from typing import List
from backend.cycle_config import CycleConfig
from backend.cycle_repository import CycleRepository


class CycleFactory:
    """Provides MRI simulation cycle configurations loaded from JSON."""

    def __init__(self):
        self._cycles: List[CycleConfig] = []
        self._load_cycles()

    def _load_cycles(self):
        """Load all cycles from repository."""
        self._cycles = CycleRepository.load_all()

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
