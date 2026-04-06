from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QStackedLayout,
)

from frontend.home_page_widgets.home_page import HomePage
from backend.home_page_logic import HomePageLogic

from frontend.sign_in_page_widgets.sign_in_page import SignInPage
from frontend.sign_in_page_widgets.timed_out_page import TimeOutPage
from backend.auth import Auth

from frontend.confirmation_page_widgets.confirmation_page import ConfirmationPage
from frontend.warning_page_widgets.warning_page import WarningPage

from frontend.running_cycle_page_widgets.cycle_running_page import CycleRunningPage
from backend.cycle_running_page_logic import CycleRunningPageLogic

from frontend.create_cycle_widgets.create_cycle_pages import CreateCycleRouter

from embedded.light_controller import LightController
from embedded.sound_player import SoundPlayer
from backend.manual_light_controller import ManualLightController
from backend.manual_sound_controller import ManualSoundController
from backend.cycle_factory import CycleFactory

#PASSWORD 
PASS = '2026'

class AppRouter(QMainWindow):
    def __init__(self,parent=None):
        """
        This is the App router class which initializes the UI pages and their respective controllers.
        It also handles page routing logic.
        """

        super().__init__(parent)
        self.cur_cycle = None

        #SHARED RESOURCES. PLEASE PASS THESE IN TO YOUR FILES THROUGH THIS FILE
        self.light_controller = LightController(self)
        self.sound_player = SoundPlayer()
        self.manual_light_controller = ManualLightController(
            self.light_controller, parent=self
        )
        self.manual_sound_controller = ManualSoundController(
            self.sound_player, parent=self
        )

        self.cycle_factory = CycleFactory()

        #create window
        self.setFixedSize(1024, 600)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("MRI Simulator")

        self.app = QWidget()
        self.main_layout = QStackedLayout()
        self.app.setLayout(self.main_layout)

        #create pages, connect controllers, add to app widget stack
        #code for sign in page
        self.sign_in_page_controller = Auth(PASS, self)
        self.sign_in_page = SignInPage(self.sign_in_page_controller, self)
        self.timed_out_page = TimeOutPage(self.sign_in_page_controller, self)
        self.main_layout.addWidget(self.sign_in_page)
        self.main_layout.addWidget(self.timed_out_page)

        #code for homepage
        self.home_page_controller = HomePageLogic(cycle_factory=self.cycle_factory)
        self.home_page = HomePage(self.home_page_controller, self.manual_light_controller, self.manual_sound_controller, self)
        self.main_layout.addWidget(self.home_page)

        #Code for confirmation page
        self.confirmation_page = ConfirmationPage(None,self)
        self.confirmation_page.start_cycle_requested.connect(self.play_cycle_confirmed)
        self.confirmation_page.cancel_requested.connect(self.show_home)
        self.main_layout.addWidget(self.confirmation_page)

        #Code for warning page
        self.warning_page = WarningPage(self)
        self.main_layout.addWidget(self.warning_page)

        #Code for cycle running page. 
        self.cycle_running_page_controller = CycleRunningPageLogic(
            sound_player=self.sound_player,
            light_controller=self.light_controller,
            parent=self,
            cycle_factory=self.cycle_factory,
        )
        self.cycle_running_page = CycleRunningPage(self.cycle_running_page_controller,None,self)
        self.main_layout.addWidget(self.cycle_running_page)

        #Code for create cycle pages (pass AppRouter explicitly — parent becomes central QWidget)
        self.create_cycle_router = CreateCycleRouter(self, self.app)
        self.main_layout.addWidget(self.create_cycle_router)

        self.setCentralWidget(self.app)


    def play_cycle(self, selected_cycle_id=None):
        """
        Prepares a cycle to be played, selected on the homepage.
        Args:
            selected_cycle_id (str): selected cycle id to play
        """
        self.cur_cycle = selected_cycle_id
        self.selected_cycle = selected_cycle_id
        # Lookup name for confirmation page
        cycle_name = None
        if selected_cycle_id:
            # Use the HomePage's cycle_factory to get the name
            try:
                cycle_obj = self.home_page.cycle_factory.get_cycle_by_id(selected_cycle_id)
                cycle_name = cycle_obj.cycle_name
            except Exception:
                cycle_name = selected_cycle_id
        # Pass both id and name to confirmation page
        self.confirmation_page.set_cycle((selected_cycle_id, cycle_name))
        self.main_layout.setCurrentWidget(self.confirmation_page)

    def show_confirmation(self):
        """
        This function shows the play cycle confirmation page to play a cycle
        """
        self.main_layout.setCurrentWidget(self.confirmation_page)

    def show_warning(
        self,
        warning_message: str | None = None,
        on_confirm=None,
        on_cancel=None,
        button_mode: str = "both",
        green_button_text: str = "CONTINUE",
        red_button_text: str = "CANCEL",
    ):
        """
        This function shows the warning page with optional message and button handlers.

        Args:
            warning_message (str | None): warning text to display
            on_confirm: callback for confirm button; uses warning page fallback if None
            on_cancel: callback for cancel button; uses warning page fallback if None
            button_mode: which warning buttons to show ("green", "red", "both")
            green_button_text: label for green warning button
            red_button_text: label for red warning button
        """
        if warning_message is not None:
            self.warning_page.set_warning_message(warning_message)
        else:
            self.warning_page.set_warning_message(self.warning_page.DEFAULT_WARNING_MESSAGE)

        self.warning_page.set_callbacks(on_confirm=on_confirm, on_cancel=on_cancel)
        self.warning_page.set_button_config(
            button_mode=button_mode,
            green_button_text=green_button_text,
            red_button_text=red_button_text,
        )
        self.main_layout.setCurrentWidget(self.warning_page)

    def show_custom_cycle_warning(self):
        """
        Show warning page for custom cycle creation with custom-cycle navigation.
        """
        self.show_warning(
            warning_message="WARNING!\n REMOVE CHILD FROM MRI\n BEFORE PROCEEDING",
            on_confirm=self.show_create_cycle_pages,
            on_cancel=self.show_home,
        )

    def play_cycle_confirmed(self):
        """
        This function routes the app to the cycle running page when the user has confirmed 
        they want to play a cycle. Sends the selected cycle's ID and duration to the running logic.
        """
        # Get the selected cycle ID
        selected_cycle_id = self.cur_cycle
        self.main_layout.setCurrentWidget(self.cycle_running_page)
        self.cycle_running_page.play_cycle(selected_cycle_id)

    def show_home(self):
        """
        This function routes the application to show the homepage
        """
        self.home_page.refresh_cycles_from_backend()
        self.main_layout.setCurrentWidget(self.home_page)

    def timeout_signin(self):
        """
        This function routes the application to the time out page after failed sign in then starts the 30s timeout counter
        """
        self.main_layout.setCurrentWidget(self.timed_out_page)

    def signout(self):
        """
        Properly signs user out in auth then moves to show the signin page
        """
        self.sign_in_page_controller.logout()
        self.show_signin()

    def show_signin(self):
        """
        This function routes the application to the sign in page after completed timeout
        """
        self.main_layout.setCurrentWidget(self.sign_in_page)

    def show_create_cycle_pages(self):
        """
        routes application to the create cycle pages via the create cycle page router.
        """
        self.create_cycle_router.create_new_cycle()
        self.main_layout.setCurrentWidget(self.create_cycle_router)