from PySide6.QtWidgets import (
    QGridLayout,
    QWidget,
    QLabel,
    QPushButton
)
from PySide6.QtGui import(
    QPixmap,
    QFont,
    QFontDatabase
)
from PySide6.QtCore import (
    QTimer,
    Qt
)
        
class TimerWidget(QWidget):
    def __init__(self):
        '''
        Timer widget for the cycle running page.
        Call .start_countdown(time_s)
        '''
        #write text that gets changed, Qtimer is hardware
        super().__init__()
        self.setFixedSize(395,141)
        self.main_layout = QGridLayout()
        self.rem_time_s = 10

        #create the bg of the widget
        timer_box_asset_path = 'resources/running_page_assets/timer_box.png'

        timer_box_asset_pix = QPixmap(timer_box_asset_path)
        self.timer_box = QLabel()
        self.timer_box.setPixmap(timer_box_asset_pix)
        self.timer_box.setScaledContents(True)
        self.timer_box.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.timer_box,0,0)

        font_family = None
        font_id = QFontDatabase.addApplicationFont("resources/cycle_running_page_assets/DigitalNumbers.ttf")

        if font_id == -1:
            print("Font failed to load")
        else:
            # Get the actual font family name
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]


        #create label that actually displays the time on the widget. this gets updated by update_countdown
        countdown_font = QFont(font_family, 65)
        self.timer_label = QLabel("00:00", self.timer_box)
        self.timer_label.setFont(countdown_font)
        self.timer_label.setStyleSheet(
            "color: #34C759; \n font-size: 36px;") 
        self.timer_label.move(115,13) #manual placement

        self.setLayout(self.main_layout)

    def start_countdown (self, time_s):
        '''
        call this to set and start the timer (in seconds)
        '''
        self.rem_time_s = time_s
        self.start()
    
    def get_time(self, time_s) -> str:
        '''
        returns the time as a string for countdown label
        '''
        minutes = time_s // 60
        seconds = time_s - (minutes*60)
        return f"{minutes:02}:{seconds:02}"

    def start(self):
        '''
        starts actually running the timer based of the value of rem_time_s
        '''
        self.timer_label.setText(self.get_time(self.rem_time_s))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

        self.timer.start(1000) 
        #1000 gives it an offset of 1s before starting.

    def update_countdown(self):
        '''
        this function updates the timer label to display the remaining time left on the cycle on screen
        '''
        if self.rem_time_s > 0:
            self.rem_time_s -= 1
            self.timer_label.setText(self.get_time(self.rem_time_s))
        else:
            self.timer.stop()
            self.cycle_completed()

    def cycle_completed(self):
        pass
        #emit that cycle is done


