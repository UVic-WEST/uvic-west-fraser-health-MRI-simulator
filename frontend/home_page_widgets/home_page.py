from PySide6.QtWidgets import(
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from frontend.home_page_widgets.cycle_player_widget import CyclePlayerWidget
from frontend.home_page_widgets.sound_controls_widget import SoundControlsWidget
from frontend.home_page_widgets.light_controls_widget import LightControlsWidget
from frontend.home_page_widgets.sign_out_button import SignOutButton


class HomePage(QWidget):
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
        self.cur_cycle = None

        #setting up and organizing widgets
        self.play_widget = CyclePlayerWidget(self)
        self.sound_controls_widget = SoundControlsWidget(self.sound_controller,self)
        self.light_controls_widget = LightControlsWidget(self.light_controller,self)

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

        #setting up logo (positioned absolutely so it doesn't affect layout)
        logo_path = 'resources/frontend_common_assets/fraser_health_logo.png'
        logo_pixmap = QPixmap(logo_path)
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setScaledContents(False)
        self.logo_label.adjustSize()
        self.logo_label.raise_()  # Bring to front
    
    
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
    # probably want to remove this and instead store in backend
    #stores the currently selected cycle from child widgets
    def set_cur_cycle(self, cycle_name):
        """
        This function stores the currently selected cycle

        Args:
            cycle_name: the name of the selected cycle
        """
        self.cur_cycle = cycle_name

    
    def set_selected_cycle(self, cycle_name):
        """
        This function forwards legacy cycle selection calls to set_cur_cycle

        Args:
            cycle_name: the name of the selected cycle
        """
        self.set_cur_cycle(cycle_name)
        
    
    def play_selected_cycle(self):
        """
        This function requests playback of the currently selected cycle
        """
        print("Current cycle confirmed to play:", self.cur_cycle)

        self.parent.play_cycle(self.cur_cycle)
        self.close_manual_controllers()

    
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
