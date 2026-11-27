from PySide6.QtCore import (
    Signal,
)
from PySide6.QtWidgets import QWidget
import platform

class EStopController(QWidget):

    estop_active = Signal(bool)

    def __init__(self, parent=None):
        """
        Monitors the physical E-Stop button on GPIO21. Emits estop_active(True)
        when pressed and estop_active(False) when released.
        """
        super().__init__(parent)
        
        if platform.system() == "Linux": # Raspberry pi 
            print("Running on Raspberry Pi")
            try:
                from gpiozero import Button
                self.estop = Button(21)
                self.estop.when_pressed = lambda: self.estop_event(True)
                self.estop.when_released = lambda: self.estop_event(False)
            except Exception as e:
                print("Failed to configure GPIO. Error: ", e)

        else:
            print("Not running on Raspberry Pi: physical E-Stop (GPIO21) unavailable")

    def estop_event(self, active):
        self.estop_active.emit(active)