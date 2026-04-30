from __future__ import annotations

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

class EstopWarningPage(QWidget):

    def __init__(self,parent=None,):
        """
        This page shows the estop warning, and cannot be removed unless the physical estop switch has been pressed.
        """
        super().__init__(parent)
        self.parent = parent
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
        self.warning_status = QLabel("The Emergency Stop has been pressed.\nPlease return the E-Stop to its\noriginal position to continue system use.")
        cycle_status_font = QFont("Ubuntu", 24)
        cycle_status_font.setBold(True)
        self.warning_status.setFont(cycle_status_font)
        self.warning_status.setStyleSheet("color: #0474BA;")
        self.warning_status.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.warning_status)
        
        self.content_box.setLayout(content_layout)
        self.main_layout.addWidget(self.content_box)

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