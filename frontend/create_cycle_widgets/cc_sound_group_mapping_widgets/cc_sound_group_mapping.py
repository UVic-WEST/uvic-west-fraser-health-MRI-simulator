from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSlider,
    QAbstractItemView,
    QScroller,
)
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import (
    QPixmap,
    QFont,
)
from frontend.helpers import ReadOnlySlider

from frontend.help_widgets.help_screen import HelpOverlay
from frontend.help_widgets.help_button import HelpButton

# Import SoundConfig at the top for reliability
from backend.sound_config import SoundConfig


# GROUP_OPTIONS is now dynamically determined from backend logic
def get_dynamic_group_options(controller):
    """
    Returns a list of group names (e.g., ["GROUP 1", ...]) based on backend CreateCycleLogic.get_total_groups().
    """
    if hasattr(controller, 'get_total_groups'):
        total_groups, _ = controller.get_total_groups()
        # Always use the backend value, never fallback
        print(f"Total groups from backend: {total_groups}")  # Debug print
        return [f"GROUP {i+1}" for i in range(total_groups)]
    # If backend not available, return empty (should not happen in production)
    return []


SOUND_DROPDOWN_PLACEHOLDER = "SOUNDS"
MAX_SOUNDS_PER_GROUP = 3
SAMPLE_PLAYBACK_SECONDS = 5


class FixedComboBox(QComboBox):
    """
    Combo box with a fixed popup position and constrained popup sizing.
    """

    def __init__(self, parent=None):
        """
        initializes the FixedComboBox and sets up touch scrolling for the popup.
        """
        super().__init__(parent)
        self.popup_max_visible_items = 5
        self._prevent_hide_popup = False
        view = self.view()
        view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        QScroller.grabGesture(view.viewport(), QScroller.LeftMouseButtonGesture)

    
    def showPopup(self):
        """
        shows the combo box popup below the widget and constrains the popup size to a maximum number of visible items, showing a scrollbar if necessary.
        Also styles the scrollbar and background for visibility.
        """
        view = self.view()
        max_visible_items = self.popup_max_visible_items
        # Show vertical scrollbar only when needed
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaxVisibleItems(max_visible_items)

        # Style the popup background and scrollbar
        view.setStyleSheet('''
            QAbstractItemView {
                color: white;
                background: #0474BA;
                border: 1px solid #0474BA;
                border-radius: 14px;
                padding: 4px;
                outline: 0;
            }
            QScrollBar:vertical {
                background: #0474BA;
                width: 14px;
                margin: 2px 0 2px 0;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 24px;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        ''')

        popup_width = self.width()
        view.setMinimumWidth(popup_width)
        view.setMaximumWidth(popup_width)

        row_height = view.sizeHintForRow(0)
        if row_height <= 0:
            row_height = 28
        popup_height = (row_height * max_visible_items) + (2 * view.frameWidth())
        view.setMaximumHeight(popup_height)

        super().showPopup()
        popup = view.window()
        if popup:
            popup.setMinimumWidth(popup_width)
            popup.setMaximumWidth(popup_width)
            popup.move(self.mapToGlobal(QPoint(0, self.height())))

    def hidePopup(self):
        """
        hides the combo box popup unless _prevent_hide_popup is set to True, in which case it leaves the popup open and resets the flag.
        """
        if getattr(self, '_prevent_hide_popup', False):
            return
        super().hidePopup()


class CCSoundGroupMappingPage(QWidget):
    """
    This class builds the sound group mapping page for the custom cycle creation flow.
    
    Args:
        controller: the page/controller reference used by CCSoundGroupMappingPage
        parent: the parent widget for this page
    """
    SAMPLE_PLAYBACK_ACTIVE = False
    SAMPLE_PLAYBACK_REMAINING = 0
    SAMPLE_PLAYBACK_TIMER = None
    _dropdown_style = None

    def __init__(self, controller, parent=None):
        """
        Sound group mapping page with the same structure as ConfirmationPage.

        Args:
            controller: page logic/controller reference
            parent: parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.setFixedSize(1024, 600)

        self.manual_sound_controller = self._resolve_manual_sound_controller()
        # Connect to backend signal for sample playback finished
        if self.manual_sound_controller is not None and hasattr(self.manual_sound_controller, 'samplePlaybackFinished'):
            self.manual_sound_controller.samplePlaybackFinished.connect(self._on_sample_playback_finished)
        self.sound_catalog = self._load_sound_catalog()
        self.sound_option_labels = [label for _, label in self.sound_catalog]
        self.sound_label_to_id = {label: sound_id for sound_id, label in self.sound_catalog}

        # Create main layout
        self.set_background("resources/cycle_running_page_assets/running_cycle.png")
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(40, 0, 40, 16)
        self.main_layout.setSpacing(4)
        self.setLayout(self.main_layout)

        # Error label for invalid sound removal (inside preview panel)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #EC221F; font-size: 16px; font-family: Ubuntu; background: transparent;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setVisible(False)

        self.help_manual_path = "resources/manuals/create_cycle_manual.pdf"
        self.help_overlay = HelpOverlay(self.help_manual_path,self)

        #setting up help button
        self.help_button = HelpButton(self)
        self.help_button.move(140, 20)
        self.help_button.raise_()
        self.help_button.clicked.connect(self.help_pressed)

        self.cancel_home_btn = QPushButton("Cancel", self)
        self.cancel_home_btn.setGeometry(20, 20, 120, 44)
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

        self.back_btn = QPushButton("Back", self)
        self.back_btn.setGeometry(20, 536, 120, 44)
        self.back_btn.setStyleSheet(
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
        self.back_btn.clicked.connect(self.mapping_cancelled)
        self.back_btn.raise_()

        self.next_btn = QPushButton("Next", self)
        self.next_btn.setGeometry(884, 536, 120, 44)
        self.next_btn.setStyleSheet(
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
        self.next_btn.clicked.connect(self.mapping_confirmed)
        self.next_btn.raise_()

        self.default_btn = QPushButton("Default", self)
        self.default_btn.setGeometry(752, 536, 120, 44)
        self.default_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #0474BA;
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
        self.default_btn.clicked.connect(self.default_button_pressed)
        self.default_btn.raise_()

        self.page_title = QLabel("Custom Cycle")
        page_title_font = QFont("Ubuntu", 32)
        self.page_title.setFont(page_title_font)
        self.page_title.setStyleSheet("color: white; background: transparent; padding: 0px; margin: 0px;")
        self.page_title.setAlignment(Qt.AlignCenter)
        self.page_title.setFixedHeight(46)
        self.page_title.setContentsMargins(0, 0, 0, 0)

        self.step_title = QLabel("Step 4: map sounds to groups")
        step_title_font = QFont("Ubuntu", 14)
        self.step_title.setFont(step_title_font)
        self.step_title.setStyleSheet("color: white; background: transparent; padding: 0px; margin: 0px;")
        self.step_title.setAlignment(Qt.AlignCenter)
        self.step_title.setFixedHeight(24)
        self.step_title.setContentsMargins(0, 0, 0, 0)

        self.title_layout = QVBoxLayout()
        self.title_layout.setSpacing(0)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.addWidget(self.page_title)
        self.title_layout.addWidget(self.step_title)
        self.main_layout.addLayout(self.title_layout)

        # Create white box with rounded corners
        self.content_box = QWidget()
        self.content_box.setObjectName("contentBox")
        self.content_box.setStyleSheet(
            """
            #contentBox {
                background-color: white;
                border-radius: 15px;
            }
            """
        )
        self.content_box.setFixedSize(700, 320)

        content_box_layout = QVBoxLayout()
        content_box_layout.setContentsMargins(18, 16, 18, 14)
        content_box_layout.setSpacing(10)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(14)

        left_col = QVBoxLayout()
        left_col.setSpacing(12)
        left_col.setContentsMargins(0, 14, 0, 0)
        left_col.setAlignment(Qt.AlignTop)

        dropdown_style = """
            QComboBox {
                background-color: #0474BA;
                color: white;
                border: 1px solid #0474BA;
                border-radius: 16px;
                padding: 4px 10px;
            }
            QComboBox QAbstractItemView {
                color: white;
                background: #0474BA;
                border: 1px solid #0474BA;
                border-radius: 14px;
                padding: 4px;
                outline: 0;
            }
            QComboBox QAbstractItemView::item {
                border: none;
                padding: 0px 6px;
                margin: 0px;
            }
            QComboBox::drop-down {
                border: none;
                width: 22px;
                background-color: #0474BA;
                border-top-right-radius: 16px;
                border-bottom-right-radius: 16px;
            }
            QComboBox::down-arrow {
                image: url(resources/frontend_common_assets/whitetriangle.png);
                width: 12px;
                height: 8px;
            }
        """


        # Dynamically determine group options from backend
        self.group_options = get_dynamic_group_options(self.controller)
        self.group_dropdown = FixedComboBox()
        self.group_dropdown.setFixedWidth(260)
        self.group_dropdown.setFont(QFont("Ubuntu", 16))
        self.group_dropdown.setStyleSheet(dropdown_style)
        self.group_dropdown.addItems(self.group_options)

        self.sound_dropdown = FixedComboBox()
        self.sound_dropdown.popup_max_visible_items = 4
        self.sound_dropdown.setFixedWidth(260)
        self.sound_dropdown.setFont(QFont("Ubuntu", 16))
        self.sound_dropdown.setStyleSheet(dropdown_style)
        self.sound_dropdown.addItem(SOUND_DROPDOWN_PLACEHOLDER)

        # Save the original dropdown style for later restoration
        self._dropdown_style = dropdown_style


        left_col.addWidget(self.group_dropdown)
        left_col.addWidget(self.sound_dropdown)
        left_col.addStretch(1)

        self.left_col_container = QWidget()
        self.left_col_container.setFixedWidth(260)
        self.left_col_container.setLayout(left_col)

        self.preview_panel = QWidget()
        self.preview_panel.setObjectName("previewPanel")
        self.preview_panel.setFixedSize(390, 240)
        self.preview_panel.setStyleSheet(
            """
            QWidget#previewPanel {
                background-color: #FAF5F5;
                border: 1px solid #0474BA;
                border-radius: 16px;
            }
            """
        )

        preview_layout = QVBoxLayout(self.preview_panel)
        preview_layout.setContentsMargins(14, 12, 14, 12)
        preview_layout.setSpacing(6)

        # Insert error label at the top of the preview panel
        preview_layout.addWidget(self.error_label)

        self.preview_buttons_host = QWidget()
        self.preview_buttons_layout = QVBoxLayout(self.preview_buttons_host)
        self.preview_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.preview_buttons_layout.setSpacing(8)

        # Volume controls anchored to bottom of the small sounds panel.
        volume_row = QHBoxLayout()
        volume_row.setSpacing(8)
        volume_row.setContentsMargins(0, 0, 0, 0)

        self.decrease_volume_button = QPushButton("-")
        self.decrease_volume_button.setFont(QFont("Ubuntu", 18, QFont.Weight.Bold))
        self.decrease_volume_button.setFixedSize(44, 34)
        self.decrease_volume_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0474BA;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:pressed {
                background-color: #024a74;
            }
            QPushButton:disabled {
                background-color: #B4B4B4;
                color: white;
                border: none;
                border-radius: 8px;
            }
            """
        )

        self.increase_volume_button = QPushButton("+")
        self.increase_volume_button.setFont(QFont("Ubuntu", 18, QFont.Weight.Bold))
        self.increase_volume_button.setFixedSize(44, 34)
        self.increase_volume_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0474BA;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:pressed {
                background-color: #024a74;
            }
            QPushButton:disabled {
                background-color: #B4B4B4;
                color: white;
                border: none;
                border-radius: 8px;
            }
            """
        )

        self.volume_slider = ReadOnlySlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setSingleStep(10)
        self.volume_slider.setPageStep(10)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.volume_slider.setStyleSheet(
            """
            QSlider {
                background-color: #FAF5F5;
            }
            """
        )
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)

        self.decrease_volume_button.clicked.connect(self._decrease_volume)
        self.increase_volume_button.clicked.connect(self._increase_volume)

        volume_row.addWidget(self.decrease_volume_button)
        volume_row.addWidget(self.volume_slider)
        volume_row.addWidget(self.increase_volume_button)

        preview_layout.addWidget(self.preview_buttons_host)
        preview_layout.addStretch(1)
        preview_layout.addLayout(volume_row)

        self.play_sample_btn = QPushButton("Play Sample")
        self.play_sample_btn.setFont(QFont("Ubuntu", 14))
        self.play_sample_btn.setFixedSize(150, 40)
        self.play_sample_btn.clicked.connect(self.play_sample_pressed)

        self.right_col_container = QWidget()
        right_col_layout = QVBoxLayout(self.right_col_container)
        right_col_layout.setContentsMargins(0, 0, 0, 0)
        right_col_layout.setSpacing(8)
        right_col_layout.addWidget(self.preview_panel)
        right_col_layout.addStretch(1)

        play_btn_row = QHBoxLayout()
        play_btn_row.setContentsMargins(0, 0, 0, 0)
        play_btn_row.addStretch(1)
        play_btn_row.addWidget(self.play_sample_btn)
        right_col_layout.addLayout(play_btn_row)

        content_layout.addWidget(self.left_col_container, alignment=Qt.AlignTop)
        content_layout.addWidget(self.right_col_container)

        content_box_layout.addLayout(content_layout)
        content_box_layout.addStretch(1)

        self.content_box.setLayout(content_box_layout)
        self.main_layout.addWidget(self.content_box)

        # State for per-group sound mapping is now managed by backend logic
        self.group_dropdown.currentTextChanged.connect(self.on_group_changed)
        self.sound_dropdown.currentTextChanged.connect(self.on_sound_selected)
        self.volume_slider.valueChanged.connect(self.on_volume_slider_changed)
        self.on_group_changed(self.group_dropdown.currentText())

    def help_pressed(self):
        """
        Shows the help screen overlay for this page
        """
        self.help_overlay.show()
        self.help_overlay.raise_()

    def refresh_groups_from_backend(self):
        """
        Refresh the group dropdown and internal group list from backend, preserving sound choices for existing groups.
        """
        old_group = self.group_dropdown.currentText()
        self.group_options = get_dynamic_group_options(self.controller)
        self.group_dropdown.blockSignals(True)
        self.group_dropdown.clear()
        self.group_dropdown.addItems(self.group_options)
        # Try to restore previous group selection if still valid
        if old_group in self.group_options:
            self.group_dropdown.setCurrentText(old_group)
        else:
            self.group_dropdown.setCurrentIndex(0)
        self.group_dropdown.blockSignals(False)
        # Refresh UI for the selected group
        self.on_group_changed(self.group_dropdown.currentText())

    def _resolve_manual_sound_controller(self):
        """
        This function finds the app-level manual sound controller from parent widgets.

        Args:
            None

        Returns:
            controller: ManualSoundController instance if available, otherwise None
        """
        current = self.parent
        while current is not None:
            if hasattr(current, "manual_sound_controller"):
                return current.manual_sound_controller

            if hasattr(current, "parent"):
                parent_ref = current.parent
                current = parent_ref() if callable(parent_ref) else parent_ref
            else:
                current = None

        return None

    def _load_sound_catalog(self):
        """
        Loads sound options from backend CreateCycleLogic.get_sounds() if available, else falls back to manual_sound_controller or generic default.

        Returns:
            catalog: list of tuples in the form (sound_id, sound_label)
        """
        # Prefer backend CreateCycleLogic if available
        if hasattr(self.controller, 'get_sounds'):
            try:
                backend_sounds = self.controller.get_sounds()
                catalog = []
                for sound_id, sound_name in backend_sounds:
                    sound_label = str(sound_name)
                    catalog.append((int(sound_id), sound_label))
                if catalog:
                    return catalog
            except Exception:
                pass
        # Fallback to manual_sound_controller if available
        if self.manual_sound_controller is not None:
            try:
                backend_sounds = self.manual_sound_controller.get_sounds()
                catalog = []
                for sound_id, sound_name in backend_sounds:
                    sound_label = str(sound_name)
                    catalog.append((int(sound_id), sound_label))
                if catalog:
                    return catalog
            except Exception:
                pass
        # Fallback: 8 generic sounds if backend is unavailable
        return [(i + 1, f"SOUND {i + 1}") for i in range(8)]

    def set_background(self, image_path):
        """
        Set the background image for this page.

        Args:
            image_path (str): path to the background image asset
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

    def mapping_cancelled(self):
        """
        Move to previous create-cycle page when mapping is cancelled.
        """
        self._stop_sample_playback()
        print("back was pressed")
        if self.parent and hasattr(self.parent, "back_pressed"):
            self.parent.back_pressed()

    def mapping_confirmed(self):
        """
        This function moves to the next create-cycle page when mapping is confirmed.
        """
        # Check backend for each group
        incomplete = False
        for group in self.group_options:
            group_id = self._group_name_to_id(group)
            backend_sounds = []
            if hasattr(self.controller, 'get_sounds_in_group'):
                try:
                    backend_sounds = self.controller.get_sounds_in_group(group_id) or []
                except Exception:
                    pass
            if len(backend_sounds) == 0:
                incomplete = True
                break
        if incomplete:
            self._show_incomplete_input_warning()
            return

        self._stop_sample_playback()
        print("next was pressed")
        if self.parent and hasattr(self.parent, "next_pressed"):
            self.parent.next_pressed()

    def _show_incomplete_input_warning(self):
        """
        This function shows a warning when one or more groups have no selected sounds.
        """
        warning_message = (
            "Unfinished Input Warning\n\n"
            "Please input at least one sound\nper group before continuing"
        )

        current = self.parent
        while current is not None:
            if hasattr(current, "show_warning"):
                current.show_warning(
                    warning_message=warning_message,
                    button_mode="red",
                    red_button_text="GO BACK",
                    on_cancel=self._return_to_sound_mapping_page,
                )
                return

            if hasattr(current, "parent"):
                current = current.parent()
            else:
                current = None

    def _return_to_sound_mapping_page(self):
        """
        This function returns from the warning page back to the sound-group mapping step.
        """
        current = self.parent
        while current is not None:
            if hasattr(current, "main_layout") and hasattr(current, "create_cycle_router"):
                current.main_layout.setCurrentWidget(current.create_cycle_router)
                if hasattr(self.parent, "main_layout") and self.parent.main_layout.indexOf(self) != -1:
                    self.parent.main_layout.setCurrentWidget(self)
                return

            if hasattr(current, "parent"):
                current = current.parent()
            else:
                current = None

    def cancel_to_home(self):
        """
        Return the user to the home page from this step.
        """
        self._stop_sample_playback()
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

    def default_button_pressed(self):
        """
        Clear the sounds for the currently selected group only (via backend), allowing empty group.
        """
        current_group = self.group_dropdown.currentText()
        group_id = self._group_name_to_id(current_group)
        try:
            # Explicitly allow empty group
            self.controller.set_sounds_in_group(group_id, [], allow_empty=True)
        except Exception as exc:
            print(f"[default_button_pressed] Error when clearing group {group_id}: {exc}")
        self.on_group_changed(current_group)
        print(f"default button was pressed for {current_group}")

    def play_sample_pressed(self):
        """
        This function handles the Play Sample action for the active group's selected sounds.
        Uses play_group_sample from backend logic.
        """
        current_group = self.group_dropdown.currentText()
        group_id = self._group_name_to_id(current_group)
        print(f"[play_sample_pressed] Play Sample pressed for group_id={group_id} ({current_group})")
        try:
            result = self.controller.play_group_sample(group_id)
            print(f"[play_sample_pressed] play_group_sample result: {result}")
        except Exception as exc:
            print(f"[play_sample_pressed] Error calling play_group_sample: {exc}")
            return

        # Use a fixed 5 second sample duration for UI lockout
        max_duration = SAMPLE_PLAYBACK_SECONDS
        self.SAMPLE_PLAYBACK_ACTIVE = True

        # Grey out dropdowns and show countdown as placeholder
        self.sound_dropdown.setEnabled(False)
        self.group_dropdown.setEnabled(False)
        self._set_dropdowns_greyed(True)
        self._set_dropdowns_placeholder(f"{max_duration}s")

        # Lock out the volume controls during sample playback
        self.decrease_volume_button.setEnabled(False)
        self.increase_volume_button.setEnabled(False)

        # Lock out navigation and default buttons
        self.cancel_home_btn.setEnabled(False)
        self.back_btn.setEnabled(False)
        self.next_btn.setEnabled(False)
        self.default_btn.setEnabled(False)
        self.help_button.setEnabled(False)

        # Change button to grey and start countdown
        from PySide6.QtCore import QTimer
        self.SAMPLE_PLAYBACK_REMAINING = max_duration
        self.play_sample_btn.setEnabled(False)
        self.play_sample_btn.setText(f"{self.SAMPLE_PLAYBACK_REMAINING}s")
        self.play_sample_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #B4B4B4;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 6px 14px;
            }
            """
        )
        if self.SAMPLE_PLAYBACK_TIMER is not None:
            self.SAMPLE_PLAYBACK_TIMER.stop()
            self.SAMPLE_PLAYBACK_TIMER.deleteLater()
        self.SAMPLE_PLAYBACK_TIMER = QTimer(self)
        self.SAMPLE_PLAYBACK_TIMER.setInterval(1000)
        self.SAMPLE_PLAYBACK_TIMER.timeout.connect(self._on_sample_countdown_tick)
        self.SAMPLE_PLAYBACK_TIMER.start()
        # UI will now be unlocked by backend signal, not by timer here

    def _on_sample_countdown_tick(self):
        """
        This function updates the sample playback countdown timer and unlocks the UI when playback is finished.
        """
        self.SAMPLE_PLAYBACK_REMAINING -= 1
        if self.SAMPLE_PLAYBACK_REMAINING > 0:
            self.play_sample_btn.setText(f"{self.SAMPLE_PLAYBACK_REMAINING}s")
        else:
            # Always clean up timer and trigger finish logic only once
            if self.SAMPLE_PLAYBACK_TIMER is not None:
                self.SAMPLE_PLAYBACK_TIMER.stop()
                self.SAMPLE_PLAYBACK_TIMER.deleteLater()
                self.SAMPLE_PLAYBACK_TIMER = None
            # Only call finish if not already unlocked
            if self.SAMPLE_PLAYBACK_ACTIVE:
                self._on_sample_playback_finished()

    def _on_sample_playback_finished(self):
        """
        This function is called when sample playback is finished.
        """
        self.SAMPLE_PLAYBACK_ACTIVE = False
        if hasattr(self.controller, "stop_sample"):
            self.controller.stop_sample()
        self.sound_dropdown.setEnabled(True)
        self.group_dropdown.setEnabled(True)
        self._set_dropdowns_greyed(False)
        self._set_dropdowns_placeholder(SOUND_DROPDOWN_PLACEHOLDER)
        # Restore volume controls after temporary sample lockout.
        self.decrease_volume_button.setEnabled(True)
        self.increase_volume_button.setEnabled(True)
        # Re-enable navigation and default buttons
        self.cancel_home_btn.setEnabled(True)
        self.back_btn.setEnabled(True)
        self.next_btn.setEnabled(True)
        self.default_btn.setEnabled(True)
        self.help_button.setEnabled(True)

    def _set_dropdowns_greyed(self, greyed):
        """
        This function sets the dropdowns to a greyed-out style when sample playback is active, and restores the original style when playback is finished.
        """
        grey_style = (
            "QComboBox {"
            "background-color: #B4B4B4;"
            "color: white;"
            "border: 1px solid #B4B4B4;"
            "border-radius: 16px;"
            "padding: 4px 10px;"
            "}"
            "QComboBox QAbstractItemView {"
            "color: white;"
            "background: #B4B4B4;"
            "border: 1px solid #B4B4B4;"
            "border-radius: 14px;"
            "padding: 4px;"
            "outline: 0;"
            "}"
            "QComboBox QAbstractItemView::item {"
            "border: none;"
            "padding: 0px 6px;"
            "margin: 0px;"
            "}"
            "QComboBox::drop-down {"
            "border: none;"
            "width: 22px;"
            "background-color: #B4B4B4;"
            "border-top-right-radius: 16px;"
            "border-bottom-right-radius: 16px;"
            "}"
            "QComboBox::down-arrow {"
            "image: url(resources/frontend_common_assets/whitetriangle.png);"
            "width: 12px;"
            "height: 8px;"
            "}"
        )
        if greyed:
            self.sound_dropdown.setStyleSheet(grey_style)
            self.group_dropdown.setStyleSheet(grey_style)
        else:
            # Restore original style
            self.sound_dropdown.setStyleSheet(self._dropdown_style)
            self.group_dropdown.setStyleSheet(self._dropdown_style)

    def _set_dropdowns_placeholder(self, text):
        """
        This function sets the placeholder text for the dropdowns.

        Args:
            text: the placeholder text to set
        """
        self.sound_dropdown.setCurrentText(text)
        if self.SAMPLE_PLAYBACK_TIMER is not None:
            self.SAMPLE_PLAYBACK_TIMER.stop()
            self.SAMPLE_PLAYBACK_TIMER.deleteLater()
            self.SAMPLE_PLAYBACK_TIMER = None
        self.play_sample_btn.setText("Play Sample")
        self._update_play_sample_button_state(self.group_dropdown.currentText())

    def _stop_sample_playback(self):
        """
        This function stops sample playback when leaving this page.
        """
        if hasattr(self.controller, "stop_sample"):
            self.controller.stop_sample()
        if self.manual_sound_controller is not None:
            self.manual_sound_controller.set_manual_sound_controller_status(False)

    def _update_play_sample_button_state(self, group_name):
        """
        This function updates Play Sample button style based on whether the current group has sounds (using backend).

        Args:
            group_name: name of the currently selected group
        """
        group_id = self._group_name_to_id(group_name)
        has_sounds = False
        if hasattr(self.controller, 'get_sounds_in_group'):
            try:
                backend_sounds = self.controller.get_sounds_in_group(group_id)
                has_sounds = bool(backend_sounds)
            except Exception:
                pass
        if has_sounds:
            self.play_sample_btn.setEnabled(True)
            self.play_sample_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #0474BA;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    padding: 6px 14px;
                }
                QPushButton:pressed {
                    background-color: #035f98;
                }
                """
            )
            return
        self.play_sample_btn.setEnabled(False)
        self.play_sample_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #B4B4B4;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 6px 14px;
            }
            """
        )

    def on_group_changed(self, group_name):
        """
        Refresh dropdown options and selected sound list for the active group, syncing with backend.
        Uses get_sounds_in_group directly for all retrievals.
        """
        group_id = self._group_name_to_id(group_name)
        selected_for_group = []
        group_volume = 50
        try:
            backend_sounds = self.controller.get_sounds_in_group(group_id)
            if backend_sounds:
                selected_for_group = [s.file_name for s in backend_sounds]
            # Only use backend for group volume
            group = self.controller._get_group(group_id)
            group_volume = getattr(group, 'group_volume', 50)
        except Exception:
            pass
        # Update dropdowns
        if len(selected_for_group) >= MAX_SOUNDS_PER_GROUP:
            self.sound_dropdown.blockSignals(True)
            self.sound_dropdown.clear()
            self.sound_dropdown.addItem("Max 3 Sounds per Group")
            self.sound_dropdown.setCurrentIndex(0)
            self.sound_dropdown.setEnabled(False)
            grey_style = (
                "QComboBox {"
                "background-color: #B4B4B4;"
                "color: white;"
                "border: 1px solid #B4B4B4;"
                "border-radius: 16px;"
                "padding: 4px 10px;"
                "}"
                "QComboBox QAbstractItemView {"
                "color: white;"
                "background: #B4B4B4;"
                "border: 1px solid #B4B4B4;"
                "border-radius: 14px;"
                "padding: 4px;"
                "outline: 0;"
                "}"
                "QComboBox QAbstractItemView::item {"
                "border: none;"
                "padding: 0px 6px;"
                "margin: 0px;"
                "}"
                "QComboBox::drop-down {"
                "border: none;"
                "width: 22px;"
                "background-color: #B4B4B4;"
                "border-top-right-radius: 16px;"
                "border-bottom-right-radius: 16px;"
                "}"
                "QComboBox::down-arrow {"
                "image: url(resources/frontend_common_assets/whitetriangle.png);"
                "width: 12px;"
                "height: 8px;"
                "}"
            )
            self.sound_dropdown.setStyleSheet(grey_style)
            self.sound_dropdown.view().setRowHidden(0, False)
            self.sound_dropdown.blockSignals(False)
        else:
            available_sounds = [s for s in self.sound_option_labels if s not in selected_for_group]
            self.sound_dropdown.blockSignals(True)
            self.sound_dropdown.clear()
            self.sound_dropdown.addItem(SOUND_DROPDOWN_PLACEHOLDER)
            self.sound_dropdown.addItems(available_sounds)
            self.sound_dropdown.setCurrentIndex(0)
            self.sound_dropdown.view().setRowHidden(0, True)
            self.sound_dropdown.setEnabled(True)
            self.sound_dropdown.setStyleSheet(self._dropdown_style)
            self.sound_dropdown.blockSignals(False)
        self.refresh_preview_panel_backend(group_name, selected_for_group)
        self._update_play_sample_button_state(group_name)
        # Set volume slider to backend value
        self.volume_slider.blockSignals(True)
        self.volume_slider.setValue(group_volume)
        self.volume_slider.blockSignals(False)

    def _group_name_to_id(self, group_name):
        """
        Convert a group name string (e.g., 'GROUP 1') to its integer group ID.

        Args:
            group_name (str): The group name in the format 'GROUP N'.

        Returns:
            int: The group ID as an integer. Defaults to 1 if parsing fails.
        """
        try:
            return int(group_name.split()[-1])
        except Exception:
            return 1

    def refresh_preview_panel_backend(self, group_name, selected_for_group):
        """
        Render the selected sounds for the active group in the preview panel (right panel).

        Args:
            group_name (str): The name of the group being displayed.
            selected_for_group (list): List of sound names selected for this group.
        """
        self._clear_preview_buttons()
        if not selected_for_group:
            return
        for sound_name in selected_for_group:
            sound_chip = QPushButton(sound_name)
            sound_chip.setFont(QFont("Ubuntu", 14))
            sound_chip.clicked.connect(
                lambda checked=False, name=sound_name: self.on_preview_sound_clicked(name)
            )
            sound_chip.setStyleSheet(
                """
                QPushButton {
                    background-color: #2E9B41;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 10px 16px;
                }
                QPushButton:hover {
                    background-color: #2E9B41;
                }
                QPushButton:pressed {
                    background-color: #2E9B41;
                }
                """
            )
            self.preview_buttons_layout.addWidget(sound_chip)
        self.preview_buttons_layout.addStretch(1)

    def on_sound_selected(self, sound_name):
        """
        Add selected sound to current group (max 3), then refresh UI and backend.
        Uses get_sounds_in_group and set_sounds_in_group directly.
        """
        if sound_name == SOUND_DROPDOWN_PLACEHOLDER or self.SAMPLE_PLAYBACK_ACTIVE:
            return
        current_group = self.group_dropdown.currentText()
        group_id = self._group_name_to_id(current_group)
        # Get current backend sounds directly
        try:
            backend_sounds = self.controller.get_sounds_in_group(group_id) or []
        except Exception as exc:
            print(f"[on_sound_selected] Error getting backend sounds for group {group_id}: {exc}")
            backend_sounds = []
        # Prevent duplicates and max
        if any(s.file_name == sound_name for s in backend_sounds):
            print(f"[on_sound_selected] Sound '{sound_name}' already in group {group_id}, skipping add.")
            self.on_group_changed(current_group)
            return
        if len(backend_sounds) >= MAX_SOUNDS_PER_GROUP:
            print(f"[on_sound_selected] Group {group_id} already has max sounds, skipping add.")
            self.on_group_changed(current_group)
            return
        # Add new sound as SoundConfig
        sound_id = self.sound_label_to_id.get(sound_name, None)
        if sound_id is None:
            print(f"[on_sound_selected] Could not find sound_id for '{sound_name}', skipping add.")
            return
        new_sound = SoundConfig(file_name=sound_name, sound_id=sound_id, duration=10.0, volume=int(self.volume_slider.value()))
        new_sounds = list(backend_sounds) + [new_sound]
        print(f"[on_sound_selected] Attempting to set new sounds for group {group_id}: {new_sounds}")
        try:
            self.controller.set_sounds_in_group(group_id, new_sounds)
            print(f"[on_sound_selected] Successfully set new sounds for group {group_id}.")
        except Exception as exc:
            print(f"[on_sound_selected] Error setting new sounds for group {group_id}: {exc}")
        self.on_group_changed(current_group)
        # Re-open the popup after selection (unless group changed or max reached)
        if len(new_sounds) < MAX_SOUNDS_PER_GROUP:
            QTimer.singleShot(150, self.sound_dropdown.showPopup)

    def refresh_preview_panel(self, group_name):
        """
        Render selected sounds for the active group in the right panel.
        """
        # Get selected sound labels for this group from backend
        selected_for_group = []
        group_id = self._group_name_to_id(group_name)
        if hasattr(self.controller, 'get_sounds_in_group'):
            try:
                backend_sounds = self.controller.get_sounds_in_group(group_id) or []
                selected_for_group = [s.file_name for s in backend_sounds]
            except Exception:
                pass

        self._clear_preview_buttons()

        if not selected_for_group:
            return

        for sound_name in selected_for_group:
            sound_chip = QPushButton(sound_name)
            sound_chip.setFont(QFont("Ubuntu", 14))
            sound_chip.clicked.connect(
                lambda checked=False, name=sound_name: self.on_preview_sound_clicked(name)
            )
            sound_chip.setStyleSheet(
                """
                QPushButton {
                    background-color: #2E9B41;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 10px 16px;
                }
                QPushButton:hover {
                    background-color: #2E9B41;
                }
                QPushButton:pressed {
                    background-color: #2E9B41;
                }
                """
            )
            self.preview_buttons_layout.addWidget(sound_chip)

        self.preview_buttons_layout.addStretch(1)

    def on_preview_sound_clicked(self, sound_name):
        """
        Remove a selected sound from the active group and update backend.
        Disabled during sample playback. Shows error if backend rejects empty group.
        Uses get_sounds_in_group and set_sounds_in_group directly.
        """
        if self.SAMPLE_PLAYBACK_ACTIVE:
            return
        current_group = self.group_dropdown.currentText()
        group_id = self._group_name_to_id(current_group)
        try:
            backend_sounds = self.controller.get_sounds_in_group(group_id) or []
        except Exception:
            backend_sounds = []
        # Remove by file_name
        new_sounds = [s for s in backend_sounds if s.file_name != sound_name]
        error = False
        try:
            self.controller.set_sounds_in_group(group_id, new_sounds)
            # If backend rejects empty, show error
            if len(new_sounds) == 0:
                self._show_error("Cannot remove sound.\nAll groups must have at least 1 sound.")
                error = True
        except Exception as exc:
            self._show_error("Cannot remove sound.\nAll groups must have at least 1 sound.")
            error = True
        self.on_group_changed(current_group)
        if not error:
            self._hide_error()

    def _show_error(self, message):
        """
        Show a red error message label and auto-hide after 3 seconds.
        """
        self.error_label.setText(message)
        self.error_label.setVisible(True)
        QTimer.singleShot(3000, self._hide_error)

    def _hide_error(self):
        """
        Hide the error message label in the preview panel.
        This is called after a timeout or when the error is no longer relevant.
        """
        self.error_label.setVisible(False)
    def on_volume_slider_changed(self, value):
        """
        Update backend group volume when slider changes using set_volume_for_group.
        """
        current_group = self.group_dropdown.currentText()
        group_id = self._group_name_to_id(current_group)
        try:
            self.controller.set_volume_for_group(group_id, value)
        except Exception as exc:
            print(f"[on_volume_slider_changed] Error setting volume for group {group_id}: {exc}")

    def _clear_preview_buttons(self):
        """
        Remove all sound chip widgets from the preview panel for the current group.
        This clears the panel before re-rendering the current group's selected sounds.
        """
        while self.preview_buttons_layout.count() > 0:
            item = self.preview_buttons_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _on_volume_changed(self, value):
        """
        Keep volume snapped to 10-point increments.
        """
        snapped = max(0, min(100, int(round(value / 10.0) * 10)))
        if snapped != value:
            self.volume_slider.blockSignals(True)
            self.volume_slider.setValue(snapped)
            self.volume_slider.blockSignals(False)

    def _decrease_volume(self):
        """
        Decrease volume by one 10-point step.
        """
        self.volume_slider.setValue(max(0, self.volume_slider.value() - 10))

    def _increase_volume(self):
        """
        Increase volume by one 10-point step.
        """
        self.volume_slider.setValue(min(100, self.volume_slider.value() + 10))