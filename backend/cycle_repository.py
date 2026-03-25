import json
from pathlib import Path
from typing import List
from backend.cycle_config import CycleConfig

CYCLE_FILE = Path("data/cycles.json")


class CycleRepository:
    """Handles all persistence for CycleConfig objects."""

    # ---------------------------------------------------------
    # LOAD ALL CYCLES
    # ---------------------------------------------------------
    @staticmethod
    def load_all() -> List[CycleConfig]:
        if not CYCLE_FILE.exists():
            return []

        with open(CYCLE_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []

        return [CycleConfig.from_dict(item) for item in data]

    # ---------------------------------------------------------
    # SAVE ALL CYCLES (overwrite file)
    # ---------------------------------------------------------
    @staticmethod
    def save_all(cycles: List[CycleConfig]) -> None:
        with open(CYCLE_FILE, "w") as f:
            json.dump([c.to_dict() for c in cycles], f, indent=2)

    # ---------------------------------------------------------
    # GET NEXT AVAILABLE ID
    # ---------------------------------------------------------
    @staticmethod
    def get_next_id() -> int:
        cycles = CycleRepository.load_all()

        if not cycles:
            return 1

        return max(c.cycle_id for c in cycles) + 1