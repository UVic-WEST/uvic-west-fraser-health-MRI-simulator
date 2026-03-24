from PySide6.QtWidgets import (
    QWidget,
    QPushButton
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class SignOutButton(QWidget):
    def __init__(self, parent=None):
        """
        This function builds the Sign Out button widget 

        Args:
            parent: the parent widget for this button container
        """
        super().__init__(parent)
        self.parent = parent
        
        # Set widget size to contain the button
        self.setFixedSize(120, 45)
        
        # Create the button
        self.sign_out_button = QPushButton("Sign Out", self)
        self.sign_out_button.setGeometry(0, 0, 120, 45)
        self.sign_out_button.setFont(QFont("Ubuntu", 14))
        
        # Blue button styling to match the play square box
        self.sign_out_button.setStyleSheet("""
            QPushButton {
                background-color: #0474BA;
                color: white;
                border: none;
                border-radius: 22px;
            }
            QPushButton:pressed {
                background-color: #024570;
            }
        """)
        
        # Connect button click
        self.sign_out_button.clicked.connect(self.sign_out_button_pressed)
    
    def sign_out_button_pressed(self):
        """
        This function signs the user out and returns to the sign in page

        """
        self.parent.signout()

