"""Tests for ManualSoundController (Layer 2 → Layer 3 sound integration)."""

import pytest
from unittest.mock import MagicMock, patch
from backend.manual_sound_controller import ManualSoundController


class FakeSoundPlayer:
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
def fake_sounds():
    return FakeSoundPlayer()


@pytest.fixture
def controller(fake_sounds):
    return ManualSoundController(fake_sounds)


# ========================
# get_sounds
# ========================

def test_get_sounds_returns_list(controller):
    sounds = controller.get_sounds()
    assert isinstance(sounds, list)

def test_get_sounds_sorted_by_id(controller):
    sounds = controller.get_sounds()
    if len(sounds) > 1:
        ids = [s[0] for s in sounds]
        assert ids == sorted(ids)

def test_get_sounds_tuples_have_id_and_name(controller):
    sounds = controller.get_sounds()
    for item in sounds:
        assert len(item) == 2
        assert isinstance(item[0], int)
        assert isinstance(item[1], str)


# ========================
# Activation / Deactivation
# ========================

def test_initial_state(controller):
    assert not controller.is_active

def test_activate(controller):
    result = controller.set_manual_sound_controller_status(True)
    assert result is True
    assert controller.is_active

def test_deactivate_stops_sounds(controller, fake_sounds):
    controller.set_manual_sound_controller_status(True)
    controller.set_manual_sound_controller_status(False)
    assert not controller.is_active
    assert fake_sounds.stop_called >= 1

def test_deactivate_clears_current_sounds(controller):
    controller.set_manual_sound_controller_status(True)
    controller.play_sounds([1], 50)
    controller.set_manual_sound_controller_status(False)
    assert controller.current_sounds == []


# ========================
# play_sounds
# ========================

def test_play_sounds_calls_player(controller, fake_sounds):
    controller.set_manual_sound_controller_status(True)
    sounds = controller.get_sounds()
    if sounds:
        result = controller.play_sounds([sounds[0][0]], 50)
        assert result is True
        assert len(fake_sounds.played) >= 1

def test_play_sounds_stops_previous_first(controller, fake_sounds):
    controller.set_manual_sound_controller_status(True)
    controller.play_sounds([], 50)
    assert fake_sounds.stop_called >= 1

def test_play_empty_list_succeeds(controller, fake_sounds):
    controller.set_manual_sound_controller_status(True)
    result = controller.play_sounds([], 50)
    assert result is True

def test_play_sounds_max_3(controller):
    controller.set_manual_sound_controller_status(True)
    result = controller.play_sounds([1, 2, 3], 50)
    assert result is True

def test_play_sounds_exceeds_max(controller):
    controller.set_manual_sound_controller_status(True)
    result = controller.play_sounds([1, 2, 3, 4], 50)
    assert result is False

def test_play_sounds_invalid_volume(controller):
    controller.set_manual_sound_controller_status(True)
    assert controller.play_sounds([1], 15) is False
    assert controller.play_sounds([1], -10) is False
    assert controller.play_sounds([1], 110) is False

def test_play_sounds_fails_when_inactive(controller):
    result = controller.play_sounds([1], 50)
    assert result is False

def test_play_sounds_stores_state(controller):
    controller.set_manual_sound_controller_status(True)
    controller.play_sounds([1, 2], 70)
    assert controller.current_sounds == [1, 2]
    assert controller.current_volume == 70

def test_play_sounds_sets_volume_on_config(controller, fake_sounds):
    controller.set_manual_sound_controller_status(True)
    sounds = controller.get_sounds()
    if sounds:
        controller.play_sounds([sounds[0][0]], 80)
        for played in fake_sounds.played:
            assert played.volume == 80
