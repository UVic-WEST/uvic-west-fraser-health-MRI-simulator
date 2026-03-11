from PySide6.QtWidgets import(
    QWidget,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QPushButton
)
from PySide6.QtGui import QFont, Qt, QPixmap

class SignInPage(QWidget):
    def __init__(self, controller, parent=None):
        """
        This is the sign in page for the application. Handles user pin/sign in before the user gains access to the system.
        
        Args:
            controller (signInPageLogic): controller that handles the backend logic for sign in page
            parent (AppRouter): parent that creates this class
        """
        #page setup
        super().__init__(parent)
        self.parent = parent
        #self.setStyleSheet("background: grey;")
        self.main_layout = QVBoxLayout()
        self.left_layout = QVBoxLayout()

        #fraser logo
        fraser_logo_path = 'resources/frontend_common_assets/west_logo.png'
        fraser_logo_pix = QPixmap(fraser_logo_path)
        self.fraser_logo = QLabel(self)
        self.fraser_logo.setFixedSize(94, 77)
        self.fraser_logo.setPixmap(fraser_logo_pix)
        self.fraser_logo.move(0,0)

        #enter pin label
        self.enter_pin_label = QLabel("Enter Pin",self)
        self.enter_pin_label.setFixedSize(341,63)
        self.enter_pin_label.setStyleSheet(
            "color: black;")
        self.enter_pin_label.setFont(QFont("Ubuntu", 50))
        #self.left_layout.addWidget(self.enter_pin_label)
        self.enter_pin_label.move(170,112)

        #password input box label
        self.input_box = QLabel("text here", self)
        self.input_box.setFixedSize(341, 77) 
        self.input_box.setStyleSheet("""
            background-color: white;
            color: #676363;
            border: 3px solid black;
            border-radius: 24px;
        """)
        self.input_box.move(135,185)

        #enter button
        self.enter_button = QPushButton("Enter",self)
        self.enter_button.setFixedSize(351,100)
        self.enter_button.setFont(QFont("Ubuntu", 50))
        self.enter_button.setStyleSheet("""
            QPushButton {
                background-color: #0474BA;
                color: white;
                border: 3px solid #00A7E1;
                border-radius: 24px
            }
        """)
        self.enter_button.move(130,293)

        #self.main_layout.addLayout(self.left_layout)
        self.setLayout(self.left_layout)