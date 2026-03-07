from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import (
    QPixmap, 
    QFont
)
from frontend.confirmation_page_widgets.confirmation_buttons import ConfirmationButtons
from frontend.running_cycle_page_widgets.timer_widget import TimerWidget    

class CycleResumePage(QWidget):
    paused_pressed = Signal()
    stop_pressed = Signal()

    def __init__(self, controller, cycle, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent   
        self.cycle = cycle
        self.ispaused = True #This is because it is initally paused

        self.setFixedSize(1024,600)
        self.set_background("resources/cycle_running_page_assets/running_cycle.png")
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.main_layout)

        #setting up widgets

        #Cycle running label
        self.cycle_status = QLabel("RUNNING")
        cycle_status_font = QFont("Ubuntu", 24)
        self.cycle_status.setFont(cycle_status_font)
        self.cycle_status.setStyleSheet(
            "color: white; \nbackground-color: #0474BA;") 
        self.cycle_status.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.cycle_status)

        #adding the countdown. Timer sends a dummy cycle time of 30s REMOVE LATER
        self.countdown_timer = TimerWidget(self)
        self.main_layout.addWidget(self.countdown_timer)

        #setup for control buttons
        self.controlling_buttons = ConfirmationButtons()
        self.main_layout.addSpacing(40)
        self.main_layout.addWidget(self.controlling_buttons)
        


