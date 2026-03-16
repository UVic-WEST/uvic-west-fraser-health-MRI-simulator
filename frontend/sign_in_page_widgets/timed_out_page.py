from PySide6.QtWidgets import(
    QWidget,
    QLabel,
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import (
    QTimer
)

GREY = "#676363"
TIMEOUT_TIME = 5

class TimeOutPage(QWidget):
    def __init__(self, parent=None):
        """
        This widget is the displayed timed out page which times out the system upon 3 failed logins.
        
        Args:
            parent (AppRouter): parent that creates/initializes this class
        """
        super().__init__(parent)
        self.parent = parent

        self.remaining_time = TIMEOUT_TIME
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        #fraser logo
        fraser_logo_path = 'resources/frontend_common_assets/fraser_health_logo_large.png'
        fraser_logo_pix = QPixmap(fraser_logo_path)
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(fraser_logo_pix)
        self.logo_label.move(90,139)

        #Message for user
        self.message_text = QLabel("Maximum failed \nlogin attempts reached.\nPlease return after system \ntimeout.",self)
        self.message_text.setFont(QFont("Ubuntu",32))
        self.message_text.setStyleSheet(f"color: {GREY}; qproperty-alignment: AlignCenter;")
        self.message_text.move(479,119)

        #countdown
        self.countdown = QLabel("30s",self)
        self.countdown.setFont(QFont("Ubuntu",64))
        self.countdown.move(653,340)
        self.countdown.setStyleSheet(f"color: {GREY}; qproperty-alignment: AlignCenter;")

        #this just says remaining as a separate set of text
        self.remaining_text = QLabel("Remaining.",self)
        self.remaining_text.setFont(QFont("Ubuntu",32))
        self.remaining_text.move(622,452)
        self.remaining_text.setStyleSheet(f"color: {GREY}; qproperty-alignment: AlignCenter;")

    def start_countdown(self):
        """
        Starts the countdown for timeout
        """
        self.remaining_time = TIMEOUT_TIME
        self.countdown.setText(str(self.remaining_time)+"s")
        self.timer.start()
        
    def update_timer(self):
        """
        updates the on screen countdown for timeout
        """
        self.countdown.setText(str(self.remaining_time)+"s")
        self.remaining_time -= 1

        if self.remaining_time < 0: 
            self.complete_timeout()

    def complete_timeout(self):
        """
        returns user to sign in page when timeout countdown is completed
        """
        self.timer.stop()
        self.parent.show_signin()
        





