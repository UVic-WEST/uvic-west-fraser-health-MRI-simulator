from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QStackedLayout,
    QMessageBox,
)

from frontend.home_page_widgets.home_page import HomePage
from backend.home_page_logic import HomePageLogic

from frontend.sign_in_page_widgets.sign_in_page import SignInPage
from frontend.sign_in_page_widgets.timed_out_page import TimeOutPage
from backend.auth import Auth

from frontend.warning_page_widgets.warning_page import WarningPage

from frontend.running_cycle_page_widgets.cycle_running_page import CycleRunningPage
from frontend.running_cycle_page_widgets.cycle_summary_confirmation import CyclePreviewPage
from backend.cycle_running_page_logic import CycleRunningPageLogic

from frontend.create_cycle_widgets.create_cycle_pages import CreateCycleRouter

from embedded.light_controller import LightController
from embedded.sound_player import SoundPlayer
from backend.manual_light_controller import ManualLightController
from backend.manual_sound_controller import ManualSoundController
from backend.cycle_factory import CycleFactory

from embedded.estop_controller import EStopController
from frontend.warning_page_widgets.estop_page import EstopWarningPage

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
        self.cycle_preview_page = QWidget() 
        self.main_layout.addWidget(self.cycle_running_page)
        self.main_layout.addWidget(self.cycle_preview_page)

        #Code for create cycle pages (pass AppRouter explicitly — parent becomes central QWidget)
        self.create_cycle_router = CreateCycleRouter(self, self.app)
        self.main_layout.addWidget(self.create_cycle_router)

        #Estop Controller
        self.estop_controller = EStopController(self)
        self.estop_controller.estop_active.connect(self.estop_event)
        self.estop_warning_page = EstopWarningPage(self)
        self.main_layout.addWidget(self.estop_warning_page)

        self.setCentralWidget(self.app)

    def estop_event(self, status:bool):
        """
        When Estop is pressed, it will reveal the estop screen and stop any relevant processes.
        Once Estop is no longer active, it will return the user to the sign in screen.
        """
        current_page = self.main_layout.currentWidget()
        if status:
            if current_page is self.cycle_running_page:
                self.cycle_running_page.stop_cycle()
            elif current_page is self.create_cycle_router:
                self.create_cycle_router.cancel_create_cycle()
            elif current_page is self.home_page:
                self.home_page.close_manual_controllers
            self.signout()
            self.main_layout.setCurrentWidget(self.estop_warning_page)

        if not status:
            self.main_layout.setCurrentWidget(self.sign_in_page)

    def play_cycle(self, selected_cycle_id=None):
        """
        Prepares a cycle to be played, selected on the homepage.
        Args:
            selected_cycle_id (str): selected cycle id to play
        """
        self.cur_cycle = selected_cycle_id
        self.selected_cycle = selected_cycle_id
        self.show_cycle_preview_page()

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

    def show_cycle_preview_page(self):
        """
        Show preview of selected cycle before running to confirm cycle selection
        """
        cycle_id = self._resolve_play_cycle_id(self.cur_cycle)
        cycle_config = self.cycle_factory.get_cycle_by_id(cycle_id)
        self.cycle_preview_page = CyclePreviewPage(cycle_config, self)
        self.main_layout.addWidget(self.cycle_preview_page)
        self.main_layout.setCurrentWidget(self.cycle_preview_page)

    def show_custom_cycle_warning(self):
        """
        Show warning page for custom cycle creation with custom-cycle navigation.
        """
        self.show_warning(
            warning_message="WARNING!\n REMOVE CHILD FROM MRI\n BEFORE PROCEEDING",
            on_confirm=self.show_create_cycle_pages,
            on_cancel=self.show_home,
        )

    def _resolve_play_cycle_id(self, selected) -> int | None:
        """Resolve ``cur_cycle`` to a real ``cycle_id`` present in ``cycle_factory``.

        The home page usually passes the combo's user data (int). We also support
        matching by ``cycle_name`` or a trailing number in labels like ``Cycle 2``,
        but only if that id still exists. Returns ``None`` if nothing valid is selected
        or the id is not in the current list (no silent fallback to cycle 1).
        """
        if selected is None:
            return None

        if isinstance(selected, int):
            try:
                self.cycle_factory.get_cycle_by_id(selected)
            except ValueError:
                return None
            return selected

        name = str(selected).strip()
        for c in self.cycle_factory.list_cycles():
            if c.cycle_name == name:
                return c.cycle_id

        tail = name.rsplit(None, 1)[-1]
        if tail.isdigit():
            cid = int(tail)
            try:
                self.cycle_factory.get_cycle_by_id(cid)
            except ValueError:
                return None
            return cid

        return None

    def play_cycle_confirmed(self):
        """
        This function routes the app to the cycle running page when the user has confirmed 
        they want to play a cycle. Sends the selected cycle's ID and duration to the running logic. Called by cycle preview page.
        """
        cycle_id = self._resolve_play_cycle_id(self.cur_cycle)
        if cycle_id is None:
            QMessageBox.warning(
                self,
                "Cannot play cycle",
                "No cycle is selected, or the selected cycle is no longer available.",
            )
            self.show_home()
            return

        self.main_layout.setCurrentWidget(self.cycle_running_page)
        self.cycle_running_page.play_cycle(cycle_id)

    def show_home(self):
        """
        This function routes the application to show the homepage
        """
        self.cycle_factory.refresh()
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