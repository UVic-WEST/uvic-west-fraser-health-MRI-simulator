from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import (
    QPixmap, 
    QFont
)
from frontend.confirmation_page_widgets.ConfirmationButtons import ConfirmationButtons

class ConfirmationPage(QWidget):
    start_cycle_requested = Signal()
    cancel_requested = Signal()

    def __init__(self,controller,cycle,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.cycle = None
        self.setFixedSize(1024,600)

        # Create main layout
        self.set_background("resources/cycle_running_page_assets/running_cycle.png")
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(self.main_layout)

        # Create white box with rounded corners
        self.content_box = QWidget()
        self.content_box.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)
        
        # Content layout inside white box
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(40)

        #setting up widgets

        #Cycle running label
        self.cycle_status = QLabel("Are you sure you want to run cycle?")
        cycle_status_font = QFont("Ubuntu", 24)
        self.cycle_status.setFont(cycle_status_font)
        self.cycle_status.setStyleSheet("color: #0474BA;")
        self.cycle_status.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.cycle_status)

        #setup for control buttons
        self.confirmation_buttons = ConfirmationButtons(self)
        self.confirmation_buttons.yes_clicked.connect(self.cycle_confirmed)
        self.confirmation_buttons.no_clicked.connect(self.cycle_cancelled)
        content_layout.addWidget(self.confirmation_buttons)
        
        self.content_box.setLayout(content_layout)
        self.main_layout.addWidget(self.content_box)
        
    def set_background(self, image_path):
        
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(image_path).scaled(
            self.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        ))
        self.bg_label.setGeometry(0, 1, self.width(), self.height())
        self.bg_label.lower()  # send to back

    # using the signals created for cycle running page
    def cycle_cancelled(self):
        self.cancel_requested.emit()

    # using the signals created for cycle running page
    def cycle_confirmed(self):
        self.start_cycle_requested.emit()