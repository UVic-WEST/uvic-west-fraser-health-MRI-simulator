"""Tests that CycleController correctly delegates to Layer 3 hardware
(LightController, SoundPlayer) during cycle start, stop, and action dispatch."""

import pytest
from unittest.mock import MagicMock, patch
from backend.cycle_controller import CycleController
from backend.cycle_action import CycleAction, ActionType


# ========================
# Fixtures
# ========================

class FakeLightController:
    """Lightweight stand-in for embedded.light_controller.LightController."""

    def __init__(self):
        self.idle_called = 0
        self.last_brightness = None
        self.off_called = 0

    def system_idle(self):
        self.idle_called += 1

    def change_lights(self, brightness):
        self.last_brightness = brightness

    def system_off(self):
        self.off_called += 1


class FakeSoundPlayer:
    """Lightweight stand-in for embedded.sound_player.SoundPlayer."""

    def __init__(self):
        self.played = []
        self.stop_called = 0

    def play(self, sound):
        self.played.append(sound)
        return f"Playing {sound.file_name}"

    def stop(self):
        self.stop_called += 1
        return "Stopped"


@pytest.fixture
def fake_lights():
    return FakeLightController()


@pytest.fixture
def fake_sounds():
    return FakeSoundPlayer()


@pytest.fixture
def controller(fake_lights, fake_sounds):
    return CycleController(fake_lights, fake_sounds)


# ========================
# Start Cycle
# ========================

def test_start_cycle_calls_light_idle(controller, fake_lights):
    controller.start_cycle()
    assert fake_lights.idle_called >= 1


def test_start_cycle_emits_started(controller, qtbot):
    with qtbot.waitSignal(controller.started, timeout=500):
        controller.start_cycle()


def test_start_cycle_sets_running_flag(controller):
    controller.start_cycle()
    assert controller._running is True


# ========================
# Stop Cycle
# ========================

def test_stop_cycle_stops_sound(controller, fake_sounds):
    controller.start_cycle()
    controller.stop_cycle()
    assert fake_sounds.stop_called >= 1


def test_stop_cycle_resets_lights(controller, fake_lights):
    controller.start_cycle()
    idle_before = fake_lights.idle_called
    controller.stop_cycle()
    assert fake_lights.idle_called > idle_before


def test_stop_cycle_clears_running_flag(controller):
    controller.start_cycle()
    controller.stop_cycle()
    assert controller._running is False


# ========================
# Dispatch Actions
# ========================

def test_dispatch_light_on(controller, fake_lights):
    controller.start_cycle()
    action = CycleAction(
        timestamp_ms=100,
        action_type=ActionType.LIGHT_ON,
        parameters={"brightness": 0.8},
    )
    controller.dispatch_action(action)
    assert fake_lights.last_brightness == 0.8


def test_dispatch_light_off(controller, fake_lights):
    controller.start_cycle()
    action = CycleAction(
        timestamp_ms=200,
        action_type=ActionType.LIGHT_OFF,
        parameters={},
    )
    controller.dispatch_action(action)
    assert fake_lights.idle_called >= 2  # once from start, once from light_off


def test_dispatch_sound_start(controller, fake_sounds):
    controller.start_cycle()
    action = CycleAction(
        timestamp_ms=100,
        action_type=ActionType.SOUND_START,
        parameters={"file_name": "mri_gradient.wav", "duration": 5.0, "volume": 70},
    )
    controller.dispatch_action(action)
    assert len(fake_sounds.played) == 1
    assert fake_sounds.played[0].file_name == "mri_gradient.wav"
    assert fake_sounds.played[0].volume == 70


def test_dispatch_sound_stop(controller, fake_sounds):
    controller.start_cycle()
    action = CycleAction(
        timestamp_ms=500,
        action_type=ActionType.SOUND_STOP,
        parameters={},
    )
    controller.dispatch_action(action)
    assert fake_sounds.stop_called >= 1


def test_dispatch_ignored_when_not_running(controller, fake_lights):
    action = CycleAction(
        timestamp_ms=100,
        action_type=ActionType.LIGHT_ON,
        parameters={"brightness": 0.5},
    )
    controller.dispatch_action(action)
    assert fake_lights.last_brightness is None


def test_dispatch_after_stop_ignored(controller, fake_sounds):
    controller.start_cycle()
    controller.stop_cycle()
    stop_count = fake_sounds.stop_called

    action = CycleAction(
        timestamp_ms=100,
        action_type=ActionType.SOUND_START,
        parameters={"file_name": "test.wav", "duration": 1.0, "volume": 50},
    )
    controller.dispatch_action(action)
    assert len(fake_sounds.played) == 0
