from PySide6.QtWidgets import( # type: ignore
    QWidget,
    QVBoxLayout,
    QLabel
)

from frontend.home_page_widgets.TimeDisplayWidget import TimeDisplayWidget
from frontend.home_page_widgets.ControllingButtons import ControllingButtons
from PySide6.QtCore import Qt #type: ignore
from PySide6.QtGui import QPixmap, QPalette, QBrush #type: ignore

class CycleRunningPage(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setFixedSize(842,445)
        self.set_background("resources/cycle_running_page_assets/running_cycle.png")


        # Create main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.main_layout)


        #setting up widgets
        #setup for time display screen
        self.time_display_screen = TimeDisplayWidget()
        self.main_layout.addSpacing(60)
        self.main_layout.addWidget(self.time_display_screen)


        #setting up widgets
        #setup for control buttons
        self.controlling_buttons = ControllingButtons()
        self.main_layout.addSpacing(-20)
        self.main_layout.addWidget(self.controlling_buttons)


    def set_background(self, image_path):
        
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(image_path).scaled(
            self.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        ))
        self.bg_label.setGeometry(0, 1, self.width(), self.height())
        self.bg_label.lower()  # send to back
        # pixmap = QPixmap(image_path)
        # palette = QPalette()
        # palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(
        #     self.size(), 
        #     Qt.IgnoreAspectRatio, 
        #     Qt.SmoothTransformation
        # )))
        # self.setPalette(palette)
        # self.setAutoFillBackground(True)



        #setting up timer screen
