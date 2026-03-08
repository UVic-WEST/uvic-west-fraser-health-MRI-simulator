from PySide6.QtWidgets import(
    QWidget,
    QGridLayout
)
from PySide6.QtCore import Qt

from frontend.home_page_widgets.cycle_player_widget import CyclePlayerWidget

class HomePage(QWidget):
    def __init__(self, controller, parent=None):

        #Homepage setup
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.main_layout = QGridLayout()
        self.main_layout.setRowMinimumHeight(0, 90)
        self.cur_cycle = None

        #setting up and organizing widgets
        self.play_widget = CyclePlayerWidget(self)
        self.main_layout.addWidget(self.play_widget, 1, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.main_layout)

    def set_cur_cycle(self, cycle_name):
        self.cur_cycle = cycle_name

    # Backward-compatible alias while other callers are being updated.
    def set_selected_cycle(self, cycle_name):
        self.set_cur_cycle(cycle_name)
        
    def play_selected_cycle(self):
        print("Current cycle confirmed to play:", self.cur_cycle)
        self.parent.play_cycle(self.cur_cycle)
    