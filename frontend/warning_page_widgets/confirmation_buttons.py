from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class WarningButtons(QWidget):
    confirm_clicked = Signal()
    cancel_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)
        button_layout.setAlignment(Qt.AlignCenter)

        # Continue button (green)
        self.yes_button = QPushButton("CONTINUE")
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
        self.no_button = QPushButton("CANCEL")
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

    def on_yes_clicked(self):
        print("Warning continue")
        self.confirm_clicked.emit()

    def on_no_clicked(self):
        print("Warning cancel")
        self.cancel_clicked.emit()
