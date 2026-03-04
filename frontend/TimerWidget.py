from PySide6.QtWidgets import (
    QGridLayout,
    QWidget,
    QLabel,
    QPushButton
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
        self.rem_time_s = None

        timer_box_asset_path = 'timer_box.png'
        timer_box_asset_pix = QPixmap(timer_box_asset_path)
        self.timer_box = QLabel()
        self.timer_box.setPixmap(timer_box_asset_pix)
        self.timer_box.setScaledContents(True)
        self.timer_box.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.timer_box,0,0)

        self.timer_label = QLabel("00:00")
        self.timer_label.setStyleSheet(
            "color: black; \n font-size: 36px;") 
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.timer_label,0,0)

        self.dumbutton = QPushButton("start")
        self.dumbutton.clicked.connect(self.start_countdown)
        self.main_layout.addWidget(self.dumbutton)

        self.setLayout(self.main_layout)

    def get_time(self, time_ms) -> str:
        minutes = time_ms // 60
        seconds = time_ms - (minutes*60)
        return f"{minutes:02}:{seconds:02}"

    def start_countdown(self):
        time = 10
        self.rem_time_s = time
        self.timer_label.setText(self.get_time(self.rem_time_s))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

        self.timer.start(1000) 
        #1000 gives it an offset of 1s before starting.

    def update_countdown(self):
        if self.rem_time_s > 0:
            self.rem_time_s -= 1
            self.timer_label.setText(self.get_time(self.rem_time_s))
        else:
            self.timer.stop()
            self.cycle_completed()

    def cycle_completed(self):
        pass
        #emit that cycle is done


