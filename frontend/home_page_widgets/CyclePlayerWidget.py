from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from frontend.home_page_widgets.PlaySquareWidget import PlaySquareWidget

class CyclePlayerWidget(QWidget):
    def __init__(self):
        #setup
        super().__init__()
        self.main_layout = QVBoxLayout()

        #setting up widgets
        #setup for play square widget
        self.play_square_widget = PlaySquareWidget()
        self.main_layout.addWidget(self.play_square_widget)

        #setting layout
        self.setLayout(self.main_layout)

