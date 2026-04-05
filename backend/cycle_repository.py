import json
from pathlib import Path
from typing import List
from backend.cycle_config import CycleConfig

CYCLE_FILE = Path("backend") / "cycles.json"


class CycleRepository:
    # ---------------------------------------------------------
    # LOAD ALL CYCLES
    # ---------------------------------------------------------
    @staticmethod
    def load_all() -> List[CycleConfig]:
        if not CYCLE_FILE.exists():
            return []

        try:
            with open(CYCLE_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return []

        return [CycleConfig.from_dict(item) for item in data]

    # ---------------------------------------------------------
    # SAVE ALL CYCLES (overwrite file)
    # ---------------------------------------------------------
    @staticmethod
    def save_all(cycles: List[CycleConfig]) -> None:
        # ensure folder exists
        CYCLE_FILE.parent.mkdir(parents=True, exist_ok=True)

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

    # ---------------------------------------------------------
    # ADD ONE CYCLE (helper)
    # ---------------------------------------------------------
    @staticmethod
    def add_cycle(cycle: CycleConfig) -> None:
        cycles = CycleRepository.load_all()
        cycles.append(cycle)
        CycleRepository.save_all(cycles)

    # ---------------------------------------------------------
    # DELETE ONE CYCLE BY ID
    # ---------------------------------------------------------
    @staticmethod
    def delete_cycle(cycle_id: int) -> bool:
        """Remove the cycle with ``cycle_id`` from storage. Returns True if one was removed."""
        cycles = CycleRepository.load_all()
        kept = [c for c in cycles if c.cycle_id != cycle_id]
        if len(kept) == len(cycles):
            return False
        CycleRepository.save_all(kept)
        return True