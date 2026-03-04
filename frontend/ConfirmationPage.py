from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap, 
    QFont
)

class ConfirmationPage(QWidget):
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
        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)
        button_layout.setAlignment(Qt.AlignCenter)
        
        # No button (red)
        self.no_button = QPushButton("NO")
        self.no_button.setFixedSize(120, 60)
        self.no_button.setFont(QFont("Ubuntu", 16, QFont.Bold))
        self.no_button.setStyleSheet("""
            QPushButton {
                background-color: #EC221F;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d41810;
            }
            QPushButton:pressed {
                background-color: #b01208;
            }
        """)
        self.no_button.clicked.connect(self.cycle_completed)
        
        # Yes button (green)
        self.yes_button = QPushButton("YES")
        self.yes_button.setFixedSize(120, 60)
        self.yes_button.setFont(QFont("Ubuntu", 16, QFont.Bold))
        self.yes_button.setStyleSheet("""
            QPushButton {
                background-color: #00AA00;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #008800;
            }
            QPushButton:pressed {
                background-color: #006600;
            }
        """)
        self.yes_button.clicked.connect(self.cycle_confirmed)
        
        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)
        content_layout.addLayout(button_layout)
        
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

    def cycle_completed(self):
        self.parent.show_home()

    def cycle_confirmed(self):
        self.parent.play_cycle_confirmed()

    def cycle_ended(self):
        self.parent.show_home()

    def update_cycle(self,cycle):
        self.curr_cycle = cycle
        #placeholder
        print(f'current cycle: cycle["minutes"],cycle["seconds"]')