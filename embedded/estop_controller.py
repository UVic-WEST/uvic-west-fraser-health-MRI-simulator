from PySide6.QtCore import (
    Signal,
)
from PySide6.QtWidgets import QWidget
from embedded.temp_estop import TempEstop
import platform

class EStopController(QWidget):

    estop_active = Signal(bool)

    def __init__(self, parent=None):
        """
        Monitors the physical E-Stop button on GPIO21. Emits estop_active(True)
        when pressed and estop_active(False) when released.
        """
        super().__init__(parent)
        self.temp_button = TempEstop(self)
        
        if platform.system() == "Linux": # Raspberry pi 
            print("Running on Raspberry Pi")
            try:
                from gpiozero import Button
                self.estop = Button(21)
                self.estop.when_pressed = lambda: self.estop_pressed(True)
                self.estop.when_released = lambda: self.estop_released(False)
            except Exception as e:
                print("Failed to configure GPIO. Error: ", e)

        else: # Skip GPIO configuration
            pass

    def estop_event(self, active):
        self.estop_active.emit(active)