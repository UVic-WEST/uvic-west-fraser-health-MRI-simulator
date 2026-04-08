import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QLabel, QFrame
)
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QPainter, QColor
from PySide6.QtPdf import QPdfPageRenderer, QPdfDocument
from PySide6.QtPdfWidgets import QPdfView


class HelpOverlay(QWidget):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        
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
        self.pdf_view.setFixedSize(700,800)
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.pdf_view.setZoomFactor(0.7)
        self.pdf_view.move(290,40)

    def return_pressed(self):
        self.hide()

    def showEvent(self, event):
        super().showEvent(event)
        self.resize(self.parent().size())

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 140))

