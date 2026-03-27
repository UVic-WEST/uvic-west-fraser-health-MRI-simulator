"""Factory for predefined MRI simulation cycle configurations.

Houses hardcoded cycle presets (e.g. Standard MRI, Fast MRI) that can be
retrieved by ID or index. New presets are added by creating private
_create_cycleN() methods and registering them in _load_cycles().
"""

from typing import List
from backend.cycle_config import CycleConfig
from backend.cycle_repository import CycleRepository


class CycleFactory:
    """Provides predefined MRI simulation cycle configurations.

    Cycles are built at init time and stored in a list and a dict
    for retrieval by index or by cycle_id respectively.
    """

    def __init__(self):
        self._cycles: List[CycleConfig] = []
        self._load_cycles()

    def _load_cycles(self):
        """Load all cycles from JSON via repository."""
        self._cycles = CycleRepository.load_all()
        
    def get_cycle_by_id(self, cycle_id: int) -> CycleConfig:
        """
        Retrieve a cycle configuration by its unique ID
        
        Raises:
            ValueError: If no cycle exists with the specified ID
        """
        
        for cycle in self._cycles:
            if cycle.cycle_id == cycle_id:
                return cycle
        raise ValueError(f"No cycle with id {cycle_id}")

    def list_cycles(self) -> List[CycleConfig]:
        return list(self._cycles)
    
    def refresh(self):
        self._load_cycles()