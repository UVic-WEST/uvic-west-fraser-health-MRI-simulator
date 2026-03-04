from PySide6.QtWidgets import(
    QLabel,
    QLayout,
    QWidget,
    QGridLayout
)
from PySide6.QtGui import(
    QPixmap
)
from PySide6.QtCore import (
    Qt
) 
from frontend.running_cycle_widgets.TimerWidget import TimerWidget

class CycleRunningPage(QWidget):
    def __init__(self, controller):
        #setup
        super().__init__()
        self.controller = controller
        self.is_running = False

        self.main_layout = QGridLayout()

        cycle_running_bg_path = 'resources/cycle_running_page_assets/running_cycle.png'
        cycle_running_bg_pix = QPixmap(cycle_running_bg_path)
        self.cycle_running_bg = QLabel()
        self.cycle_running_bg.setScaledContents(True)
        self.cycle_running_bg.setPixmap(cycle_running_bg_pix)
        self.cycle_running_bg.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.cycle_running_bg,0,0)

        self.timer = TimerWidget(self.cycle_running_bg)
        self.timer.move(300,180)
        #self.main_layout.addWidget(self.timer,0,0)

        self.setLayout(self.main_layout)
        self.timer.start_countdown(30)


    def change_running_status(self, cycle_running: bool):
        if self.is_running != cycle_running:
            self.is_running = cycle_running
        else: 
            #emmit signal that theres an issue
            return "ruh roh"