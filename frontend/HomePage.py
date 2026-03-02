from PySide6.QtWidgets import(
    QWidget,
    QGridLayout
)
#from ../backend/HomePageLogic import HomePageLogic
from CyclePlayerWidget import CyclePlayerWidget

class HomePage(QWidget):
    def __init__(self):

        #basic setup
        super().__init__()
        #self.controller = controller
        #self.setFixedSize(372,600)

        self.component_layout = QGridLayout()
        self.play_widget = CyclePlayerWidget()
        self.component_layout.addWidget(self.play_widget)
        self.setLayout(self.component_layout)
