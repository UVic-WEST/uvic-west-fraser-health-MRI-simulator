"""Tests that CycleRunningPageLogic correctly calls CycleController
on start, pause, resume, and stop — verifying Layer 2 → Layer 3 integration."""

import pytest
from unittest.mock import MagicMock
from backend.cycle_running_page_logic import CycleRunningPageLogic


@pytest.fixture
def mock_controller():
    ctrl = MagicMock()
    return ctrl


@pytest.fixture
def logic(mock_controller):
    return CycleRunningPageLogic(cycle_controller=mock_controller)


# ========================
# Start
# ========================

def test_start_calls_controller_start(logic, mock_controller):
    logic.start_cycle(1, 30)
    mock_controller.start_cycle.assert_called_once()


def test_start_emits_time_signal(logic, qtbot):
    with qtbot.waitSignal(logic.time_signal_in_s, timeout=500):
        logic.start_cycle(1, 30)


# ========================
# Pause
# ========================

def test_pause_calls_controller_stop(logic, mock_controller):
    logic.start_cycle(1, 30)
    logic.pause_cycle()
    mock_controller.stop_cycle.assert_called_once()


def test_pause_emits_negative_signal(logic, qtbot):
    logic.start_cycle(1, 30)
    signals = []
    logic.time_signal_in_s.connect(signals.append)
    logic.pause_cycle()
    assert -1 in signals


# ========================
# Resume
# ========================

def test_resume_calls_controller_start(logic, mock_controller):
    logic.start_cycle(1, 30)
    logic.pause_cycle()
    mock_controller.reset_mock()

    logic.resume_cycle()
    mock_controller.start_cycle.assert_called_once()


def test_resume_does_nothing_when_no_time_left(mock_controller):
    logic = CycleRunningPageLogic(cycle_controller=mock_controller)
    logic.resume_cycle()
    mock_controller.start_cycle.assert_not_called()


# ========================
# Stop
# ========================

def test_stop_calls_controller_stop(logic, mock_controller):
    logic.start_cycle(1, 30)
    mock_controller.reset_mock()

    logic.stop_cycle()
    mock_controller.stop_cycle.assert_called_once()


def test_stop_clears_timer(logic):
    logic.start_cycle(1, 30)
    logic.stop_cycle()
    assert logic.timer is None
    assert logic.rem_time_ms is None


# ========================
# Timer completion triggers stop
# ========================

def test_timer_completion_stops_hardware(mock_controller, qtbot):
    logic = CycleRunningPageLogic(cycle_controller=mock_controller)
    logic.start_cycle(1, 1)
    with qtbot.waitSignal(logic.time_signal_in_s, timeout=3000,
                          check_params_cb=lambda val: val == 0):
        pass
    mock_controller.stop_cycle.assert_called()


# ========================
# Without controller (backward compat)
# ========================

def test_works_without_controller():
    logic = CycleRunningPageLogic()
    logic.start_cycle(1, 10)
    logic.pause_cycle()
    logic.resume_cycle()
    logic.stop_cycle()
