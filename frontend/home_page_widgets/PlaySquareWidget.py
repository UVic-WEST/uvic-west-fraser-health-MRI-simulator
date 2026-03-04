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
from frontend.helpers import make_button_circle
from frontend.ConfirmationPopupDialog import ConfirmationPopupDialog

class PlaySquareWidget(QWidget):
    '''
    GUI implementation for the blue box that is on the homepage which plays a cycle.
    '''
    def __init__(self, parent=None):
        #setting up widget size and main_layout
        super().__init__(parent)
        main_layout = QGridLayout()
        self.setFixedSize(353,273)

        ## this has the current cycle information, gets updated from CycleplayerWidget
        self.cur_cycle = None

        #asset paths
        blue_box_asset_path = 'resources/home_page_assets/blue_cycle_player.png'
        play_button_asset_path = 'resources/home_page_assets/cycle_play_button.png'
        
        #setting up widgets
        #for the blue_box that has the play button in it
        blue_box_pix = QPixmap(blue_box_asset_path)
        blue_box = QLabel()
        blue_box.setScaledContents(True)
        blue_box.setPixmap(blue_box_pix)
        blue_box.setAlignment(Qt.AlignCenter)

        
        #for the actual play button to press the cycle
        cycle_play_button_pix = QPixmap(play_button_asset_path)
        cycle_play_button = QPushButton()
        cycle_play_button_size = cycle_play_button_pix.width()

        cycle_play_button.setFixedSize(cycle_play_button_size,cycle_play_button_size)
        cycle_play_button.setIcon(cycle_play_button_pix)
        cycle_play_button.setIconSize(QSize(cycle_play_button_size,cycle_play_button_size))
        make_button_circle(cycle_play_button,cycle_play_button_size)

        #organize widget layout
        main_layout.addWidget(blue_box)
        main_layout.addWidget(cycle_play_button, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        #connect buttons
        cycle_play_button.clicked.connect(self.cycle_play_button_pressed)

    def cycle_play_button_pressed(self):
        cycle_name = self.cur_cycle.name if self.cur_cycle else "a cycle"
        self.play_cycle_confirmation = ConfirmationPopupDialog("Confirmation", f"Are you sure you want to start {cycle_name}?", "Start Cycle", "Cancel", False)
        if self.play_cycle_confirmation.exec():
            pass 
            #this should emit signal to cycleplayer -> homepage to open cycle running page

    def update_selected_cycle(self, new_cycle):
        self.cur_cycle = new_cycle
