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
    def __init__(self, parent=None):
        """
        This function builds the play square widget

        Args:
            parent: the parent widget for this container
        """
        #setting up widget size and main_layout
        super().__init__(parent)
        self.parent = parent
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setFixedSize(353,273)

        ## this has the current cycle id, gets updated from CyclePlayerWidget
        self.cur_cycle_id = None

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


        # for the clock icon and duration label
        clock_icon_pix = QPixmap(clock_icon_asset_path)
        clock_icon = QLabel()
        clock_icon.setStyleSheet("background: transparent;")
        clock_icon.setPixmap(clock_icon_pix)
        clock_icon.setScaledContents(True)
        clock_icon.setFixedSize(40, 40)

        self.duration_label = QLabel("")
        self.duration_label.setFont(QFont("Ubuntu", 28))
        self.duration_label.setStyleSheet("color: white; background: transparent;")
        self.duration_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        #for the cycle title at the top of the play square
        cycle_title = QLabel("Full Cycle")
        cycle_title.setFont(QFont("Ubuntu", 30))
        cycle_title.setStyleSheet("color: white; background: transparent;")
        cycle_title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        #organize widget layout

        blue_box_layout.addWidget(cycle_title, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        # Add clock icon and duration label in a horizontal layout at bottom left
        from PySide6.QtWidgets import QHBoxLayout, QWidget as QtQWidget
        clock_row = QHBoxLayout()
        clock_row.setContentsMargins(0, 0, 0, 0)
        clock_row.setSpacing(6)
        clock_row.addWidget(clock_icon)
        clock_row.addWidget(self.duration_label)
        clock_row_container = QtQWidget()
        clock_row_container.setLayout(clock_row)
        blue_box_layout.addWidget(clock_row_container, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        blue_box_layout.addWidget(cycle_play_button, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(blue_box, 0, 0, 1, 2)
        self.setLayout(main_layout)

        #connect buttons
        cycle_play_button.clicked.connect(self.cycle_play_button_pressed)

    def cycle_play_button_pressed(self):
        """
        This function triggers playback for the selected cycle

        Args:
            None
        """
        self.parent.play_selected_cycle()
        

    def update_selected_cycle(self, cycle_id):
        """
        This function updates the selected cycle from the dropdown
        and updates the duration label.
        Args:
            cycle_id: the cycle id selected by the user
        """
        self.cur_cycle_id = cycle_id
        # Try to get the duration from backend
        duration_text = ""
        if cycle_id and hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'cycle_factory'):
            try:
                cycle_obj = self.parent.parent.cycle_factory.get_cycle_by_id(cycle_id)
                duration_sec = int(round(cycle_obj.cycle_duration_ms / 1000))
                duration_text = f"{duration_sec} s"
            except Exception:
                duration_text = ""
        self.duration_label.setText(duration_text)
