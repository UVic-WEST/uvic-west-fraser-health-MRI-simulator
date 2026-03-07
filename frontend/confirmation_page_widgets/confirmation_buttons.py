from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class ConfirmationButtons(QWidget):
    yes_clicked = Signal()
    no_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)
        button_layout.setAlignment(Qt.AlignCenter)

        # Yes button (green)
        self.yes_button = QPushButton("YES")
        self.yes_button.setFixedSize(120, 60)
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

        # No button (red)
        self.no_button = QPushButton("NO")
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
        print("Yes")
        self.yes_clicked.emit()

    def on_no_clicked(self):
        print("No")
        self.no_clicked.emit()
