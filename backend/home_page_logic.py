"""Backend logic for the home page."""

from __future__ import annotations

from typing import Optional

from backend.cycle_factory import CycleFactory
from backend.cycle_repository import CycleRepository


class HomePageLogic:
    """Home page controller: cycle list access via ``CycleFactory`` and deletion via ``CycleRepository``."""

    def __init__(self, cycle_factory: Optional[CycleFactory] = None):
        self._cycle_factory: CycleFactory = cycle_factory or CycleFactory()

    @property
    def cycle_factory(self) -> CycleFactory:
        """Shared ``CycleFactory`` used to resolve cycles for the home page."""
        return self._cycle_factory

    @cycle_factory.setter
    def cycle_factory(self, factory: CycleFactory) -> None:
        if factory is None:
            raise ValueError("cycle_factory cannot be None")
        self._cycle_factory = factory

    def delete_cycle(self, cycle_id: int) -> bool:
        """Persist removal of ``cycle_id`` and refresh the in-memory factory cache.

        Returns:
            True if a cycle was removed, False if ``cycle_id`` was not found.
        """
        removed = CycleRepository.delete_cycle(cycle_id)
        if removed:
            self._cycle_factory.refresh()
        return removed
