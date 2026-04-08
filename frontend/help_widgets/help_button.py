from PySide6.QtWidgets import(
    QPushButton
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon, QRegion


class HelpButton(QPushButton):
    def __init__(self, parent):
        """ 
        The help button is used throughout the program to show the help screen overlay
        Args:
            parent(QWidget): parent calling this widget
        """
        super().__init__(parent)
        self.setFixedSize(50,50)
        self.setIconSize(QSize(50,50))
        self.setFlat(True)
        self.setFocusPolicy(Qt.NoFocus)
        #set icon for button
        self.setIcon(QIcon("resources/frontend_common_assets/help_button.png"))
