from unittest.mock import patch

from backend.cycle_config import CycleConfig
from backend.cycle_repository import CycleRepository


def test_delete_cycle_removes_and_returns_true():
    cycles = [
        CycleConfig(1, "A", 1000, 50, actions=[]),
        CycleConfig(2, "B", 2000, 50, actions=[]),
    ]
    with patch.object(CycleRepository, "load_all", return_value=cycles):
        with patch.object(CycleRepository, "save_all") as save_mock:
            assert CycleRepository.delete_cycle(1) is True
            save_mock.assert_called_once()
            saved = save_mock.call_args[0][0]
            assert len(saved) == 1
            assert saved[0].cycle_id == 2


def test_delete_cycle_missing_returns_false():
    cycles = [CycleConfig(1, "A", 1000, 50, actions=[])]
    with patch.object(CycleRepository, "load_all", return_value=cycles):
        with patch.object(CycleRepository, "save_all") as save_mock:
            assert CycleRepository.delete_cycle(99) is False
            save_mock.assert_not_called()
