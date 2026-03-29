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

        self.parent = parent
        button_layout = QHBoxLayout()
        button_layout.setSpacing(59)
        #if this is set to false, then PAUSE button is currently being displayed
        self.cycle_paused = False 


        # # **IMPORTANT:** set layout to this widget
        self.pause_button_asset_path = 'resources/cycle_running_page_assets/pause_button.png'
        self.stop_button_asset_path = 'resources/cycle_running_page_assets/stop_button.png'
        self.resume_button_asset_path = 'resources/cycle_running_page_assets/Resume_Button.png'
        
        #setting up widgets
        #pause button
        self.pause_resume_button = QPushButton() 
        pause_button_pix = QPixmap(self.pause_button_asset_path)
        self.pause_resume_button.setFixedSize(pause_button_pix.size())
        self.pause_resume_button.setIcon(QIcon(pause_button_pix))
        self.pause_resume_button.setIconSize(QSize(pause_button_pix.size()))
        self.pause_resume_button.setStyleSheet("""
                QPushButton{background: transparent; border: none;}
                    QPushButton:pressed{
                    padding-left:2px;
                    padding-top:2px;
                }
            QPushButton:focus {
                outline: none;
                border: none;
            }""")
        self.pause_resume_button.clicked.connect(self.pause_resume_clicked)
        self.pause_resume_button.setMask(pause_button_pix.mask())

        #stop button setup.

        stop_button_pix = QPixmap(self.stop_button_asset_path)
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
        button_layout.addWidget(self.pause_resume_button)
        button_layout.addWidget(self.stop_button)

        # **IMPORTANT:** set layout to this widget
        self.setLayout(button_layout)

    def pause_resume_clicked(self):
        if self.cycle_paused:
            self.set_pause_button()
            self.parent.resume_cycle()
        else:
            self.set_resume_button()
            self.parent.pause_cycle()

    def stop_clicked(self):
        self.parent.stop_cycle()
        self.set_pause_button()
        print("Stop")

    def set_pause_button(self):

        self.cycle_paused = False

        #setting button size to image size
        pause_button_pix = QPixmap(self.pause_button_asset_path)
        self.pause_resume_button.setIcon(QIcon(pause_button_pix))
        self.pause_resume_button.setIconSize(QSize(pause_button_pix.size()))

    def set_resume_button(self):

        self.cycle_paused = True
        #setting button size to image size
        resume_button_pix = QPixmap(self.resume_button_asset_path)
        self.pause_resume_button.setIcon(QIcon(resume_button_pix))
        self.pause_resume_button.setIconSize(QSize(resume_button_pix.size()))

    