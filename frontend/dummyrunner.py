import sys
from PySide6.QtWidgets import (
    QGridLayout,
    QMainWindow,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
    QApplication
)
from PySide6.QtGui import(
    QPixmap
)
from PySide6.QtCore import (
    QTimer,
    Qt
)
from TimerWidget import TimerWidget

class TimeDisplayApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Image Display")
        self.setFixedSize(1024,600)
        
        self.main_layout = QVBoxLayout()
        self.wid = TimerWidget()
        self.main_layout.addWidget(self.wid)

        self.app = QWidget()
        self.app.setLayout(self.main_layout)
        # Center the label within the window
        self.setCentralWidget(self.app)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeDisplayApp()
    window.show()
    app.exec()