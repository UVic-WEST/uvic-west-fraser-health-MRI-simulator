from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap, 
    QFont
)
from frontend.warning_page_widgets.confirmation_buttons import WarningButtons

class WarningPage(QWidget):

    def __init__(self, parent=None):
        """
        This function builds the warning page shown before custom cycle creation

        Args:
            parent: the parent widget for this page
        """
        super().__init__(parent)
        self.parent = parent
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
        content_layout.setSpacing(10)

        #setting up widgets

        # warning label
        self.warning_status = QLabel("WARNING!\n REMOVE CHILD FROM MRI\n BEFORE PROCEEDING")
        cycle_status_font = QFont("Ubuntu", 24)
        cycle_status_font.setBold(True)
        self.warning_status.setFont(cycle_status_font)
        self.warning_status.setStyleSheet("color: #000000;")
        self.warning_status.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.warning_status)

        #setup for control buttons
        self.warning_buttons = WarningButtons(self)
        self.warning_buttons.confirm_clicked.connect(self.warning_confirmed)
        self.warning_buttons.cancel_clicked.connect(self.warning_cancelled)
        content_layout.addWidget(self.warning_buttons)
        
        self.content_box.setLayout(content_layout)
        self.main_layout.addWidget(self.content_box)

    def set_background(self, image_path):
        """
        This sets the background of the page

        Args:
            image_path (str): path to the asset for the background image
        """
        
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(image_path).scaled(
            self.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        ))
        self.bg_label.setGeometry(0, 1, self.width(), self.height())
        self.bg_label.lower()  # send to back

    def warning_cancelled(self):
        """
        This function emits cancel when warning is dismissed
        """
        self.parent.show_home()

    def warning_confirmed(self):
        """
        This function emits proceed when warning is accepted
        """
        self.parent.show_create_cycle_pages()