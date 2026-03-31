from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap,
    QFont,
    QIcon,
    QPainter,
    QColor
)


class CCGroupsPage(QWidget):
    def __init__(self, controller, parent=None):
        """
        This function builds the groups selection page and initializes its UI state

        Args:
            controller: the controller used by this page
            parent: the parent widget for this page
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

        self.back_btn = QPushButton("Back", self)
        self.back_btn.setGeometry(20, 536, 120, 44)
        self.back_btn.setStyleSheet(self.cancel_home_btn.styleSheet())
        self.back_btn.clicked.connect(self.mapping_cancelled)
        self.back_btn.raise_()

        self.next_btn = QPushButton("Next", self)
        self.next_btn.setGeometry(884, 536, 120, 44)
        self.next_btn.setStyleSheet(self.cancel_home_btn.styleSheet())
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
        self.page_title.setFont(QFont("Ubuntu", 32))
        self.page_title.setStyleSheet("color: white; background: transparent;")
        self.page_title.setAlignment(Qt.AlignCenter)

        self.step_title = QLabel("Step 2: set the number of groups")
        self.step_title.setFont(QFont("Ubuntu", 14))
        self.step_title.setStyleSheet("color: white; background: transparent;")
        self.step_title.setAlignment(Qt.AlignCenter)

        self.title_layout = QVBoxLayout()
        self.title_layout.setSpacing(0)
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
        content_layout.setSpacing(40)
        self.group_value = 4

        self.prompt= QLabel("How many sound groups would you like\nto have for the new cycle?")
        self.prompt.setFont(QFont("Ubuntu", 20))
        self.prompt.setStyleSheet("color: black;")
        self.prompt.setAlignment(Qt.AlignCenter)
        self.prompt.setWordWrap(True)
        content_layout.addWidget(self.prompt)

        stepper_layout = QHBoxLayout()
        stepper_layout.setAlignment(Qt.AlignCenter)
        stepper_layout.setSpacing(24)

        self.minus_btn = QPushButton("")
        self.plus_btn = QPushButton("")
        self.value_label = QLabel(str(self.group_value))
        self.value_label.setFont(QFont("Ubuntu", 24))
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setFixedSize(260, 64)
        self.value_label.setStyleSheet(
            """
            QLabel {
                background-color: #F7F5F5;
                color: black;
                border-radius: 24px;
                padding-bottom: 2px;
            }
            """
        )

        self.minus_btn.setFixedSize(48, 48)
        self.plus_btn.setFixedSize(48, 48)

        self.minus_btn.setIcon(QIcon("resources/timeduration_assets/minus_sign.png"))
        self.minus_btn.setIconSize(self.minus_btn.size())
        self.plus_btn.setIcon(QIcon("resources/timeduration_assets/plus_sign.png"))
        self.plus_btn.setIconSize(self.plus_btn.size())

        self.minus_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 24px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 30);
                border-radius: 24px;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 60);
                border-radius: 24px;
            }
            QPushButton:disabled {
                background: rgba(255, 255, 255, 60);
                border-radius: 24px;
            }
        """)
        self.minus_btn.setIcon(self._build_icon_with_disabled("resources/timeduration_assets/minus_sign.png"))


        self.plus_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 24px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 30);
                border-radius: 24px;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 60);
                border-radius: 24px;
            }
            QPushButton:disabled {
                background: rgba(255, 255, 255, 60);
                border-radius: 24px;
            }
        """)
        self.plus_btn.setIcon(self._build_icon_with_disabled("resources/timeduration_assets/plus_sign.png"))


        self.minus_btn.clicked.connect(self.decrease)
        self.plus_btn.clicked.connect(self.increase)

        stepper_layout.addWidget(self.minus_btn)
        stepper_layout.addWidget(self.value_label)
        stepper_layout.addWidget(self.plus_btn)
        content_layout.addLayout(stepper_layout)

        self.range_hint = QLabel("Please choose between 1 and 8")
        self.range_hint.setFont(QFont("Ubuntu", 20))
        self.range_hint.setStyleSheet("color: black;")
        self.range_hint.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.range_hint)
        
        #Added part ends here

        self.content_box.setLayout(content_layout)
        self.main_layout.addWidget(self.content_box)
        self._update_stepper_button_states()

    def _update_stepper_button_states(self):
        """
        This function updates plus and minus button enabled states based on current group value
        """
        self.minus_btn.setEnabled(self.group_value > 1)
        self.plus_btn.setEnabled(self.group_value < 8)

    def set_background(self, image_path):
        """
        This function sets and displays the background image for the page

        Args:
            image_path: the file path to the background image
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
        This function handles when the Back button is pressed
        """
        print("back was pressed")
        if self.parent and hasattr(self.parent, "back_pressed"):
            self.parent.back_pressed()

    def mapping_confirmed(self):
        """
        This function handles when the Next button is pressed
        """
        print("next was pressed")
        if self.parent and hasattr(self.parent, "next_pressed"):
            self.parent.next_pressed()

    def cancel_to_home(self):
        """
        This function handles cancel behavior and routes back to home if available
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

    def default_button_pressed(self):
        """
        This function resets the selected group value to the default setting
        """
        print("default button was pressed")
        self.group_value = 4
        self.value_label.setText(str(self.group_value))
        self._update_stepper_button_states()

    def increase(self):
        """
        This function increases the group value by one, up to the maximum allowed value
        """
        if self.group_value < 8:
            self.group_value += 1
            self.value_label.setText(str(self.group_value))
        self._update_stepper_button_states()

    def decrease(self):
        """
        This function decreases the group value by one, down to the minimum allowed value
        """
        if self.group_value > 1:
            self.group_value -= 1
            self.value_label.setText(str(self.group_value))
        self._update_stepper_button_states()

    def _build_icon_with_disabled(self, path: str) -> QIcon:
        """
        Sets up the disabled mask for the plus and minus buttons when they are at boundary
        Args:
            path(str): path to the icon for the button
        """
        normal = QPixmap(path)

        # Keep transparency, then tint to gray
        disabled = QPixmap(normal.size())
        disabled.fill(Qt.transparent)

        painter = QPainter(disabled)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.drawPixmap(0, 0, normal)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(disabled.rect(), QColor(150, 150, 150, 210))
        painter.end()

        icon = QIcon()
        icon.addPixmap(normal, QIcon.Normal, QIcon.Off)
        icon.addPixmap(disabled, QIcon.Disabled, QIcon.Off)
        return icon
