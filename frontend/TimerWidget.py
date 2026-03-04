import sys
from PySide6.QtWidgets import (
    QGridLayout,
    QMainWindow,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
    QApplication
)
from PySide6.QtGui import(
    QPixmap
)
from PySide6.QtCore import (
    QTimer,
    Qt
)
        
class TimerWidget(QWidget):
    def __init__(self):
        #write text that gets changed, Qtimer is hardware
        super().__init__()
        self.setFixedSize(403,149)
        self.main_layout = QGridLayout()
        self.total_time_ms = None
        self.cur_time_ms = None

        timer_box_asset_path = 'timer_box.png'
        timer_box_asset_pix = QPixmap(timer_box_asset_path)
        self.timer_box = QLabel()
        self.timer_box.setPixmap(timer_box_asset_pix)
        self.timer_box.setScaledContents(True)
        self.timer_box.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.timer_box)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.main_layout.addWidget(self.timer)

        self.setLayout(self.main_layout)

    def start_countdown(self, time_ms:int):
        self.timer.start(time_ms)

    def update_countdown(self):
        if self.cur_time_ms > 0:
            self.cur_time_ms -= 1
            # Update GUI label with new time
        else:
            self.timer.stop()


