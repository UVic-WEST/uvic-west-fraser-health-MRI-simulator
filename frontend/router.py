from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QStackedLayout,
)

from HomePage import HomePage
from SignInPage import SignInPage
from CycleRunningPage import CycleRunningPage

class AppRouter(QMainWindow):
    def __init__(self):
        super().__init__()

        #create window
        self.setFixedSize(1024, 600)
        self.main_layout = QStackedLayout()
        self.setWindowTitle("MRI Simulator")

        #create page routings with their respective controllers
        self.signInPage = SignInPage()
        self.HomePage = HomePage()
        self.CycleRunningPage = CycleRunningPage()

        #set layout of QstackedWidget
        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)