from PySide6.QtWidgets import (
    QGridLayout,
    QWidget,
    QLabel,
)
from PySide6.QtGui import(
    QPixmap,
    QFont,
    QFontDatabase
)
from PySide6.QtCore import (
    Qt
)
        
class TimerWidget(QWidget):
    def __init__(self, parent=None):
        '''
        Timer widget for the cycle running page.
        Call .start_countdown(time_s)
        '''
        #write text that gets changed, Qtimer is hardware
        super().__init__(parent)
        self.timer_controller = None
        self.setFixedSize(395,141)
        self.setStyleSheet("background-color: #0474BA;")
        self.main_layout = QGridLayout()
        self.parent = parent

        #create the bg of the widget
        timer_box_asset_path = 'resources/cycle_running_page_assets/timer_box.png'

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
            "color: #34C759; \n font-size: 36px; \nbackground-color: white;") 
        self.timer_label.move(115,13) #manual placement

        self.setLayout(self.main_layout)

    def cycle_not_running(self):
        self.parent.cycle_completed()

    def get_time(self, time_s) -> str:
        '''
        returns the time as a string for countdown label
        '''
        minutes = time_s // 60
        seconds = time_s - (minutes*60)
        return f"{minutes:02}:{seconds:02}"

    def connect_to_backend(self, timer_controller):
        self.timer_controller = timer_controller
        self.timer_controller.time_signal_in_s.connect(self.update_gui_timer)

    def update_gui_timer(self, time_s: int):
        if time_s < 0:
            self.timer_label.setText("00:00")
            return
        elif time_s == 0:
            #timer has ended
            self.cycle_not_running()
        else:
            #timer is still going
            self.timer_label.setText(self.get_time(time_s))
