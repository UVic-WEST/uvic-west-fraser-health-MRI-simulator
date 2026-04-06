from unittest.mock import MagicMock, patch

import pytest

from backend.cycle_factory import CycleFactory
from backend.cycle_repository import CycleRepository
from backend.home_page_logic import HomePageLogic


def test_cycle_factory_getter_uses_injected_instance():
    factory = CycleFactory()
    logic = HomePageLogic(cycle_factory=factory)
    assert logic.cycle_factory is factory


def test_cycle_factory_setter_replaces_instance():
    logic = HomePageLogic()
    other = CycleFactory()
    logic.cycle_factory = other
    assert logic.cycle_factory is other


def test_cycle_factory_setter_rejects_none():
    logic = HomePageLogic()
    with pytest.raises(ValueError, match="cannot be None"):
        logic.cycle_factory = None  # type: ignore[assignment]


def test_delete_cycle_calls_repository_and_refreshes_when_removed():
    factory = MagicMock(spec=CycleFactory)
    logic = HomePageLogic(cycle_factory=factory)
    with patch.object(CycleRepository, "delete_cycle", return_value=True) as del_mock:
        assert logic.delete_cycle(3) is True
        del_mock.assert_called_once_with(3)
        factory.refresh.assert_called_once()


def test_delete_cycle_no_refresh_when_missing():
    factory = MagicMock(spec=CycleFactory)
    logic = HomePageLogic(cycle_factory=factory)
    with patch.object(CycleRepository, "delete_cycle", return_value=False):
        assert logic.delete_cycle(999) is False
        factory.refresh.assert_not_called()
