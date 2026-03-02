from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from frontend.home_page_widgets.PlaySquareWidget import PlaySquareWidget
from embedded.Cycle import Cycle

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

        #dummy cycle for future sprints, 
        #this would be selected from cycle selector embedded in this widget in later iteration
        self.cur_cycle = Cycle()
        self.play_square_widget.update_selected_cycle(self.cur_cycle)

