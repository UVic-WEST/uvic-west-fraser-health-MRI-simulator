import pytest
from unittest.mock import patch, MagicMock
from embedded.sound_player import SoundPlayer
from backend.sound_config import SoundConfig

# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
def sound_player():
    return SoundPlayer()

@pytest.fixture
def sound_mid_volume():
    return SoundConfig(sound_id=1, file_name="test.wav", duration=5.0, volume=50)

@pytest.fixture
def sound_low_volume():
    return SoundConfig(sound_id=2, file_name="test.wav", duration=5.0, volume=10)

@pytest.fixture(autouse=True)
def mock_pygame(monkeypatch):
    """Prevents real pygame audio calls during tests."""
    mock_sound = MagicMock()
    mock_channel = MagicMock()
    mock_channel.get_busy.return_value = True

    monkeypatch.setattr("pygame.mixer.Sound", lambda f: mock_sound)
    monkeypatch.setattr("pygame.mixer.find_channel", lambda: mock_channel)
    monkeypatch.setattr("pygame.mixer.stop", MagicMock())
    monkeypatch.setattr("pygame.mixer.get_busy", MagicMock(return_value=True))
    monkeypatch.setattr("pygame.mixer.get_num_channels", MagicMock(return_value=3))
    monkeypatch.setattr("pygame.mixer.Channel", MagicMock(return_value=mock_channel))

    return mock_channel