# backend/memory_adapter.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CycleRecord:
    """Raw cycle data loaded from 'memory' (file system, DB, etc.)."""
    cycle_name: str
    cycle_duration: float
    payload: dict[str, Any] | None = None


class MemoryAdapter:
    """
    Layer 2 stub: eventually reads from Raspberry Pi storage / resources.
    For now, provides stub methods that are easy to test.
    """

    def __init__(self) -> None:
        self.last_call: tuple[str, tuple, dict] | None = None

    def load_cycle_records(self) -> list[CycleRecord]:
        """
        STUB: Pretend to load cycle definitions from disk/memory.
        """
        self.last_call = ("load_cycle_records", (), {})
        # Return empty list for now (or add a dummy record if your UI needs it)
        return []
    
    def load_cycle_instructions(self, location: str) -> str:
        """
        STUB: Pretend to read cycle instructions from disk/memory.
        """
        self.last_call = ("load_cycle_instructions", (location,), {})
        return ""