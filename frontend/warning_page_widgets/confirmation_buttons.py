from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from typing import Literal


class WarningButtons(QWidget):
    confirm_clicked = Signal()
    cancel_clicked = Signal()

    def __init__(
        self,
        parent=None,
        green_text: str = "CONTINUE",
        red_text: str = "CANCEL",
        button_mode: Literal["green", "red", "both"] = "both",
    ):
        super().__init__(parent)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)
        button_layout.setAlignment(Qt.AlignCenter)
        self.button_layout = button_layout

        # Continue button (green)
        self.yes_button = QPushButton(green_text)
        self.yes_button.setFixedSize(180, 60)
        self.yes_button.setFont(QFont("Ubuntu", 16, QFont.Bold))
        self.yes_button.setStyleSheet("""
            QPushButton {
                background-color: #00AA00;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #008800;
            }
            QPushButton:pressed {
                background-color: #006600;
            }
        """)
        self.yes_button.clicked.connect(self.on_yes_clicked)

        # Cancel button (red)
        self.no_button = QPushButton(red_text)
        self.no_button.setFixedSize(120, 60)
        self.no_button.setFont(QFont("Ubuntu", 16, QFont.Bold))
        self.no_button.setStyleSheet("""
            QPushButton {
                background-color: #EC221F;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d41810;
            }
            QPushButton:pressed {
                background-color: #b01208;
            }
        """)
        self.no_button.clicked.connect(self.on_no_clicked)

        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)
        self.setLayout(button_layout)
        self.set_button_config(button_mode=button_mode)

    def set_button_config(
        self,
        button_mode: Literal["green", "red", "both"] = "both",
        green_text: str | None = None,
        red_text: str | None = None,
    ):
        """
        Configure button visibility and optional labels.

        Args:
            button_mode: "green", "red", or "both"
            green_text: optional text for the green confirm button
            red_text: optional text for the red cancel button
        """
        if green_text is not None:
            self.yes_button.setText(green_text)
        if red_text is not None:
            self.no_button.setText(red_text)

        if button_mode not in {"green", "red", "both"}:
            button_mode = "both"

        show_green = button_mode in {"green", "both"}
        show_red = button_mode in {"red", "both"}
        self.yes_button.setVisible(show_green)
        self.no_button.setVisible(show_red)

        # Keep centered look whether one or two buttons are shown.
        self.button_layout.setSpacing(40 if button_mode == "both" else 0)

    def on_yes_clicked(self):
        print("Warning continue")
        self.confirm_clicked.emit()

    def on_no_clicked(self):
        print("Warning cancel")
        self.cancel_clicked.emit()
