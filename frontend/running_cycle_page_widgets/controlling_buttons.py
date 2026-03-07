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

        #setting button size to image size
        self.pause_button.setFixedSize(pause_button_pix.size())
        self.pause_button.setIcon(QIcon(pause_button_pix))
        self.pause_button.setIconSize(QSize(pause_button_pix.size()))
        self.pause_button.setStyleSheet("""
                                        
                QPushButton{background: transparent; border: none;}
                    QPushButton:pressed{
                    padding-left:2px;
                    padding-top:2px;
                }
            QPushButton:focus {
                outline: none;
                border: none;
            }""")
        self.pause_button.clicked.connect(self.pause_clicked)
        self.pause_button.setMask(pause_button_pix.mask())


        #stop button

        stop_button_pix = QPixmap(stop_button_asset_path)
        self.stop_button = QPushButton()

        
        self.stop_button.setFixedSize(stop_button_pix.size())
        self.stop_button.setIcon(QIcon(stop_button_pix))
        self.stop_button.setIconSize(QSize(stop_button_pix.size()))
        self.stop_button.setFocusPolicy(Qt.NoFocus)
        self.stop_button.setStyleSheet("""
            QPushButton{background: transparent; border: none;outline:none;}
            QPushButton:pressed{
                padding-left:2px;
                padding-top:2px;
            }
            QPushButton:focus {
                outline: none;
                border: none;
            }
        """)
        self.stop_button.clicked.connect(self.stop_clicked)
        # self.stop_button.setMask(stop_button_pix.mask())
        
          # add buttons
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)

        # **IMPORTANT:** set layout to this widget
        self.setLayout(button_layout)

    def pause_clicked(self):
        print("Pause")

    def stop_clicked(self):
        print("Stop")