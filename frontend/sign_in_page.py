from PySide6.QtWidgets import(
    QWidget,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QPushButton
)
from PySide6.QtGui import QFont, Qt, QPixmap
from frontend.sign_in_page_widgets.pinpad_widget import PinPad

MAX_PASSWORD_INPUT = 4
MAX_PASSWORD_ATTEMPTS = 3

## DELETE LATER THIS IS A DUMMY PASSWORD TO GET INTO THE SYSTEM
PASS_TEMP = '2026'

class SignInPage(QWidget):
    def __init__(self, controller, parent=None):
        """
        This is the sign in page for the application. Handles user pin/sign in before the user gains access to the system.
        
        Args:
            controller (signInPageLogic): controller that handles the backend logic for sign in page
            parent (AppRouter): parent that creates/initializes this class
        """
        #page setup
        super().__init__(parent)
        self.parent = parent
        self.login_controller = controller

        #password management
        self.current_entry = ""
        self.password_attempts = 0

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
        self.input_box = QLabel("", self)
        self.input_box.setFont(QFont("Ubuntu",40))
        self.input_box.setFixedSize(341, 77) 
        self.input_box.setStyleSheet("""
            background-color: white;
            color: #676363;
            border: 3px solid black;
            border-radius: 24px;
            qproperty-alignment: AlignCenter;
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
            QPushButton:pressed {
                background-color: #0A6AA6;
                color: #E9E1E1;
                border: 3px solid #0474BA;
                }
        """)
        self.enter_button.move(130,293)
        self.enter_button.clicked.connect(self.enter_pressed)

        self.pinpad = PinPad(self)
        self.pinpad.pinpad_pressed.connect(self.update_entry)
        self.pinpad.move(567,41)

    def update_entry(self, pin:str):

        if pin == "clr":
            self.clr_password_input()
        elif pin == "del":
            self.del_pressed()
        elif len(self.current_entry) == MAX_PASSWORD_INPUT:
            return   
        else:
            self.current_entry += pin
        
        self.input_box.setText("*"*len(self.current_entry))

        print(self.current_entry)
        
    def clr_password_input(self):
        self.current_entry = ""
        self.input_box.setText("*"*len(self.current_entry))

    def del_pressed(self):
        self.current_entry = self.current_entry[0:len(self.current_entry)-1]
        
    def enter_pressed(self):
        if len(self.current_entry) < 4:
            return
        
        if self.current_entry == PASS_TEMP:
            self.login_successful()
        else: 
            self.update_password_attempts()

        self.clr_password_input()

    def login_successful(self):
        self.parent.show_home()
        self.clr_password_input()
        self.password_attempts = 0

    def update_password_attempts(self):
        self.password_attempts += 1

        if self.password_attempts == MAX_PASSWORD_ATTEMPTS:
            self.parent.timeout_signin()
            self.password_attempts = 0

