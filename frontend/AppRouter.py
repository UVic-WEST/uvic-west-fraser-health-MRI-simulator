from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QStackedLayout,
)

from frontend.HomePage import HomePage
from backend.HomePageLogic import HomePageLogic

from frontend.SignInPage import SignInPage

from frontend.CycleRunningPage import CycleRunningPage
from backend.CycleRunningLogic import CycleRunningLogic

class AppRouter(QMainWindow):
    def __init__(self):
        super().__init__()

        #create window
        self.setFixedSize(1024, 600)
        self.main_layout = QStackedLayout()
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("MRI Simulator")

        #create pages, connect controllers, add to app widget stack
        self.sign_in_Page = SignInPage()

        #Code for cycle running page. 
        self.cycle_running_page_controller = CycleRunningLogic()
        self.cycle_running_page = CycleRunningPage(self.cycle_running_page_controller,self,None)
        self.main_layout.addWidget(self.cycle_running_page)

        self.home_page_controller = HomePageLogic()
        self.home_page = HomePage(self.home_page_controller)
        self.main_layout.addWidget(self.home_page)

        #set layout of QstackedWidget
        self.app = QWidget()
        self.app.setLayout(self.main_layout)
        self.setCentralWidget(self.app)

    def show_home(self):
        self.main_layout.setCurrentWidget(self.home_page)