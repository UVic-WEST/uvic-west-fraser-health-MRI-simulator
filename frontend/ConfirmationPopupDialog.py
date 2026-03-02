from PySide6.QtWidgets import (
    QVBoxLayout, 
    QLabel, 
    QDialog, 
    QDialogButtonBox )

class CustomDialog(QDialog):
    def __init__(self, window_name: str, message: str, acceptance: str, rejection: str, angry: bool):
        
        #setup
        super().__init__()
        self.setWindowTitle(window_name)
        self.setFixedSize(600, 320)
        main_layout = QVBoxLayout()

        #in dialog box
        #message to confirm
        message = QLabel(message)

        #setting up buttons
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.Ok).setText(acceptance)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText(rejection)

        #finalizing layout
        main_layout.addWidget(message)
        main_layout.addWidget(self.buttonBox)
        self.setLayout(main_layout)

        #connecting buttons
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


        