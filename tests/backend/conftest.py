import pytest
from PySide6.QtCore import QObject, Signal
from backend.cycle_logic import CycleLogic
from backend.auth import Auth
from state import AppStateMachine

# -------------------------
# Fake lower-layer controller
# TODO: change this to match actual signatures once lower layer controller class is finalized
# -------------------------
class FakeController(QObject):
    started = Signal()
    failed = Signal()

    def __init__(self):
        super().__init__()
        self.start_called = False
        self.stop_called = False

    def start_cycle(self):
        self.start_called = True
        self.stop_called = False

    def stop_cycle(self):
        self.stop_called = True
        self.start_called = False

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

@pytest.fixture
def auth():
    auth = Auth(correct_pin='1234')
    return auth