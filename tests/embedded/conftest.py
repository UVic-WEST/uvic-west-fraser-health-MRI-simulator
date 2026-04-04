import pytest
from unittest.mock import patch
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
    return SoundConfig(file_name="test.wav", duration=5.0, volume=50)

@pytest.fixture
def sound_low_volume():
    return SoundConfig(file_name="test.wav", sound_id=1, duration=5.0, volume=10)

@pytest.fixture(autouse=True)
def mock_subprocess():
    """Prevents real amixer/aplay calls during tests."""
    with patch("embedded.sound_player.subprocess.run") as mock_run:
        yield mock_run