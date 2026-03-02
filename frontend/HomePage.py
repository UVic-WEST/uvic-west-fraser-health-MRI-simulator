from PySide6.QtWidgets import(
    QWidget,
    QGridLayout
)
from frontend.home_page_widgets.CyclePlayerWidget import CyclePlayerWidget

class HomePage(QWidget):
    def __init__(self, controller):

        #Homepage setup
        super().__init__()
        self.controller = controller
        self.main_layout = QGridLayout()

        #setting up and organizing widgets
        self.play_widget = CyclePlayerWidget()
        self.main_layout.addWidget(self.play_widget)

        self.setLayout(self.main_layout)
