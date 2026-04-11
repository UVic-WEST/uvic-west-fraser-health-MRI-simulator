from PySide6.QtWidgets import (
    QWidget,
    QPushButton
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal

class CustomCycleButton(QWidget):
    custom_cycle_requested = Signal(int)

    def __init__(self, parent=None):
        """
        This function builds the Create Custom Cycle button widget

        Args:
            parent: the parent widget for this button container
        """
        super().__init__(parent)
        self.parent = parent
        
        #set widget size to match dropdown width
        self.setFixedSize(353, 50)
        
        #create the button
        self.custom_cycle_button = QPushButton("Create Custom Cycle", self)
        self.custom_cycle_button.setFixedSize(353, 50)
        self.custom_cycle_button.setFont(QFont("Ubuntu", 20))
        
        #orange button styling
        self.custom_cycle_button.setStyleSheet("""
            QPushButton {
                background-color: #FFA630;
                color: white;
                border: none;
                border-radius: 24px;
            }
            QPushButton:pressed {
                background-color: #FF8410;
            }
        """)
        
        #connect button click
        self.custom_cycle_button.clicked.connect(self.custom_cycle_button_pressed)

    def custom_cycle_button_pressed(self):
        """
        This function handles the Create Custom Cycle button press action.
        """
        self.custom_cycle_requested.emit(1)
