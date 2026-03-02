from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout
)
from PlaySquareWidget import PlaySquareWidget

class CyclePlayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.play_square_widget = PlaySquareWidget()

        self.main_layout.addWidget(self.play_square_widget)
        self.setLayout(self.main_layout)

