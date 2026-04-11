from PySide6.QtWidgets import(
    QWidget,
    QGridLayout,
    QPushButton,
)

from PySide6.QtCore import (
    Signal,
)

from PySide6.QtGui import QFont, Qt, QPixmap, QFont

class PinPad(QWidget):

    pinpad_pressed = Signal(str)

    def __init__(self, parent=None):
        """
        This widget is the pinpad for the sign in page, which sends its input to the SignInPage class via signals.

        Args:
            parent (SignInPage/QWidget): the parent widget of this widget
        """
        super().__init__(parent)
        self.parent = parent
        self.setFixedSize(370,498)
        self.buttons = []

        #styling the pinpad
        self.setObjectName("PinPad")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            QWidget#PinPad {
                background-color: white;
                border-radius: 20;
            }
        """)
        self.main_layout = QGridLayout()
        self.main_layout.setHorizontalSpacing(9)
        self.main_layout.setVerticalSpacing(12)

        #create buttons and organize them as a grid on widget
        self.create_buttons()

        horiz_butn_index = 0
        vert_butn_index = 0
        for butn in self.buttons:
            self.main_layout.addWidget(butn,vert_butn_index,horiz_butn_index)
            horiz_butn_index = (horiz_butn_index+1)%3
            if horiz_butn_index == 0:
                vert_butn_index += 1
        
        self.setLayout(self.main_layout)

    def set_button_dimensions(self,button:QPushButton):
            """
            sets all of the initialized pinpad buttons to the necessary size and style

            Args:
                button (QPushButton): button to be changed
            """
            button.setFixedSize(109,109)
            button.setStyleSheet("""
            QPushButton{
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
            """
            )
            button.setFont(QFont("Ubuntu", 43))

    def create_buttons(self):
        """
        creates the buttons for the pinpad and saves them to the list of buttons for this class, this function also sets up their signal connections.
        """
        for digit in range(1,13):
            
            pin = str(digit)

            if pin == '10':
                pin = "del"
            elif pin == '11':
                pin = '0'
            elif pin == '12':
                pin = 'clr'

            button = QPushButton(pin)
            self.set_button_dimensions(button)
            button.clicked.connect(lambda checked=False, p=pin: self.pinpad_pressed.emit(p))
            self.buttons.append(button)