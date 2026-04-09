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

class SoundGroupSummaryWidgetPreviewPage(QWidget):
    def __init__(self, sound_group_mapping, parent=None):
        """
        Build the summary sound map box with group navigation and per-group preview.

        Args:
            cycle (CycleConfig): cycle to display preview of
            parent (QWidget): parent summary page widget
        """
        super().__init__(parent)
        self.sound_group_mapping = sound_group_mapping
        self.current_group_index = 1
        self.total_groups = len(sound_group_mapping)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("SoundGroupSummaryWidget")
        self.setFixedSize(365, 267)
        self.setStyleSheet("""
        #SoundGroupSummaryWidget {
            background-color: #FAF5F5;
            border: 1px solid #0474BA;
            border-radius: 16px;
        }
        """)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        
        group_selector_button_style = """
            QPushButton {
                background-color: #0474BA;
                color: white;
                border: none;
                border-radius: 14px;
                padding: 8px 14px;
                text-align: center;
                font-family: Ubuntu;
                font-size: 18px;
            }
        """

        arrow_button_style = """
            QPushButton {
                background: transparent;
                color: #0474BA;
                border: none;
                font-family: Ubuntu;
                font-size: 28px;
                font-weight: 700;
            }
            QPushButton:pressed {
                color: #035f98;
            }
            QPushButton:disabled {
                color: #A8A8A8;
            }
        """

        self.group_header_layout = QHBoxLayout()
        self.group_header_layout.setContentsMargins(0, 0, 0, 0)
        self.group_header_layout.setSpacing(18)

        self.prev_group_btn = QPushButton("<")
        self.prev_group_btn.setFixedSize(24, 50)
        self.prev_group_btn.setStyleSheet(arrow_button_style)
        self.prev_group_btn.clicked.connect(self._select_previous_group)

        self.group_selector_button = QPushButton("Group 1")
        self.group_selector_button.setFixedSize(142,46)
        self.group_selector_button.setStyleSheet(group_selector_button_style)
        self.group_selector_button.setEnabled(False)

        self.next_group_btn = QPushButton(">")
        self.next_group_btn.setFixedSize(24, 50)
        self.next_group_btn.setStyleSheet(arrow_button_style)
        self.next_group_btn.clicked.connect(self._select_next_group)

        self.group_header_layout.addWidget(self.prev_group_btn)
        self.group_header_layout.addWidget(self.group_selector_button)
        self.group_header_layout.addWidget(self.next_group_btn)
        self.group_header_layout.setAlignment(Qt.AlignHCenter)
        self.main_layout.addLayout(self.group_header_layout)

        self.preview_buttons_host = QWidget(self)
        self.preview_buttons_host.setStyleSheet("""
            background-color: #FAF5F5;
        """)
        self.preview_buttons_host.setFixedSize(335,136)
        self.preview_buttons_layout = QVBoxLayout()
        self.preview_buttons_host.setLayout(self.preview_buttons_layout)
        self.preview_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.preview_buttons_layout.setSpacing(4)
        self.main_layout.addWidget(self.preview_buttons_host)

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
        self.refresh_preview_panel_backend()
        self._update_group_controls()

    def _update_group_controls(self):
        """Refresh group label and arrow enabled states based on current index."""
        if self.current_group_index > self.total_groups:
            self.current_group_index = self.total_groups
        self.group_selector_button.setText(f"Group {self.current_group_index}")
        self.prev_group_btn.setEnabled(self.current_group_index > 1)
        self.next_group_btn.setEnabled(self.current_group_index < self.total_groups)

    def _group_id(self):
        """Return the currently selected group id."""
        return self.current_group_index

    def _get_sound_labels_for_group(self, group_id):
        """Return the names of sounds by group id"""
        labels = self.sound_group_mapping.get(group_id, {}).get("sound_names", [])
        return labels

    def _get_group_volume_for_group(self, group_id):
        """Return the current volume for the given group"""
        return self.sound_group_mapping.get(group_id, {}).get("volume")

    def _clear_preview_panel(self):
        """Remove all existing sound preview widgets from the panel."""
        while self.preview_buttons_layout.count():
            item = self.preview_buttons_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _select_previous_group(self):
        """Move selection to the previous group and refresh the preview."""
        if self.current_group_index > 1:
            self.current_group_index -= 1
        self.refresh_preview_panel_backend()
        self._update_group_controls()

    def _select_next_group(self):
        """Move selection to the next group and refresh the preview."""
        if self.current_group_index < self.total_groups:
            self.current_group_index += 1
        self.refresh_preview_panel_backend()
        self._update_group_controls()


    def refresh_preview_panel_backend(self):
        """Render sound chips and volume text for the currently selected group."""
        self._clear_preview_panel()
        current_group_id = self._group_id()
        sound_names = self._get_sound_labels_for_group(current_group_id)

        for sound_name in sound_names:
            sound_chip = QLabel(sound_name)
            sound_chip.setFont(QFont("Ubuntu", 14))
            sound_chip.setAlignment(Qt.AlignCenter)
            sound_chip.setStyleSheet("""
                background-color: white;
                color: black;
                border: 1px solid #D3CBCB;
                border-radius: 15px;
                padding: 10px 16px;
                text-align: center;
                font-family: Ubuntu;
                font-size: 18px;
            """)
            sound_chip.setFixedSize(335,41)
            self.preview_buttons_layout.addWidget(sound_chip)

        group_volume = self._get_group_volume_for_group(current_group_id)
        self.volume_display.setText(f"Volume: {group_volume}%")
        self.group_selector_button.setText(f"Group {current_group_id}")
        self.preview_buttons_layout.addStretch(1)