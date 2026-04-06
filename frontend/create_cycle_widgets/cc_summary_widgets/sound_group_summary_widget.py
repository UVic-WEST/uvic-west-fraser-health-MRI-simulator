from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap,
    QIcon,
    QFont,
)

class SoundGroupSummaryWidget(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("SoundGroupSummaryWidget")
        self.setFixedSize(365, 263)
        self.setStyleSheet("""
        #SoundGroupSummaryWidget {
            background-color: #FAF5F5;
            border: 1px solid #0474BA;
            border-radius: 16px;
        }
        """)

        self.main_layout = QVBoxLayout()
        
        group_selector_button_style = """
            QPushButton {
                background-color: #0474BA;
                color: white;
                border: none;
                border-radius: 14px;
                padding: 8px 14px;
                text-align: left;
                font-family: Ubuntu;
                font-size: 18px;
            }
            QPushButton:pressed {
                background-color: #035f98;
            }
        """

        self.group_selector_button = QPushButton("Group 1")
        self.group_selector_button.setFixedSize(142,50)
        self.group_selector_button.setStyleSheet(group_selector_button_style)
        self.main_layout.addWidget(self.group_selector_button)

        self.preview_buttons_host = QWidget(self)
        self.preview_buttons_host.setStyleSheet("""
            background-color: #FAF5F5;
        """)
        self.preview_buttons_host.setFixedSize(335,130)
        self.preview_buttons_layout = QVBoxLayout()
        self.preview_buttons_host.setLayout(self.preview_buttons_layout)
        self.preview_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.preview_buttons_layout.setSpacing(8)
        self.main_layout.addWidget(self.preview_buttons_host)
        self.refresh_preview_panel_backend(None)

        self.volume_display = QPushButton("Volume: 50%")
        self.volume_display.setFixedSize(242,37)
        self.volume_display.setStyleSheet("""
            background-color: white;
            color: black;
            border: 1px solid #D3CBCB;
            border-radius: 15px;
            padding: 10px 16px;
            text-align: left;
            font-family: Ubuntu;
            font-size: 15px;
        """)
        self.volume_display.setIcon(QIcon('resources/create_cycle_assets/volume_icon.png'))
        self.main_layout.addWidget(self.volume_display)
        
        self.setLayout(self.main_layout)

    def refresh_preview_panel_backend(self, sound_names):
        for sound_name in ["1","2","3"]:
            sound_chip = QLabel(sound_name)
            sound_chip.setFont(QFont("Ubuntu", 14))
            sound_chip.setStyleSheet("""
                background-color: white;
                color: black;
                border: 1px solid #D3CBCB;
                border-radius: 15px;
                padding: 10px 16px;
                text-align: center;
                font-family: Ubuntu;
                font-size: 20px;
            """)
            sound_chip.setFixedSize(335,37)
            self.preview_buttons_layout.addWidget(sound_chip)
        self.preview_buttons_layout.addStretch(1)