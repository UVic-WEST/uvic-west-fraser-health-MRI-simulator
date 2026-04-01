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

GROUP_OPTIONS = [
    "GROUP 1",
    "GROUP 2",
    "GROUP 3",
    "GROUP 4",
]



SOUND_DROPDOWN_PLACEHOLDER = "SOUNDS"
MAX_SOUNDS_PER_GROUP = 3


class FixedComboBox(QComboBox):
    """
    Combo box with a fixed popup position and constrained popup sizing.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.popup_max_visible_items = 5
        self._prevent_hide_popup = False
        view = self.view()
        view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        QScroller.grabGesture(view.viewport(), QScroller.LeftMouseButtonGesture)

    def showPopup(self):
        view = self.view()
        max_visible_items = self.popup_max_visible_items
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaxVisibleItems(max_visible_items)

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
        if getattr(self, '_prevent_hide_popup', False):
            return
        super().hidePopup()


class CCSoundGroupMappingPage(QWidget):
    SAMPLE_PLAYBACK_ACTIVE = False
    SAMPLE_PLAYBACK_REMAINING = 0
    SAMPLE_PLAYBACK_TIMER = None
    _dropdown_style = None
    SAMPLE_PLAYBACK_ACTIVE = False
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

        self.group_dropdown = FixedComboBox()
        self.group_dropdown.setFixedWidth(260)
        self.group_dropdown.setFont(QFont("Ubuntu", 16))
        self.group_dropdown.setStyleSheet(dropdown_style)
        self.group_dropdown.addItems(GROUP_OPTIONS)

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

        # State for per-group sound mapping.
        self.group_to_sounds = {group: [] for group in GROUP_OPTIONS}
        self.group_dropdown.currentTextChanged.connect(self.on_group_changed)
        self.sound_dropdown.currentTextChanged.connect(self.on_sound_selected)
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
        This function loads sound options from backend and falls back to a generic default if backend is unavailable.

        Returns:
            catalog: list of tuples in the form (sound_id, sound_label)
        """
        if self.manual_sound_controller is not None:
            try:
                backend_sounds = self.manual_sound_controller.get_sounds()
                catalog = []
                for sound_id, sound_name in backend_sounds:
                    sound_label = str(sound_name)  # Use backend name as-is
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

        Args:
            None
        """
        if any(len(self.group_to_sounds.get(group, [])) == 0 for group in GROUP_OPTIONS):
            self._show_incomplete_input_warning()
            return

        self._stop_sample_playback()
        print("next was pressed")
        if self.parent and hasattr(self.parent, "next_pressed"):
            self.parent.next_pressed()

    def _show_incomplete_input_warning(self):
        """
        This function shows a warning when one or more groups have no selected sounds.

        Args:
            None
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

        Args:
            None
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
        Clear the sounds for the currently selected group only.
        """
        current_group = self.group_dropdown.currentText()
        if current_group in self.group_to_sounds:
            self.group_to_sounds[current_group] = []
            self.on_group_changed(current_group)
        print(f"default button was pressed for {current_group}")

    def play_sample_pressed(self):
        """
        This function handles the Play Sample action for the active group's selected sounds.

        Args:
            None
        """
        current_group = self.group_dropdown.currentText()
        selected_labels = self.group_to_sounds.get(current_group, [])
        if not selected_labels:
            return

        selected_sound_ids = [
            self.sound_label_to_id[label]
            for label in selected_labels
            if label in self.sound_label_to_id
        ]
        if not selected_sound_ids:
            return

        volume = int(self.volume_slider.value())
        if self.manual_sound_controller is None:
            print("manual sound controller unavailable for sample playback")
            return


        self.manual_sound_controller.set_manual_sound_controller_status(True)
        result = self.manual_sound_controller.play_sounds(selected_sound_ids, volume)
        print(f"play sample pressed for {current_group}: ids={selected_sound_ids}, volume={volume}, ok={result}")
        self.SAMPLE_PLAYBACK_ACTIVE = True

        # Grey out dropdowns and show countdown as placeholder
        self.sound_dropdown.setEnabled(False)
        self.group_dropdown.setEnabled(False)
        self._set_dropdowns_greyed(True)
        self._set_dropdowns_placeholder(f"{self.SAMPLE_PLAYBACK_REMAINING}s")

        # Lock out navigation and default buttons
        self.cancel_home_btn.setEnabled(False)
        self.back_btn.setEnabled(False)
        self.next_btn.setEnabled(False)
        self.default_btn.setEnabled(False)

        # Change button to grey and start countdown
        from backend.manual_sound_controller import SAMPLE_PLAYBACK_SECONDS
        from PySide6.QtCore import QTimer
        self.SAMPLE_PLAYBACK_REMAINING = SAMPLE_PLAYBACK_SECONDS
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
        self.SAMPLE_PLAYBACK_REMAINING -= 1
        if self.SAMPLE_PLAYBACK_REMAINING > 0:
            self.play_sample_btn.setText(f"{self.SAMPLE_PLAYBACK_REMAINING}s")
        else:
            if self.SAMPLE_PLAYBACK_TIMER is not None:
                self.SAMPLE_PLAYBACK_TIMER.stop()
                self.SAMPLE_PLAYBACK_TIMER.deleteLater()
                self.SAMPLE_PLAYBACK_TIMER = None

    def _on_sample_playback_finished(self):
        self.SAMPLE_PLAYBACK_ACTIVE = False
        self.sound_dropdown.setEnabled(True)
        self.group_dropdown.setEnabled(True)
        self._set_dropdowns_greyed(False)
        self._set_dropdowns_placeholder(SOUND_DROPDOWN_PLACEHOLDER)
        # Re-enable navigation and default buttons
        self.cancel_home_btn.setEnabled(True)
        self.back_btn.setEnabled(True)
        self.next_btn.setEnabled(True)
        self.default_btn.setEnabled(True)

    def _set_dropdowns_greyed(self, greyed):
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

        Args:
            None
        """
        if self.manual_sound_controller is not None:
            self.manual_sound_controller.set_manual_sound_controller_status(False)

    def _update_play_sample_button_state(self, group_name):
        """
        This function updates Play Sample button style based on whether the current group has sounds.

        Args:
            group_name: name of the currently selected group
        """
        has_sounds = bool(self.group_to_sounds.get(group_name, []))
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
        Refresh dropdown options and selected sound list for the active group.
        """
        if group_name not in self.group_to_sounds:
            return

        selected_for_group = self.group_to_sounds[group_name]
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

        self.refresh_preview_panel(group_name)
        self._update_play_sample_button_state(group_name)

    def on_sound_selected(self, sound_name):
        """
        Add selected sound to current group (max 3), then refresh UI.
        """
        if sound_name == SOUND_DROPDOWN_PLACEHOLDER or self.SAMPLE_PLAYBACK_ACTIVE:
            return

        current_group = self.group_dropdown.currentText()
        if current_group not in self.group_to_sounds:
            return

        selected_for_group = self.group_to_sounds[current_group]
        if sound_name in selected_for_group:
            self.on_group_changed(current_group)
            return

        if len(selected_for_group) >= MAX_SOUNDS_PER_GROUP:
            print(f"{current_group} already has {MAX_SOUNDS_PER_GROUP} sounds")
            self.on_group_changed(current_group)
            return

        selected_for_group.append(sound_name)
        self.on_group_changed(current_group)
        # Re-open the popup after selection (unless group changed or max reached)
        if len(selected_for_group) < MAX_SOUNDS_PER_GROUP:
            QTimer.singleShot(150, self.sound_dropdown.showPopup)

    def refresh_preview_panel(self, group_name):
        """
        Render selected sounds for the active group in the right panel.
        """
        selected_for_group = self.group_to_sounds.get(group_name, [])

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
        Remove a selected sound from the active group and refresh UI.
        Disabled during sample playback.
        """
        if self.SAMPLE_PLAYBACK_ACTIVE:
            return
        current_group = self.group_dropdown.currentText()
        if current_group not in self.group_to_sounds:
            return

        selected_for_group = self.group_to_sounds[current_group]
        if sound_name not in selected_for_group:
            return

        selected_for_group.remove(sound_name)
        self.on_group_changed(current_group)

    def _clear_preview_buttons(self):
        """
        Remove all rendered sound chips from the preview panel.
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