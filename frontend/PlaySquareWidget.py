from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout,
)
from PySide6.QtGui import (
    QPixmap,
)
from PySide6.QtCore import Qt, QSize

class PlaySquareWidget(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QGridLayout()
        self.setFixedSize(353,273)
        
        
        blue_box_pix = QPixmap('../resources/home_page_assets/blue_cycle_player.png')
        blue_box = QLabel()
        blue_box.setScaledContents(True)
        blue_box.setPixmap(blue_box_pix)
        blue_box.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(blue_box)
        
        cycle_play_button_pix = QPixmap('../resources/home_page_assets/cycle_play_button.png')
        cycle_play_button = QPushButton()
        cycle_play_button.setFixedSize(136,136)
        cycle_play_button.setIcon(cycle_play_button_pix)
        cycle_play_button.setIconSize(QSize(136,136))
        cycle_play_button.setStyleSheet(f"""
        QPushButton {{
            border: 2px solid #555;
            border-radius: {136 // 2}px;
            background-color: darkgray;
        }}
        QPushButton:hover {{
            background-color: gray;
        }}
        QPushButton:pressed {{
            border-style: inset;
            background-color: darkgray;
        }}
        """)

        main_layout.addWidget(cycle_play_button, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        cycle_play_button.clicked.connect(self.cycle_play_button_pressed)

    def cycle_play_button_pressed(self):
        #popup dialog goes here
        pass