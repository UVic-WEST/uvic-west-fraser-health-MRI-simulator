from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from frontend.home_page_widgets.play_square_widget import PlaySquareWidget
class CyclePlayerWidget(QWidget):
    def __init__(self, parent=None):
        #setup
        super().__init__(parent)
        self.parent = parent
        self.main_layout = QVBoxLayout()
        self.cur_cycle = None

        #setting up widgets
        #setup for play square widget
        self.play_square_widget = PlaySquareWidget(self)
        self.main_layout.addWidget(self.play_square_widget)

        #setting layout
        self.setLayout(self.main_layout)

        #dummy cycle for future sprints, 
        #this would be selected from cycle selector embedded in this widget in later iteration
        self.play_square_widget.update_selected_cycle(self.cur_cycle)

    def play_selected_cycle(self):
        self.parent.play_selected_cycle()

