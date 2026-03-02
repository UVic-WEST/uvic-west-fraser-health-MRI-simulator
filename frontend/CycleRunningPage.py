from PySide6.QtWidgets import(
    QWidget
)
class CycleRunningPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller