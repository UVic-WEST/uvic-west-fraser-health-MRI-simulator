from PySide6.QtWidgets import( # type: ignore
    QWidget,
    QVBoxLayout,
    QLabel
)


from frontend.running_cycle_page_widgets.ControllingButtons import ControllingButtons
from PySide6.QtCore import Qt #type: ignore
from PySide6.QtGui import QPixmap, QPalette, QBrush #type: ignore

class CycleRunningPage(QWidget):
    def __init__(self,controller,router,cycle):
        super().__init__()
        self.controller = controller
        self.router = router
        # cycle running logic

        self.cycle = None

        self.setFixedSize(1024,600)
        self.set_background("resources/cycle_running_page_assets/running_cycle.png")


        # Create main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.main_layout)


        ##timer screen needs to be linked


        #setting up widgets
        #setup for control buttons
        self.controlling_buttons = ControllingButtons()
        self.main_layout.addSpacing(40)
        self.main_layout.addWidget(self.controlling_buttons)

        self.controlling_buttons.stop_button.clicked.connect(self.router.show_home)
    def set_background(self, image_path):
        
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(image_path).scaled(
            self.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        ))
        self.bg_label.setGeometry(0, 1, self.width(), self.height())
        self.bg_label.lower()  # send to back
        
    def update_cycle(self,cycle):
        self.curr_cycle = cycle
        #placeholder
        print(f'current cycle: cycle["minutes"],cycle["seconds"]')