from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QAbstractItemView,
    QScroller

)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap,
    QIcon,
    QFont,
)

from frontend.help_widgets.help_screen import HelpOverlay
from frontend.help_widgets.help_button import HelpButton

from frontend.running_cycle_page_widgets.sound_group_summary_widget import SoundGroupSummaryWidgetPreviewPage

class CyclePreviewPage(QWidget):
    def __init__(self, cycle, parent=None):
        """
        Build the summary page UI and bind controls for final review/edit flow.

        Args:
            cycle (CycleConfig): cycle to display preview of
            parent (QWidget): parent widget/router for navigation callbacks
        """
        super().__init__(parent)
        self.parent = parent
        self.cur_cycle = cycle

        self.total_groups = self.cur_cycle.get_total_groups()
        self.brightness = self.cur_cycle.get_brightness()
        self.duration = self.cur_cycle.get_duration_sec()
        self.cycle_name = self.cur_cycle.get_cycle_name()
        self.sound_group_mapping = self.cur_cycle.get_sound_group_mapping()

        self.setFixedSize(1024, 600)

        self.set_background("resources/cycle_running_page_assets/running_cycle.png")
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(40, 0, 40, 16)
        self.main_layout.setSpacing(4)
        self.setLayout(self.main_layout)

        self.help_manual_path = None
        self.help_overlay = HelpOverlay(self.help_manual_path,self)

        #setting up help button
        self.help_button = HelpButton(self)
        self.help_button.move(140, 20)
        self.help_button.raise_()
        self.help_button.clicked.connect(self.help_pressed)

        self.play_cycle_btn = QPushButton("Play Cycle", self)
        self.play_cycle_btn.setGeometry(884, 536, 125, 44)
        self.play_cycle_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #14AE5C;
                color: white;
                border: none;
                border-radius: 22px;
                font-family: Ubuntu;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #0474BA;
            }
            QPushButton:pressed {
                background-color: #035f98;
            }
            """
        )
        self.play_cycle_btn.clicked.connect(self.play_cycle_button_pressed)
        self.play_cycle_btn.raise_()

        self.cancel_home_btn = QPushButton("Cancel", self)
        self.cancel_home_btn.setGeometry(752, 536, 120, 44)
        self.cancel_home_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #FFA630;
                color: white;
                border: none;
                border-radius: 22px;
                font-family: Ubuntu;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #FFA630;
            }
            QPushButton:pressed {
                background-color: #FF8410;
            }
            """
        )
        self.cancel_home_btn.clicked.connect(self.cancel_to_home)
        self.cancel_home_btn.raise_()
        
        self.page_title = QLabel(f"Play {self.cycle_name}?")
        self.page_title.setFont(QFont("Ubuntu", 32))
        self.page_title.setStyleSheet("color: white; background: transparent; padding: 0px; margin: 0px;")
        self.page_title.setAlignment(Qt.AlignCenter)
        self.page_title.setFixedHeight(46)
        self.page_title.setContentsMargins(0, 0, 0, 0)

        self.title_layout = QVBoxLayout()
        self.title_layout.setSpacing(0)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.addWidget(self.page_title)
        self.main_layout.addLayout(self.title_layout)

        self.content_box = QWidget()
        self.content_box.setObjectName("contentBox")
        self.content_box.setStyleSheet("""
        #contentBox {
        background-color: white;
        border-radius: 15px;
        }
        """)
        self.content_box.setFixedSize(700, 320)

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setContentsMargins(18,18,18,18)
        content_layout.setSpacing(16)

        duration_summary_btn_icon = 'resources/create_cycle_assets/clock_icon.png'
        self.duration_summary_btn = QPushButton("Cycle Duration: --:--", self)
        self.set_up_remapping_buttons(self.duration_summary_btn, duration_summary_btn_icon)

        lights_summary_btn_icon = 'resources/create_cycle_assets/brightness_icon.png'
        self.lights_summary_btn = QPushButton("Cycle Lights: --%")
        self.set_up_remapping_buttons(self.lights_summary_btn, lights_summary_btn_icon)

        groups_summary_btn = 'resources/create_cycle_assets/group_icon.png'
        self.groups_summary_btn = QPushButton("Total Groups: --")
        self.set_up_remapping_buttons(self.groups_summary_btn, groups_summary_btn)

        self.preview_panel = SoundGroupSummaryWidgetPreviewPage(self.sound_group_mapping, self)

        content_layout.addWidget(self.duration_summary_btn)
        content_layout.addWidget(self.lights_summary_btn)
        content_layout.addWidget(self.groups_summary_btn)

        mapping_layout = QVBoxLayout()
        mapping_layout.addWidget(self.preview_panel)
        mapping_layout.setContentsMargins(18,18,18,18)

        overall_layout = QHBoxLayout()
        overall_layout.addLayout(mapping_layout)
        overall_layout.addLayout(content_layout)

        self.content_box.setLayout(overall_layout)
        self.main_layout.addWidget(self.content_box)
        self._update_summary_buttons()

    def help_pressed(self):
        """
        Shows the help screen overlay for this page
        """
        self.help_overlay.show()
        self.help_overlay.raise_()

    def _update_summary_buttons(self):
        """
        Refreshes summary button labels from backend controller values.
        """
        self._update_duration_summary_button()
        self._update_lights_summary_button()
        self._update_groups_summary_button()
        if hasattr(self, "preview_panel") and hasattr(self.preview_panel, "refresh_from_backend"):
            self.preview_panel.refresh_from_backend()

    def _update_duration_summary_button(self):
        """
        Reads duration from backend controller and updates the summary button label.
        """
        duration_text = "--:--"
        if hasattr(self.cur_cycle, "get_duration"):
            try:
                total_seconds = int(self.duration)
                minutes, seconds = divmod(max(0, total_seconds), 60)
                duration_text = f"{minutes:02}:{seconds:02}"
            except Exception as e:
                print(f"[_update_duration_summary_button] Error: {e}")

        self.duration_summary_btn.setText(f"Cycle Duration: {duration_text}")

    def _update_lights_summary_button(self):
        """
        Reads light level from backend controller and updates the summary button label.
        """
        lights_text = "--"
        if hasattr(self.cur_cycle, "get_light_level"):
            try:
                lights_text = str(int(self.brightness))
            except Exception as e:
                print(f"[_update_lights_summary_button] Error: {e}")

        self.lights_summary_btn.setText(f"Cycle Lights: {lights_text}%")

    def _update_groups_summary_button(self):
        """
        Reads total groups from backend controller and updates the summary button label.
        """
        groups_text = "--"
        if hasattr(self.cur_cycle, "get_total_groups"):
            try:
                total_groups, _ = self.total_groups
                groups_text = str(int(total_groups))
            except Exception as e:
                print(f"[_update_groups_summary_button] Error: {e}")

        self.groups_summary_btn.setText(f"Total Groups: {groups_text}")

    def set_background(self, image_path):
        """
        Set the page background image.

        Args:
            image_path: path to the background asset
        """
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(
            QPixmap(image_path).scaled(
                self.size(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation,
            )
        )
        self.bg_label.setGeometry(0, 1, self.width(), self.height())
        self.bg_label.lower()

    def cancel_to_home(self):
        """
        Cancel customization and navigate back to the home page.
        """
        print("cancel was pressed")
        current = self.parent
        while current is not None:
            if hasattr(current, "show_home"):
                current.show_home()
                return
            if hasattr(current, "parent"):
                current = current.parent()
            else:
                current = None

    def set_up_remapping_buttons(self, button, path):
        """
        Apply shared styling/icon setup for summary remapping buttons.

        Args:
            button: button instance to style
            path: icon asset path
        """
        summary_button_style = """
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
        button.setFixedHeight(48)
        button.setFixedSize(242, 47.67)
        button.setStyleSheet(summary_button_style)
        button.setIcon(QIcon(path))

    def play_cycle_pressed(self):
        """
        confirms that the cycle is to play, begins running cycle
        """
        pass