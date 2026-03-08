from PySide6.QtWidgets import (
    QWidget,
    QPushButton
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class CustomCycleButton(QWidget):
    '''
    GUI implementation for the "Create Custom Cycle" button on the homepage.
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Set widget size to match dropdown width
        self.setFixedSize(353, 50)
        
        # Create the button
        self.custom_cycle_button = QPushButton("Create Custom Cycle", self)
        self.custom_cycle_button.setFixedSize(353, 50)
        self.custom_cycle_button.setFont(QFont("Ubuntu", 20))
        
        # Orange button styling
        self.custom_cycle_button.setStyleSheet("""
            QPushButton {
                background-color: #FFA630;
                color: white;
                border: none;
                border-radius: 24px;
            }
            QPushButton:hover {
                background-color: #FF9520;
            }
            QPushButton:pressed {
                background-color: #FF8410;
            }
        """)
        
        # Connect button click
        self.custom_cycle_button.clicked.connect(self.custom_cycle_button_pressed)
    
    def custom_cycle_button_pressed(self):
        '''
        Handle button press - currently just prints to terminal.
        '''
        print("Create Custom Cycle selected")
