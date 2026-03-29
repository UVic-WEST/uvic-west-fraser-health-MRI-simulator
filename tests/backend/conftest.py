import pytest
from backend.auth import Auth
from backend.cycle_running_page_logic import CycleRunningPageLogic
from backend.cycle_config import CycleConfig
from embedded.sound_player import SoundPlayer
from embedded.light_controller import LightController
from PySide6.QtCore import Signal

# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
def mock_sound_player(mocker):
    mock = mocker.Mock(spec=SoundPlayer)
    mock.play.return_value = True, "Playing mock sound"
    return mock

@pytest.fixture
def mock_light_controller(mocker):
    return mocker.Mock(spec=LightController)

@pytest.fixture
def mock_cycle_factory(mocker):
    """Sets up the cycle factory mock for testing test_cycle_running_page_logic"""
    mock = mocker.patch('backend.cycle_running_page_logic.CycleRunningPageLogic.cycle_factory')
    mock.get_cycle_by_id.return_value = CycleConfig(1, "test cycle", 3000, 70, [])
    return mock

@pytest.fixture
def cycle_running_logic(mocker, mock_sound_player, mock_light_controller, mock_cycle_factory):
    """Instantiates the CycleRunningPageLogic object for each test. Injects mocks automatically."""
    mocker.patch('backend.cycle_running_page_logic.QTimer')
    
    logic = CycleRunningPageLogic(
        sound_player=mock_sound_player, 
        light_controller=mock_light_controller
    )
    
    logic.timer.isActive.return_value = False
    
    def mock_start():
        logic.timer.isActive.return_value = True

    def mock_stop():
        logic.timer.isActive.return_value = False
        
    logic.timer.start.side_effect = mock_start
    logic.timer.stop.side_effect = mock_stop
    
    return logic

@pytest.fixture
def auth():
    auth = Auth(correct_pin='1234', parent=None)
    return auth