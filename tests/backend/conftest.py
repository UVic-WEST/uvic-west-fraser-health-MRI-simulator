import pytest
from PyQt5.QtCore import QObject, pyqtSignal
from backend.cycle_logic import CycleLogic
from state import AppStateMachine

# -------------------------
# Fake lower-layer controller
# TODO: change this to match actual signatures once lower layer controller class is finalized
# -------------------------
class FakeController(QObject):
    started = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.start_called = False
        self.stop_called = False

    def start_cycle(self):
        self.start_called = True
    
    def stop_cycle(self):
        self.stop_called = True

# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
def fake_controller():
    return FakeController()

@pytest.fixture
def app_state():
    return AppStateMachine()

@pytest.fixture
def cycle_logic(app_state, fake_controller):
    logic = CycleLogic(app_state=app_state, controller=fake_controller)
    return logic