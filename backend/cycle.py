from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from backend.memory_adapter import MemoryAdapter


@dataclass
class Cycle:
    """
    Layer 3: Cycle object that stores cycle info and where its instructions live.
    Instruction reading is delegated to Layer 2 (MemoryAdapter) and is stubbed.
    """
    name: str
    duration_sec: float
    instructions_location: str  # path or ID

    def load_instructions(self, memory: Optional[MemoryAdapter] = None) -> str:
        adapter = memory or MemoryAdapter()
        return adapter.load_cycle_instructions(self.instructions_location)