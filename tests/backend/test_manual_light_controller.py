"""Tests for ManualLightController (Layer 2 → Layer 3 light integration)."""

import pytest
from backend.manual_light_controller import ManualLightController, DEFAULT_BRIGHTNESS


class FakeLightController:
    def __init__(self):
        self.last_brightness = None
        self.idle_called = 0
        self.off_called = 0

    def system_idle(self):
        self.idle_called += 1

    def change_lights(self, brightness):
        self.last_brightness = brightness

    def system_off(self):
        self.off_called += 1


@pytest.fixture
def fake_lights():
    return FakeLightController()


@pytest.fixture
def controller(fake_lights):
    return ManualLightController(fake_lights)


# ========================
# Activation / Deactivation
# ========================

def test_initial_state(controller):
    assert not controller.is_active
    assert controller.brightness == DEFAULT_BRIGHTNESS

def test_activate_sets_active(controller):
    result = controller.set_manual_light_controller_status(True)
    assert result is True
    assert controller.is_active

def test_activate_turns_lights_on(controller, fake_lights):
    controller.set_manual_light_controller_status(True)
    assert fake_lights.last_brightness == DEFAULT_BRIGHTNESS / 100.0

def test_deactivate_resets_to_idle(controller, fake_lights):
    controller.set_manual_light_controller_status(True)
    controller.set_manual_light_controller_status(False)
    assert not controller.is_active
    assert fake_lights.idle_called >= 1

def test_deactivate_resets_brightness_to_default(controller):
    controller.set_manual_light_controller_status(True)
    controller.update_brightness(80)
    controller.set_manual_light_controller_status(False)
    assert controller.brightness == DEFAULT_BRIGHTNESS


# ========================
# Toggle Lights
# ========================

def test_toggle_off(controller, fake_lights):
    controller.set_manual_light_controller_status(True)
    result = controller.toggle_lights(False)
    assert result is True
    assert not controller.lights_on
    assert fake_lights.off_called >= 1

def test_toggle_on_after_off(controller, fake_lights):
    controller.set_manual_light_controller_status(True)
    controller.toggle_lights(False)
    controller.toggle_lights(True)
    assert controller.lights_on
    assert fake_lights.last_brightness == DEFAULT_BRIGHTNESS / 100.0

def test_toggle_fails_when_inactive(controller):
    result = controller.toggle_lights(True)
    assert result is False


# ========================
# Update Brightness
# ========================

def test_update_brightness_valid(controller, fake_lights):
    controller.set_manual_light_controller_status(True)
    result = controller.update_brightness(80)
    assert result is True
    assert controller.brightness == 80
    assert fake_lights.last_brightness == 0.8

def test_update_brightness_zero(controller, fake_lights):
    controller.set_manual_light_controller_status(True)
    result = controller.update_brightness(0)
    assert result is True
    assert controller.brightness == 0

def test_update_brightness_100(controller, fake_lights):
    controller.set_manual_light_controller_status(True)
    result = controller.update_brightness(100)
    assert result is True
    assert fake_lights.last_brightness == 1.0

def test_update_brightness_invalid_increment(controller):
    controller.set_manual_light_controller_status(True)
    result = controller.update_brightness(15)
    assert result is False

def test_update_brightness_out_of_range(controller):
    controller.set_manual_light_controller_status(True)
    assert controller.update_brightness(110) is False
    assert controller.update_brightness(-10) is False

def test_update_brightness_fails_when_inactive(controller):
    result = controller.update_brightness(50)
    assert result is False

def test_brightness_preserved_while_lights_off(controller, fake_lights):
    controller.set_manual_light_controller_status(True)
    controller.toggle_lights(False)
    off_called_before = fake_lights.off_called

    controller.update_brightness(90)
    assert controller.brightness == 90
    assert fake_lights.off_called == off_called_before

def test_brightness_applied_when_lights_toggled_back_on(controller, fake_lights):
    controller.set_manual_light_controller_status(True)
    controller.toggle_lights(False)
    controller.update_brightness(70)
    controller.toggle_lights(True)
    assert fake_lights.last_brightness == 0.7
