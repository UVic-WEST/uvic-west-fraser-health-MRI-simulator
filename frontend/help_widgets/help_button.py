from PySide6.QtWidgets import(
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon

from frontend.helpers import make_button_circle

class HelpButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(50,50)
        self.setIconSize(QSize(50,50))
        self.setIcon(QIcon("resources/frontend_common_assets/help_button.png"))
        #make_button_circle(self,50,"transparent")