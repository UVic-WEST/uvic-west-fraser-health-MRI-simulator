from PySide6.QtWidgets import(
    QWidget,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap, 
    QFont
)
from frontend.running_cycle_page_widgets.ControllingButtons import ControllingButtons
from frontend.running_cycle_page_widgets.TimerWidget import TimerWidget

class CycleRunningPage(QWidget):
    def __init__(self,controller,cycle,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.cycle = None
        self.setFixedSize(1024,600)

        # Create main layout
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
        self.controlling_buttons = ControllingButtons()
        self.main_layout.addSpacing(40)
        self.main_layout.addWidget(self.controlling_buttons)

        self.controlling_buttons.stop_button.clicked.connect(self.cycle_completed)
        
    def play_cycle(self, cycle_dur_s:int):
        self.countdown_timer.start_countdown(cycle_dur_s)

    def set_background(self, image_path):
        
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(image_path).scaled(
            self.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        ))
        self.bg_label.setGeometry(0, 1, self.width(), self.height())
        self.bg_label.lower()  # send to back

    def cycle_completed(self):
        self.countdown_timer.stop_timer()
        self.parent.show_home()
        
    def update_cycle(self,cycle):
        self.curr_cycle = cycle
        #placeholder
        print(f'current cycle: cycle["minutes"],cycle["seconds"]')