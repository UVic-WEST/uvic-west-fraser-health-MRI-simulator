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

class CycleRunningPage(QWidget):
    def __init__(self, controller):
        #setup
        super().__init__()
        self.controller = controller
        self.is_running = False

        self.main_layout = QGridLayout()

        cycle_running_bg_path = 'resources/cycle_running_page_assets/running_cycle.png'
        cycle_running_bg_pix = QPixmap(cycle_running_bg_path)
        cycle_running_bg = QLabel()
        cycle_running_bg.setScaledContents(True)
        cycle_running_bg.setPixmap(cycle_running_bg_pix)
        cycle_running_bg.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(cycle_running_bg)
        self.setLayout(self.main_layout)

    def change_running_status(self, cycle_running: bool):
        if self.is_running != cycle_running:
            self.is_running = cycle_running
        else: 
            #emmit signal that theres an issue
            return "ruh roh"