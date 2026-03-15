from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QStackedLayout,
)

from frontend.home_page import HomePage
from backend.home_page_logic import HomePageLogic

from frontend.sign_in_page import SignInPage
from frontend.sign_in_page_widgets.timed_out_page import TimeOutPage

from frontend.confirmation_page import ConfirmationPage

from frontend.cycle_running_page import CycleRunningPage
from backend.cycle_running_page_logic import CycleRunningPageLogic

from embedded.light_controller import LightController

class AppRouter(QMainWindow):
    def __init__(self):
        """
        This is the App router class which initializes the UI pages and their respective controllers.
        It also handles page routing logic.
        """

        super().__init__()
        self.cur_cycle = None

        #SHARED RESOURCES. PLEASE PASS THESE IN TO YOUR FILES THROUGH THIS FILE
        self.light_controller = LightController(self)

        #create window
        self.setFixedSize(1024, 600)
        self.main_layout = QStackedLayout()
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("MRI Simulator")

        #create pages, connect controllers, add to app widget stack
        #code for sign in page
        self.sign_in_page_controller = None #CHANGE WHEN THERES A CONTROLLER TO CONNECT
        self.sign_in_page = SignInPage(self.sign_in_page_controller, self)
        self.timed_out_page = TimeOutPage(self)
        self.main_layout.addWidget(self.sign_in_page)
        self.main_layout.addWidget(self.timed_out_page)

        #code for homepage
        self.home_page_controller = HomePageLogic()
        self.home_page = HomePage(self.home_page_controller,self)
        self.main_layout.addWidget(self.home_page)

        #Code for confirmation page
        self.confirmation_page = ConfirmationPage(None,self)
        self.confirmation_page.start_cycle_requested.connect(self.play_cycle_confirmed)
        self.confirmation_page.cancel_requested.connect(self.show_home)
        self.main_layout.addWidget(self.confirmation_page)

        #Code for cycle running page. 
        self.cycle_running_page_controller = CycleRunningPageLogic(self)
        self.cycle_running_page = CycleRunningPage(self.cycle_running_page_controller,None,self)
        self.main_layout.addWidget(self.cycle_running_page)

        #set layout of QstackedWidget
        self.app = QWidget()
        self.app.setLayout(self.main_layout)
        self.setCentralWidget(self.app)


    def play_cycle(self, selected_cycle=None):
        """
        This function prepares a cycle to be played, selected on the homepage.

        Args:
            selected_cycle (Cycle): selected cycle to play
        """
        
        self.cur_cycle = selected_cycle
        # Backward-compatible alias while transitioning to cur_cycle naming.
        self.selected_cycle = selected_cycle
        self.confirmation_page.set_cycle(self.cur_cycle)
        self.main_layout.setCurrentWidget(self.confirmation_page)

    def show_confirmation(self):
        """
        This function shows the play cycle confirmation page to play a cycle
        """
        self.main_layout.setCurrentWidget(self.confirmation_page)

    def play_cycle_confirmed(self):
        """
        This function routes the app to the cycle running page when the user has confirmed 
        they want to play a cycle
        """
        self.main_layout.setCurrentWidget(self.cycle_running_page)
        #REMOVE LATER
        dummytime = 30
        self.cycle_running_page.play_cycle(dummytime)

    def show_home(self):
        """
        This function routes the application to show the homepage
        """
        self.main_layout.setCurrentWidget(self.home_page)

    def timeout_signin(self):
        """
        This function routes the application to the time out page after failed sign in then starts the 30s timeout counter
        """
        self.timed_out_page.start_countdown()
        self.main_layout.setCurrentWidget(self.timed_out_page)

    def show_signin(self):
        """
        This function routes the application to the sign in page after completed timeout
        """
        self.main_layout.setCurrentWidget(self.sign_in_page)