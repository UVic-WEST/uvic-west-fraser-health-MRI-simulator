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

from frontend.create_cycle_widgets.cc_summary_widgets.sound_group_summary_widget import SoundGroupSummaryWidget

DURATION_PAGE_INDEX = 0
GROUPS_PAGE_INDEX = 1
LIGHTS_PAGE_INDEX = 2
SOUNDS_PAGE_INDEX = 3

class CCSummary(QWidget):
    def __init__(self, controller, parent=None):
        """
        Build the summary page UI and bind controls for final review/edit flow.

        Args:
            controller: create-cycle controller used to read/save configuration
            parent: parent widget/router for navigation callbacks
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.setFixedSize(1024, 600)

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

        self.help_manual_path = None
        self.help_overlay = HelpOverlay(self.help_manual_path,self)
        #setting up help button
        self.help_button = HelpButton(self)
        self.help_button.move(140, 20)
        self.help_button.raise_()
        self.help_button.clicked.connect(self.help_pressed)

        self.back_btn = QPushButton("Back", self)
        self.back_btn.setGeometry(20, 536, 120, 44)
        self.back_btn.setStyleSheet(self.cancel_home_btn.styleSheet())
        self.back_btn.clicked.connect(self.mapping_cancelled)
        self.back_btn.raise_()

        self.page_title = QLabel("Custom Cycle")
        self.page_title.setFont(QFont("Ubuntu", 32))
        self.page_title.setStyleSheet("color: white; background: transparent; padding: 0px; margin: 0px;")
        self.page_title.setAlignment(Qt.AlignCenter)
        self.page_title.setFixedHeight(46)
        self.page_title.setContentsMargins(0, 0, 0, 0)

        self.step_title = QLabel("Step 5: summary")
        self.step_title.setFont(QFont("Ubuntu", 14))
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
        self.duration_summary_btn.clicked.connect(self.edit_duration)

        lights_summary_btn_icon = 'resources/create_cycle_assets/brightness_icon.png'
        self.lights_summary_btn = QPushButton("Cycle Lights: --%")
        self.set_up_remapping_buttons(self.lights_summary_btn, lights_summary_btn_icon)
        self.lights_summary_btn.clicked.connect(self.edit_lights)

        groups_summary_btn = 'resources/create_cycle_assets/group_icon.png'
        self.groups_summary_btn = QPushButton("Total Groups: --")
        self.set_up_remapping_buttons(self.groups_summary_btn, groups_summary_btn)
        self.groups_summary_btn.clicked.connect(self.edit_groups)

        self.preview_panel = SoundGroupSummaryWidget(controller,self)

        confirm_button_style = """
            QPushButton {
                background-color: #2E9B41;
                color: white;
                border: none;
                border-radius: 14px;
                padding: 8px 14px;
                text-align: center;
                font-family: Ubuntu;
                font-size: 18px;
            }
            QPushButton:pressed {
                background-color: #1D682B;
            }
        """

        self.confirm_btn = QPushButton("Confirm")
        self.confirm_btn.setFixedHeight(48)
        self.confirm_btn.setStyleSheet(confirm_button_style)
        self.confirm_btn.clicked.connect(self.confirm_summary)

        content_layout.addWidget(self.duration_summary_btn)
        content_layout.addWidget(self.lights_summary_btn)
        content_layout.addWidget(self.groups_summary_btn)
        content_layout.addWidget(self.confirm_btn)

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

    def showEvent(self, event):
        """
        Refresh summary values whenever the page becomes visible.

        Args:
            event: Qt show event
        """
        super().showEvent(event)
        self._update_summary_buttons()

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
        if hasattr(self.controller, "get_duration"):
            try:
                total_seconds = int(self.controller.get_duration())
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
        if hasattr(self.controller, "get_light_level"):
            try:
                lights_text = str(int(self.controller.get_light_level()))
            except Exception as e:
                print(f"[_update_lights_summary_button] Error: {e}")

        self.lights_summary_btn.setText(f"Cycle Lights: {lights_text}%")

    def _update_groups_summary_button(self):
        """
        Reads total groups from backend controller and updates the summary button label.
        """
        groups_text = "--"
        if hasattr(self.controller, "get_total_groups"):
            try:
                total_groups, _ = self.controller.get_total_groups()
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

    def mapping_cancelled(self):
        """
        Route to the previous step in the create-cycle flow.
        """
        print("back was pressed")
        if self.parent and hasattr(self.parent, "back_pressed"):
            self.parent.back_pressed()

    def mapping_confirmed(self):
        """
        Route to the next step in the create-cycle flow.
        """
        print("next was pressed")
        if self.parent and hasattr(self.parent, "next_pressed"):
            self.parent.next_pressed()

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

    def _go_to_page(self, page_index):
        """
        This function routes to a specific page in the create-cycle flow.

        Args:
            page_index: index of page in the parent stacked layout
        """
        if self.parent and hasattr(self.parent, "main_layout"):
            if page_index == SOUNDS_PAGE_INDEX and hasattr(self.parent, "_ensure_sound_group_mapping_page"):
                self.parent._ensure_sound_group_mapping_page()
                if hasattr(self.parent, "cc_sound_group_mapping_page") and self.parent.cc_sound_group_mapping_page is not None:
                    self.parent.cc_sound_group_mapping_page.refresh_groups_from_backend()
            self.parent.main_layout.setCurrentIndex(page_index)

    def edit_duration(self):
        """
        This function routes the user back to the duration page for editing.

        Args:
            None
        """
        self._go_to_page(DURATION_PAGE_INDEX)

    def edit_lights(self):
        """
        This function routes the user back to the lights page for editing.

        Args:
            None
        """
        self._go_to_page(LIGHTS_PAGE_INDEX)

    def edit_groups(self):
        """
        This function routes the user back to the groups page for editing.

        Args:
            None
        """
        self._go_to_page(GROUPS_PAGE_INDEX)

    def edit_sounds(self):
        """
        This function routes the user back to the sounds page for editing.

        Args:
            None
        """
        self._go_to_page(SOUNDS_PAGE_INDEX)

    def confirm_summary(self):
        """
        This function opens a final confirmation warning before keeping customization.

        Args:
            None
        """
        self._show_keep_customization_warning()

    def _show_keep_customization_warning(self):
        """
        This function shows a yes/no warning before finalizing customization.

        Args:
            None
        """
        current = self.parent
        while current is not None:
            if hasattr(current, "show_warning"):
                current.show_warning(
                    warning_message="Are you sure you want\nto keep this customization?",
                    on_confirm=self._confirm_customization,
                    on_cancel=self._return_to_summary,
                    button_mode="both",
                    green_button_text="YES",
                    red_button_text="NO",
                )
                return

            if hasattr(current, "parent"):
                parent_ref = current.parent
                current = parent_ref() if callable(parent_ref) else parent_ref
            else:
                current = None

    def _confirm_customization(self):
        """
        This function handles the YES action from the final customization warning.

        Args:
            None
        """
        save_errors = []
        saved_cycle = None
        if hasattr(self.controller, "save_cycle"):
            try:
                saved_cycle = self.controller.save_cycle()
            except Exception as e:
                save_errors.append(f"Save failed: {e}")

        if saved_cycle is None:
            if hasattr(self.controller, "validate_cycle"):
                try:
                    is_valid, errors = self.controller.validate_cycle()
                    if not is_valid:
                        save_errors.extend(errors)
                except Exception as e:
                    save_errors.append(f"Validation failed: {e}")

            self._show_save_failed_warning(save_errors)
            return

        current = self.parent
        while current is not None:
            if hasattr(current, "show_home"):
                current.show_home()
                return

            if hasattr(current, "parent"):
                parent_ref = current.parent
                current = parent_ref() if callable(parent_ref) else parent_ref
            else:
                current = None

    def _show_save_failed_warning(self, errors=None):
        """
        Show a warning when cycle save fails and return user to summary.
        """
        if not errors:
            warning_message = "Could not save cycle.\nPlease review your inputs and try again."
        else:
            details = "\n".join(f"- {msg}" for msg in errors[:3])
            warning_message = f"Could not save cycle:\n{details}"

        current = self.parent
        while current is not None:
            if hasattr(current, "show_warning"):
                current.show_warning(
                    warning_message=warning_message,
                    button_mode="red",
                    red_button_text="GO BACK",
                    on_cancel=self._return_to_summary,
                )
                return

            if hasattr(current, "parent"):
                parent_ref = current.parent
                current = parent_ref() if callable(parent_ref) else parent_ref
            else:
                current = None

    def _return_to_summary(self):
        """
        This function handles the NO action and returns to the summary page.

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
                parent_ref = current.parent
                current = parent_ref() if callable(parent_ref) else parent_ref
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