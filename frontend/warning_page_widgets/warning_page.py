from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap, 
    QFont
)
from typing import Callable, Literal
from frontend.warning_page_widgets.confirmation_buttons import WarningButtons

class WarningPage(QWidget):

    DEFAULT_WARNING_MESSAGE = "WARNING"

    def __init__(
        self,
        parent=None,
        warning_message: str | None = None,
        on_confirm: Callable[[], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
        button_mode: Literal["green", "red", "both"] = "both",
        green_button_text: str = "CONTINUE",
        red_button_text: str = "CANCEL",
    ):
        """
        This function builds the warning page shown before custom cycle creation

        Args:
            parent: the parent widget for this page
            warning_message (str | None): optional warning text to display
            on_confirm (Callable[[], None] | None): optional callback when confirm is clicked
            on_cancel (Callable[[], None] | None): optional callback when cancel is clicked
            button_mode: which warning buttons to display ("green", "red", or "both")
            green_button_text: label for green button
            red_button_text: label for red button
        """
        super().__init__(parent)
        self.parent = parent
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.setFixedSize(1024,600)

        # Create main layout
        self.set_background("resources/cycle_running_page_assets/running_cycle.png")
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(self.main_layout)

        # Create white box with rounded corners
        self.content_box = QWidget()
        self.content_box.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)
        
        # Content layout inside white box
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(10)

        #setting up widgets

        # warning label
        self.warning_status = QLabel(warning_message or self.DEFAULT_WARNING_MESSAGE)
        cycle_status_font = QFont("Ubuntu", 24)
        cycle_status_font.setBold(True)
        self.warning_status.setFont(cycle_status_font)
        self.warning_status.setStyleSheet("color: #0474BA;")
        self.warning_status.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.warning_status)

        #setup for control buttons
        self.warning_buttons = WarningButtons(
            self,
            green_text=green_button_text,
            red_text=red_button_text,
            button_mode=button_mode,
        )
        self.warning_buttons.confirm_clicked.connect(self.warning_confirmed)
        self.warning_buttons.cancel_clicked.connect(self.warning_cancelled)
        content_layout.addWidget(self.warning_buttons)
        
        self.content_box.setLayout(content_layout)
        self.main_layout.addWidget(self.content_box)

    def set_warning_message(self, message: str):
        """
        Update the warning text displayed on the page.

        Args:
            message (str): text to display in the warning label
        """
        self.warning_status.setText(message)

    def set_callbacks(
        self,
        on_confirm: Callable[[], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
    ):
        """
        Update confirm/cancel callbacks used by warning buttons.

        Args:
            on_confirm (Callable[[], None] | None): callback for confirm action
            on_cancel (Callable[[], None] | None): callback for cancel action
        """
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

    def set_button_config(
        self,
        button_mode: Literal["green", "red", "both"] = "both",
        green_button_text: str | None = None,
        red_button_text: str | None = None,
    ):
        """
        Update warning button visibility and labels.

        Args:
            button_mode: which warning buttons to display ("green", "red", or "both")
            green_button_text: optional label for green button
            red_button_text: optional label for red button
        """
        self.warning_buttons.set_button_config(
            button_mode=button_mode,
            green_text=green_button_text,
            red_text=red_button_text,
        )

    def set_background(self, image_path):
        """
        This sets the background of the page

        Args:
            image_path (str): path to the asset for the background image
        """
        
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(image_path).scaled(
            self.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        ))
        self.bg_label.setGeometry(0, 1, self.width(), self.height())
        self.bg_label.lower()  # send to back

    def warning_cancelled(self):
        """
        Handle cancel click; runs on_cancel callback if provided,
        otherwise falls back to the sign-in page.
        """
        if self.on_cancel is not None:
            self.on_cancel()
            return

        self.parent.show_signin()

    def warning_confirmed(self):
        """
        Handle confirm click; runs on_confirm callback if provided,
        otherwise falls back to the home page.
        """
        if self.on_confirm is not None:
            self.on_confirm()
            return

        self.parent.show_home()