from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap,
    QFont,
)


DURATION_PAGE_INDEX = 0
GROUPS_PAGE_INDEX = 1
LIGHTS_PAGE_INDEX = 2
SOUNDS_PAGE_INDEX = 3


class CCSummary(QWidget):
    def __init__(self, controller, parent=None):
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
        self.content_box.setStyleSheet(
            """
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
            """
        )
        self.content_box.setFixedSize(700, 320)

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(16)

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

        self.duration_summary_btn = QPushButton("Cycle Duration: 03:00")
        self.duration_summary_btn.setFixedHeight(48)
        self.duration_summary_btn.setStyleSheet(summary_button_style)
        self.duration_summary_btn.clicked.connect(self.edit_duration)

        self.groups_summary_btn = QPushButton("Cycle Groups: 4")
        self.groups_summary_btn.setFixedHeight(48)
        self.groups_summary_btn.setStyleSheet(summary_button_style)
        self.groups_summary_btn.clicked.connect(self.edit_groups)

        self.lights_summary_btn = QPushButton("Cycle Lights: 60%")
        self.lights_summary_btn.setFixedHeight(48)
        self.lights_summary_btn.setStyleSheet(summary_button_style)
        self.lights_summary_btn.clicked.connect(self.edit_lights)

        self.sounds_summary_btn = QPushButton("Cycle Sounds: 4 groups")
        self.sounds_summary_btn.setFixedHeight(48)
        self.sounds_summary_btn.setStyleSheet(summary_button_style)
        self.sounds_summary_btn.clicked.connect(self.edit_sounds)

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
        content_layout.addWidget(self.groups_summary_btn)
        content_layout.addWidget(self.lights_summary_btn)
        content_layout.addWidget(self.sounds_summary_btn)
        content_layout.addWidget(self.confirm_btn)

        self.content_box.setLayout(content_layout)
        self.main_layout.addWidget(self.content_box)

    def set_background(self, image_path):
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
        print("back was pressed")
        if self.parent and hasattr(self.parent, "back_pressed"):
            self.parent.back_pressed()

    def mapping_confirmed(self):
        print("next was pressed")
        if self.parent and hasattr(self.parent, "next_pressed"):
            self.parent.next_pressed()

    def cancel_to_home(self):
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