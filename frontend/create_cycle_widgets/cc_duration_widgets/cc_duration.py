from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import (
    QPixmap,
    QFont,
    QIcon, 
    QPainter,
    QColor
)
from PySide6.QtGui import QFontDatabase

class CCDurationPage(QWidget):
    def __init__(self,controller,parent):
        """
        Initializes the CCDurationPage widget with a parent and controller.
        Initialize minutes and seconds
        Sets up window size, background, buttons and duration screen.
        Further call all the helper functions and link the logic

        Args:
            controller (QWidget): Handles the application logic and connects the frontend UI to the backend through signals and data flow. Defaults to None.
            parent (QWidget): The parent widget that contains this page. Used for UI hierarchy, positioning, and memory management. Defaults to None.
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

        self.step_title = QLabel("Step 1: Select cycle duration")
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

        self.content_box.setLayout(content_layout)
        self.main_layout.addWidget(self.content_box)
        self.minutes = 0
        self.seconds = 0

        self.set_logicbuttons()
        self.setup_DurationScreen()
        self.on_page_enter()
        
    def set_logicbuttons(self):
        """
        This function handles logic for making all control buttons clickable ad setting their positions
        """

        #help button
        self.help_btn = QPushButton("",self)
        self.help_btn.setGeometry(164,23.18,49,45.44)
        self.help_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 30);
                border-radius: 25px;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 60);
                border-radius: 25px;
            }
        """)
        self.help_btn.clicked.connect(self.go_help)

    def setup_DurationScreen(self):
        """
        This function sets the main screen orientation of time screen
        It handles time box, label, plus/minus buttons
        """
        font_id = QFontDatabase.addApplicationFont("resources/timeduration_assets/DigitalNumbers.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        self.durationText = QLabel("Enter Cycle Duration", self)
        self.durationText.setGeometry(328,199,415,76)
        self.durationText.setStyleSheet("Font-Family: Ubuntu; font-size: 44px; color: black")
        self.durationText.setAlignment(Qt.AlignCenter)

        self.time_img = QLabel(self)
        self.time_img.setGeometry(366,291,307,94)
        self.time_img.setPixmap(QPixmap("resources/timeduration_assets/timebox.png").scaled(
            307, 94, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        ))

        self.time_label = QLabel("05:00", self)
        self.time_label.setGeometry(366, 291, 307, 94)  # same position!
        self.time_label.setStyleSheet(f"background: transparent; color: #34C759; font-size: 48px; font-family: '{font_family}'; padding-bottom: 10px;")
        self.time_label.setAlignment(Qt.AlignCenter)

        self.minus_btn = QPushButton("", self)
        self.minus_btn.setGeometry(280,314,48,48)
        self.minus_btn.setIcon(QIcon("resources/timeduration_assets/minus_sign.png"))
        self.minus_btn.setIconSize(QSize(48,48))
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
                    background: rgba(255, 255, 255, 60);  /* similar to selected/pressed look */
                    border-radius: 24px;
                }
        """)
        self.minus_btn.clicked.connect(self.dec_time)

        self.minus_ripple = QLabel("", self)
        self.minus_ripple.setGeometry(280,314,48,48)
        self.minus_ripple.setStyleSheet("background:  rgba(255,255,255,100); border-radius: 24px")
        self.minus_ripple.hide()

        self.plus_btn = QPushButton("", self)
        self.plus_btn.setGeometry(682,314,48,48)
        self.plus_btn.setIcon(self._build_icon_with_disabled("resources/timeduration_assets/plus_sign.png"))
        self.plus_btn.setIconSize(QSize(48,48))
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
                background: rgba(255, 255, 255, 30);
                border-radius: 24px;
            }
            QPushButton:disabled {
                background: rgba(255, 255, 255, 60);
                border-radius: 24px;
            }
        """)
        self.plus_btn.clicked.connect(self.inc_time)

        self.plus_ripple = QLabel("", self)
        self.plus_ripple.setGeometry(682,314,48,48)
        self.plus_ripple.setStyleSheet("background:  rgba(255,255,255,100); border-radius: 24px")
        self.plus_ripple.hide()

    #Place holders

    def go_next(self):
        """
        This function handles the logic to land on next page
        """
        self.parent.next_pressed()

    def reset_customization(self):
        """
        This function cancels the customization and reset to default
        """
        print("reset")

    def go_help(self):
        """
        This function handle when help button is clicked user is taken to the help screen
        """
        print("help")

    def inc_time(self):
        """
        Increase the duration by 30 seconds using controller.set_duration.
        """
        self.show_ripple("plus")
        # Get current duration from controller
        if hasattr(self.controller, "get_duration") and hasattr(self.controller, "set_duration"):
            try:
                current_duration = self.controller.get_duration()
                new_duration = min(900, current_duration + 30)
                self.controller.set_duration(new_duration)
                self._update_time_from_controller()
                self.cycledisplayScreen()
                self.check_boundaries()
                print("add time")
            except Exception as e:
                print(f"[inc_time] Error: {e}")
        
    def dec_time(self):
        """
        Decrease the duration by 30 seconds using controller.set_duration.
        """
        self.show_ripple("minus")
        if hasattr(self.controller, "get_duration") and hasattr(self.controller, "set_duration"):
            try:
                current_duration = self.controller.get_duration()
                new_duration = max(60, current_duration - 30)
                self.controller.set_duration(new_duration)
                self._update_time_from_controller()
                self.cycledisplayScreen()
                self.check_boundaries()
                print("minus time")
            except Exception as e:
                print(f"[dec_time] Error: {e}")

    def show_ripple(self,btn_type):
        """
        This function is used to create a ripple effect arouund plus and minus buttons when clicked

        btn_type: The argument keeps teh track of which button is clicked
        """
        if btn_type=="plus":
            self.plus_ripple.show()
            self.plus_ripple.raise_()
            QTimer.singleShot(200, self.plus_ripple.hide)
        else:
            self.minus_ripple.show()
            self.minus_ripple.raise_()
            QTimer.singleShot(200, self.minus_ripple.hide)

    def check_boundaries(self):
        """
        This function helps check the boundary
        This ensures the greying out of minus button when time is 1 MINUTE prohibiting access to reduce time 
        since that's a minimum limit 
        Similarly, greying out of plus button when time screen shows 15 MINUTES since that is s max time limit a user can set
        """
        at_min = (self.minutes == 1 and self.seconds == 0)
        at_max = (self.minutes == 15 and self.seconds == 0)

        self.minus_btn.setEnabled(not at_min)
        self.plus_btn.setEnabled(not at_max)      

    def cycledisplayScreen(self):
        """
        This function displays the time on time screen box
        """
        self.time_label.setText(f"{self.minutes:02}:{self.seconds:02}") 

    def on_page_enter(self):
        """
        This function takes the time from controller and converts the duration into 
        minutes and seconds format before displaying
        """
        self._update_time_from_controller()
        self.cycledisplayScreen()
        self.check_boundaries()

    def _update_time_from_controller(self):
        """
        Helper to update self.minutes and self.seconds from controller.get_duration().
        """
        if hasattr(self.controller, "get_duration"):
            try:
                total_dur = self.controller.get_duration()
                self.minutes = total_dur // 60
                self.seconds = total_dur % 60
            except Exception as e:
                print(f"[_update_time_from_controller] Error: {e}")

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
        # Print the duration sent to the backend when next is pressed
        duration = None
        if hasattr(self.controller, "get_duration"):
            try:
                duration = self.controller.get_duration()
            except Exception as e:
                print(f"[mapping_confirmed] Error getting duration: {e}")
        print(f"next was pressed, duration sent to backend: {duration}")
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

    def default_button_pressed(self):
        """
        Set default cycle time using controller.set_duration.
        """
        if hasattr(self.controller, "set_duration"):
            try:
                self.controller.set_duration(300)
                self._update_time_from_controller()
                self.cycledisplayScreen()
                self.check_boundaries()
                print("default clicked")
            except Exception as e:
                print(f"[default_button_pressed] Error: {e}")