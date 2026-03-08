from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout,
)
from PySide6.QtGui import (
    QPixmap,
    QIcon,
    QFont,
)
from PySide6.QtCore import (
    Qt, 
    QSize
) 
from frontend.helpers import make_button_circle

class PlaySquareWidget(QWidget):
    '''
    GUI implementation for the blue box that is on the homepage which plays a cycle.
    '''
    def __init__(self, parent=None):
        #setting up widget size and main_layout
        super().__init__(parent)
        self.parent = parent
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setFixedSize(353,273)

        ## this has the current cycle information, gets updated from CycleplayerWidget
        self.cur_cycle = None

        #asset paths
        play_button_asset_path = 'resources/home_page_assets/cycle_play_button.png'
        clock_icon_asset_path = 'resources/frontend_common_assets/whiteclockicon.png'
        
        #setting up widgets
        #for the blue_box that has the play button in it
        blue_box = QWidget()
        blue_box.setAttribute(Qt.WA_StyledBackground, True)
        blue_box.setStyleSheet("""
            QWidget {
                background-color: #0474BA;
                border-radius: 12px;
            }
        """)

        # Keep icon/button on top of the blue box so transparent pixels show blue, not page white.
        blue_box_layout = QGridLayout(blue_box)
        blue_box_layout.setContentsMargins(12, 6, 12, 12)
        blue_box_layout.setSpacing(0)
        
        #for the actual play button to press the cycle
        cycle_play_button_pix = QPixmap(play_button_asset_path)
        cycle_play_button = QPushButton()
        cycle_play_button_size = cycle_play_button_pix.width()

        cycle_play_button.setFixedSize(cycle_play_button_size,cycle_play_button_size)
        cycle_play_button.setIcon(QIcon(cycle_play_button_pix))
        cycle_play_button.setIconSize(QSize(cycle_play_button_size,cycle_play_button_size))
        make_button_circle(cycle_play_button,cycle_play_button_size)

        #for the clock icon
        clock_icon_pix = QPixmap(clock_icon_asset_path)
        clock_icon = QLabel()
        clock_icon.setStyleSheet("background: transparent;")
        clock_icon.setPixmap(clock_icon_pix)
        clock_icon.setScaledContents(True)
        clock_icon.setFixedSize(40, 40)

        #for the cycle title at the top of the play square
        cycle_title = QLabel("Full Cycle")
        cycle_title.setFont(QFont("Ubuntu", 30))
        cycle_title.setStyleSheet("color: white; background: transparent;")
        cycle_title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        #organize widget layout
        blue_box_layout.addWidget(cycle_title, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        blue_box_layout.addWidget(clock_icon, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        blue_box_layout.addWidget(cycle_play_button, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(blue_box, 0, 0, 1, 2)
        self.setLayout(main_layout)

        #connect buttons
        cycle_play_button.clicked.connect(self.cycle_play_button_pressed)

    def cycle_play_button_pressed(self):
        '''
        cycle_name = self.cur_cycle.name if self.cur_cycle else "a cycle"
        self.play_cycle_confirmation = ConfirmationPopupDialog("Confirmation", f"Are you sure you want to start {cycle_name}?", "Start Cycle", "Cancel", False)
        if self.play_cycle_confirmation.exec():
            pass 
            #this should emit signal to cycleplayer -> homepage to open cycle running page
        '''
        self.parent.play_selected_cycle()
        

    def update_selected_cycle(self, new_cycle):
        self.cur_cycle = new_cycle
