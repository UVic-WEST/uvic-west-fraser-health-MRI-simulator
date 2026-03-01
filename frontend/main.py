
import sys
from router import AppRouter
from PySide6.QtWidgets import QApplication, QMainWindow

def main():
    app = QApplication(sys.argv)
    window = AppRouter()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
