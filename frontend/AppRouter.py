from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QStackedLayout,
)

from frontend.HomePage import HomePage
from backend.HomePageLogic import HomePageLogic

from frontend.SignInPage import SignInPage

from frontend.ConfirmationPage import ConfirmationPage

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

        #code for homepage
        self.home_page_controller = HomePageLogic()
        self.home_page = HomePage(self.home_page_controller,self)
        self.main_layout.addWidget(self.home_page)

        #Code for confirmation page
        self.confirmation_page = ConfirmationPage(None,None,self)
        self.confirmation_page.start_cycle_requested.connect(self.play_cycle_confirmed)
        self.confirmation_page.cancel_requested.connect(self.show_home)
        self.main_layout.addWidget(self.confirmation_page)

        #Code for cycle running page. 
        self.cycle_running_page_controller = CycleRunningLogic()
        self.cycle_running_page = CycleRunningPage(self.cycle_running_page_controller,None,self)
        self.main_layout.addWidget(self.cycle_running_page)

        #set layout of QstackedWidget
        self.app = QWidget()
        self.app.setLayout(self.main_layout)
        self.setCentralWidget(self.app)

    def play_cycle(self):
        self.main_layout.setCurrentWidget(self.confirmation_page)

    def show_confirmation(self):
        self.main_layout.setCurrentWidget(self.confirmation_page)

    def play_cycle_confirmed(self):
        self.main_layout.setCurrentWidget(self.cycle_running_page)
        #REMOVE LATER
        dummytime = 30
        self.cycle_running_page.play_cycle(dummytime)

    def show_home(self):
        self.main_layout.setCurrentWidget(self.home_page)