import os
import sys
from frontend.app_router import AppRouter
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView

# The UI is laid out in fixed pixels for this design size (see setFixedSize calls in frontend/).
DESIGN_WIDTH = 1024
DESIGN_HEIGHT = 600


class ScaledView(QGraphicsView):
    """
    Full-screen host that scales the fixed-size AppRouter to fit any display resolution,
    keeping the aspect ratio. Mouse/touch input is mapped through the same transform,
    so clicks land on the buttons they visually hit.
    """

    def __init__(self, window):
        super().__init__()
        self._window = window
        scene = QGraphicsScene(0, 0, DESIGN_WIDTH, DESIGN_HEIGHT, self)
        scene.setBackgroundBrush(QColor("black"))
        self.setScene(scene)
        # Qt.Widget keeps the main window from being decorated as a separate top-level window
        self._proxy = scene.addWidget(window, Qt.Widget)
        self._proxy.setPos(0, 0)

        self.setFrameShape(QGraphicsView.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QColor("black"))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)


def main():
    app = QApplication(sys.argv)
    window = AppRouter()
    view = ScaledView(window)
    view.showFullScreen()
    app.exec()

if __name__ == '__main__':
    main()
