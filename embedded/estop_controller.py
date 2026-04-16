from PySide6.QtCore import (
    Signal,
)
from PySide6.QtWidgets import QWidget
from embedded.temp_estop import TempEstop

class EStopController(QWidget):

    estop_active = Signal(bool)

    def __init__(self, parent=None):
        """
        When estop is hit it sends a signal to the frontend to close all functions
        UPDATE THIS
        """
        super().__init__(parent)
        self.temp_button = TempEstop(self)

    def estop_event(self, active):
        self.estop_active.emit(active)
        






