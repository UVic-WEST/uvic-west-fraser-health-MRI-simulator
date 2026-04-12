import pytest
import sys
from unittest.mock import MagicMock, patch

sys.modules["pygame"] = MagicMock()
sys.modules["pygame.mixer"] = MagicMock()

from backend.auth import Auth
from backend.cycle_running_page_logic import CycleRunningPageLogic
from backend.cycle_config import CycleConfig
from embedded.sound_player import SoundPlayer
from embedded.light_controller import LightController

# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
def mock_sound_player():
    mock = MagicMock(spec=SoundPlayer)
    mock.play.return_value = True, "Playing mock sound"
    return mock


@pytest.fixture
def mock_light_controller():
    return MagicMock(spec=LightController)


@pytest.fixture
def mock_cycle_factory():
    """Mock ``CycleFactory`` injected into ``CycleRunningPageLogic``."""
    mock = MagicMock()
    mock.get_cycle_by_id.return_value = CycleConfig(1, "test cycle", 3000, 70, actions=[])
    return mock


@pytest.fixture
def cycle_running_logic(mock_sound_player, mock_light_controller, mock_cycle_factory):
    """Instantiates CycleRunningPageLogic with mocks; QTimer is patched."""
    with patch("backend.cycle_running_page_logic.QTimer"):
        logic = CycleRunningPageLogic(
            sound_player=mock_sound_player,
            light_controller=mock_light_controller,
            cycle_factory=mock_cycle_factory,
        )

        logic.timer.isActive.return_value = False

        def mock_start():
            logic.timer.isActive.return_value = True

        def mock_stop():
            logic.timer.isActive.return_value = False

        logic.timer.start.side_effect = mock_start
        logic.timer.stop.side_effect = mock_stop

        yield logic


@pytest.fixture
def auth():
    auth = Auth(correct_pin="1234", parent=None)
    return auth
