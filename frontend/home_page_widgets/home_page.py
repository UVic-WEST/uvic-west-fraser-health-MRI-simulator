from PySide6.QtWidgets import(
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from frontend.help_widgets.help_screen import HelpOverlay
from frontend.help_widgets.help_button import HelpButton

from frontend.home_page_widgets.cycle_player_widget import CyclePlayerWidget
from frontend.home_page_widgets.sound_controls_widget import SoundControlsWidget
from frontend.home_page_widgets.light_controls_widget import LightControlsWidget
from frontend.home_page_widgets.sign_out_button import SignOutButton


class HomePage(QWidget):
    def refresh_cycles_from_backend(self):
        """
        Refresh the cycle list from the backend and update the player widget.
        Call this when rerouting to the homepage to ensure the list is up to date.
        """
        cycles = self.cycle_factory.list_cycles()
        cycle_tuples = [(c.cycle_id, c.cycle_name) for c in cycles]
        self.play_widget.cycle_selector_widget.cycles = cycle_tuples
        self.play_widget.cycle_selector_widget.id_to_name = {cid: name for cid, name in cycle_tuples}
        self.play_widget.cycle_selector_widget.name_to_id = {name: cid for cid, name in cycle_tuples}
        self.play_widget.cycle_selector_widget.cycle_selector.clear()
        for cid, name in cycle_tuples:
            self.play_widget.cycle_selector_widget.cycle_selector.addItem(name, cid)
        self.play_widget.cycle_selector_widget.cycle_selector.setCurrentIndex(0)

    def __init__(self, controller, light_controller, sound_controller, parent=None):
        """
        This function builds the HomePage UI and initializes page-level state

        Args:
            controller: the page/controller reference used by HomePage
            light_controller: the manual light panel controller reference
            sound_controller: the manual sound panel controller reference
            parent: the parent widget for this page
        """

        #Homepage setup
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.light_controller = light_controller
        self.sound_controller = sound_controller
        self.main_layout = QGridLayout()
        self.main_layout.setContentsMargins(40, 110, 40, 40)
        self.cur_cycle_id = None

        self.help_manual_path = None
        self.help_overlay = HelpOverlay(self.help_manual_path,self)

        # Get cycles from backend
        from backend.cycle_factory import CycleFactory
        self.cycle_factory = CycleFactory()
        cycles = self.cycle_factory.list_cycles()
        cycle_tuples = [(c.cycle_id, c.cycle_name) for c in cycles]

        #setting up and organizing widgets
        self.play_widget = CyclePlayerWidget(cycle_tuples, self)
        self.sound_controls_widget = SoundControlsWidget(self.sound_controller, self)
        self.light_controls_widget = LightControlsWidget(self.light_controller, self)

        #right column: sound controls stacked above light controls
        right_col = QVBoxLayout()
        right_col.setSpacing(20)
        right_col.setContentsMargins(0, 0, 0, 0)
        right_col.addWidget(self.sound_controls_widget)
        right_col.addWidget(self.light_controls_widget)
        right_col.addStretch()

        #horizontal row: cycle player | stacked sound+light controls
        widgets_row = QHBoxLayout()
        widgets_row.setSpacing(20)
        widgets_row.setContentsMargins(0, 0, 0, 0)
        widgets_row.addWidget(self.play_widget)
        widgets_row.addLayout(right_col)
        widgets_container = QWidget()
        widgets_container.setLayout(widgets_row)
        self.main_layout.addWidget(widgets_container, 0, 0, Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(self.main_layout)

        #setting up sign out button (positioned absolutely in top left)
        self.sign_out_button = SignOutButton(self)
        self.sign_out_button.move(20, 20)
        self.sign_out_button.raise_()  # Bring to front

        #setting up help button
        self.help_button = HelpButton(self)
        self.help_button.move(140, 20)
        self.help_button.raise_()
        self.help_button.clicked.connect(self.help_pressed)

        #setting up logo (positioned absolutely so it doesn't affect layout)
        logo_path = 'resources/frontend_common_assets/fraser_health_logo.png'
        logo_pixmap = QPixmap(logo_path)
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setScaledContents(False)
        self.logo_label.adjustSize()
        self.logo_label.raise_()  # Bring to front
    
    def help_pressed(self):
        self.help_overlay.show()
        
    def resizeEvent(self, event):
        """
        This function repositions the logo when the widget is resized

        Args:
            event: the Qt resize event passed by the framework
        """
        super().resizeEvent(event)
        # Position logo in top-right corner with padding
        self.logo_label.move(self.width() - self.logo_label.width() - 40, 20)

    ###########################
    #######################
    # stores the currently selected cycle ID from child widgets
    def set_cur_cycle(self, cycle_id):
        """
        Stores the currently selected cycle ID
        Args:
            cycle_id: the ID of the selected cycle
        """
        self.cur_cycle_id = cycle_id

    
    def set_selected_cycle(self, cycle_id):
        self.set_cur_cycle(cycle_id)
        
    
    def play_selected_cycle(self):
        """
        Requests playback of the currently selected cycle by ID
        """
        print("Current cycle confirmed to play (ID):", self.cur_cycle_id)
        self.close_manual_controllers()
        self.parent.play_cycle(self.cur_cycle_id)

    
    def signout(self):
        '''
        when sign out button is pressed, user is signed out and sent to sign in page.
        '''
        self.parent.signout()
        self.close_manual_controllers()


    def show_custom_cycle_warning(self):
        """
        Routes to the MRI warning, then create-cycle flow. Must use AppRouter's
        ``show_custom_cycle_warning`` so confirm/cancel callbacks are set; bare
        ``show_warning()`` leaves callbacks unset and Continue falls back to home.
        """
        self.close_manual_controllers()
        self.parent.show_custom_cycle_warning()

    def close_manual_controllers(self):
        """
        Collapse manual sound/light panels. Does not navigate — routing stays with the caller.
        """
        if self.sound_controls_widget._expanded:
            self.sound_controls_widget._toggle_panel()

        if self.light_controls_widget._expanded:
            self.light_controls_widget._toggle_panel()