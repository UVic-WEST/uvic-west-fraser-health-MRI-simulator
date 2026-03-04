# backend/CycleFactory.py
from __future__ import annotations

from typing import Optional, Any

from backend.memory_adapter import MemoryAdapter, CycleRecord


class CycleFactory:
    """
    Layer 3: loads cycles for the UI to select.

    It reads raw records via a Layer 2 MemoryAdapter (stubbed for now),
    then converts them into Cycle objects/configs later.
    """

    def __init__(self, memory: Optional[MemoryAdapter] = None) -> None:
        self._memory = memory or MemoryAdapter()

    def get_available_cycles(self) -> list[str]:
        """
        Returns a list of cycle names for the Home screen selection UI.

        Layer 2 communication: MemoryAdapter.load_cycle_records() (stubbed).
        """
        records = self._memory.load_cycle_records()
        return [r.cycle_name for r in records]

    def load_cycles(self) -> list[Any]:
        """
        Returns 'cycle classes' / objects.

        For now this is stubbed and returns raw CycleRecord objects.
        Later, you can convert CycleRecord -> CycleConfig/Cycle instance.
        """
        records = self._memory.load_cycle_records()
        # STUB: returning raw records until CycleConfig is finalized
        return records

    def refresh(self) -> None:
        """
        Hook for UI to force reload later.
        Stubbed for now.
        """
        # STUB: In future could clear caches, re-read disk, etc.
        return
    