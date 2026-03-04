from PySide6.QtWidgets import ( # type: ignore
    QWidget,
    QPushButton,
    QHBoxLayout
)
from PySide6.QtCore import Qt, QSize # type: ignore
from PySide6.QtGui import QPixmap, QIcon #type: ignore
from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout #type: ignore

class ControllingButtons(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(59)


        # # add buttons
        # button_layout.addWidget(self.pause_button)
        # button_layout.addWidget(self.stop_button)

        # # **IMPORTANT:** set layout to this widget
        # self.setLayout(button_layout)
        pause_button_asset_path = 'resources/cycle_running_page_assets/pause_button.png'
        stop_button_asset_path = 'resources/cycle_running_page_assets/stop_button.png'
        
        #setting up widgets
        #for the blue_box that has the play button in it
        pause_button_pix = QPixmap(pause_button_asset_path)
        self.pause_button = QPushButton()
        pause_size = pause_button_pix.width()
        self.pause_button.setFixedSize(pause_size, pause_size)
        self.pause_button.setIcon(QIcon(pause_button_pix))
        self.pause_button.setIconSize(QSize(pause_size, pause_size))
        self.pause_button.setStyleSheet("background: transparent; border: none;")


        #stop button

        stop_button_pix = QPixmap(stop_button_asset_path)
        self.stop_button = QPushButton()

        stop_size = stop_button_pix.width()
        self.stop_button.setFixedSize(stop_size,stop_size)
        self.stop_button.setIcon(QIcon(stop_button_pix))
        self.stop_button.setIconSize(QSize(stop_size,stop_size))
        self.stop_button.setStyleSheet("background: transparent; border: none;")

          # add buttons
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)

        # **IMPORTANT:** set layout to this widget
        self.setLayout(button_layout)