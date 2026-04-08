from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap,
    QFont,
)

from frontend.help_widgets.help_screen import HelpOverlay
from frontend.help_widgets.help_button import HelpButton

from frontend.running_cycle_page_widgets.controlling_buttons import ControllingButtons
from frontend.running_cycle_page_widgets.timer_widget import TimerWidget


class CycleRunningPage(QWidget):
    def __init__(self, controller, cycle, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.cycle = cycle
        self.is_paused = False
        self.setFixedSize(1024, 600)

        # Create main layout
        self.set_background("resources/cycle_running_page_assets/running_cycle.png")
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.main_layout)

        # setting up widgets

        # Cycle running label
        self.cycle_status = QLabel("RUNNING")
        cycle_status_font = QFont("Ubuntu", 24)
        self.cycle_status.setFont(cycle_status_font)
        self.cycle_status.setStyleSheet(
            "color: white; \nbackground-color: #0474BA;"
        )
        self.cycle_status.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.cycle_status)

        # adding the countdown. Timer sends a dummy cycle time of 30s REMOVE LATER
        self.countdown_timer = TimerWidget(self)
        self.countdown_timer.connect_to_backend(self.controller)
        self.main_layout.addWidget(self.countdown_timer)

        self.help_manual_path = None
        self.help_overlay = HelpOverlay(self.help_manual_path, self)

        # setting up help button
        self.help_button = HelpButton(self)
        self.help_button.move(20, 20)
        self.help_button.raise_()
        self.help_button.clicked.connect(self.help_pressed)

        # setup for control buttons
        self.controlling_buttons = ControllingButtons(self)
        self.main_layout.addSpacing(40)
        self.main_layout.addWidget(self.controlling_buttons)

        self.controller.cycle_start_failed.connect(self._on_cycle_start_failed)

    def _on_cycle_start_failed(self, message: str):
        """Invalid cycle id or missing config: show message and leave running page."""
        QMessageBox.warning(
            self,
            "Cannot start cycle",
            message,
        )
        self.parent.show_home()

    def help_pressed(self):
        """
        Shows the help screen overlay for this page
        """
        self.pause_cycle()
        self.controlling_buttons.set_resume_button()
        self.help_overlay.show()
        self.help_overlay.raise_()

    def play_cycle(self, cycle_id):
        """
        Start the selected cycle by passing its ID and duration to the controller.
        """
        self.cycle = cycle_id
        self.controller.start_cycle(cycle_id)
        self.cycle_status.setText("RUNNING")

    def pause_cycle(self):
        """
        pauses the currently running cycle
        """
        self.controller.pause_cycle()
        self.cycle_status.setText("PAUSED")

    def resume_cycle(self):
        """
        resumes the currently running cycle
        """
        self.controller.resume_cycle()
        self.cycle_status.setText("RUNNING")

    def stop_cycle(self):
        """
        stops the currently running cycle
        """
        self.controller.stop_cycle()
        self.parent.show_home()

    def cycle_completed(self):
        """
        when cycle is completed, return to the homepage
        """
        self.parent.show_home()

    def update_cycle(self, cycle):
        """
        update the current cycle that will be played
        """
        self.curr_cycle = cycle
        print('current cycle: cycle["minutes"],cycle["seconds"]')

    def set_background(self, image_path):
        """
        organizes the background of the running cycle page
        """
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(
            QPixmap(image_path).scaled(
                self.size(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation,
            )
        )
        self.bg_label.setGeometry(0, 1, self.width(), self.height())
        self.bg_label.lower()  # send to back
