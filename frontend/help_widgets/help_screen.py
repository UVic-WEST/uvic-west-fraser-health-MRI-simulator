from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QPainter, QColor
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView


class HelpOverlay(QWidget):
    # Class-level registry to track all HelpOverlay instances
    _instances = []

    def __init__(self, path, parent=None):
        """
        The HelpOverlay reveals the relevant manual as a pdf over the current screen/widget
        Args:
            path (str): path to the relevant manual pdf in reference to the project root
            parent (QWidget): parent object of this widget
        """
        super().__init__(parent)
        self.setFixedSize(1024,600)
        
        # Register this instance
        HelpOverlay._instances.append(self)
        
        if path is None:
            path = "resources/manuals/sample_manual.pdf"

        self.hide()

        self.return_button = QPushButton("Return",self)
        self.return_button.setStyleSheet("""
            background-color: #FFA630;
            border-radius: 20px;
            font: 24px 'Ubuntu';
        """)
        self.return_button.setFixedSize(200,53)
        self.return_button.clicked.connect(self.return_pressed)
        self.return_button.move(50,40)

        # Set up document
        self.pdf_document = QPdfDocument()
        self.pdf_document.load(path)

        self.pdf_view = QPdfView(self)
        self.pdf_view.setDocument(self.pdf_document)
        self.pdf_view.setFixedSize(700,600)
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.pdf_view.setZoomFactor(0.7)
        self.pdf_view.move(290,40)

    def return_pressed(self):
        """
        Hides the help overlay when return is pressed
        """
        self.hide()

    @classmethod
    def hide_all(cls):
        """
        Hides all active HelpOverlay instances. Called when estop is pressed.
        """
        for instance in cls._instances:
            if instance is not None and instance.isVisible():
                instance.hide()

    def paintEvent(self, event):
        """
        paints the background so that the background is greyed out
        """
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 140))