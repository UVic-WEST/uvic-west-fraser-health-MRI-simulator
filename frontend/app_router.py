from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QStackedLayout,
)

from frontend.home_page import HomePage
from backend.home_page_logic import HomePageLogic

from frontend.sign_in_page import SignInPage

from frontend.confirmation_page import ConfirmationPage

from frontend.cycle_running_page import CycleRunningPage
from backend.cycle_running_page_logic import CycleRunningPageLogic

from embedded.light_controller import LightController

class AppRouter(QMainWindow):
    def __init__(self):
        super().__init__()

        #SHARED RESOURCES. PLEASE PASS THESE IN TO YOUR FILES THROUGH THIS FILE
        self.light_controller = LightController(self)

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
        self.cycle_running_page_controller = CycleRunningPageLogic()
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