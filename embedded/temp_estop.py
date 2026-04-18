from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QMainWindow,
    QVBoxLayout,
)

class TempEstop(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.estop_active = False
        self.setWindowTitle("Temporary E-Stop")
        self.setFixedSize(240, 140)

        root = QWidget(self)
        layout = QVBoxLayout(root)

        self.estop_button = QPushButton("E-STOP", root)
        self.estop_button.setStyleSheet(
            "color: black; background-color: red;"
        )
        self.estop_button.setFixedSize(100,100)
        self.estop_button.clicked.connect(self.estop_pressed)
        layout.addWidget(self.estop_button)

        self.setCentralWidget(root)
        self.show()

    def estop_pressed(self):
        self.estop_active = not self.estop_active
        if self.parent is not None:
            self.parent.estop_event(self.estop_active)