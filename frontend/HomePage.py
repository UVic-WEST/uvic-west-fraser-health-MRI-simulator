from PySide6.QtWidgets import(
    QWidget,
    QGridLayout
)
from frontend.home_page_widgets.CyclePlayerWidget import CyclePlayerWidget

class HomePage(QWidget):
    def __init__(self, controller):

        #basic setup
        super().__init__()
        self.controller = controller

        self.component_layout = QGridLayout()
        self.play_widget = CyclePlayerWidget()
        self.component_layout.addWidget(self.play_widget)
        self.setLayout(self.component_layout)
