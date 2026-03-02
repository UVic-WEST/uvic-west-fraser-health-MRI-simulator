
import sys
from frontend.router import AppRouter
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = AppRouter()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
