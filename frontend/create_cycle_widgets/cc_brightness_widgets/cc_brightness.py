from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QSlider,
    QVBoxLayout
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import (
    QPixmap,
    QFont,
    QIcon, 

)

from frontend.help_widgets.help_screen import HelpOverlay
from frontend.help_widgets.help_button import HelpButton

from frontend.helpers import ReadOnlySlider

class CCBrightnessPage(QWidget):
    def __init__(self, controller, parent=None):

        """
        This function initializes the CCBrightnessPage and sets up all UI components.

        Args:
            controller: the application controller for handling brightness logic
            parent: the parent widget for navigation handling
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

        self.help_manual_path = "resources/manuals/create_cycle_manual.pdf"
        self.help_overlay = HelpOverlay(self.help_manual_path,self)
        #setting up help button
        self.help_button = HelpButton(self)
        self.help_button.move(140, 20)
        self.help_button.raise_()
        self.help_button.clicked.connect(self.help_pressed)


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

        self.step_title = QLabel("Step 3: set lights")
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

        self.page_status = QLabel("Set light brightness for each group")
        self.page_status.setFont(QFont("Ubuntu", 24))
        self.page_status.setStyleSheet("color: #0474BA;")
        self.page_status.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.page_status)

        self.content_box.setLayout(content_layout)
        self.main_layout.addWidget(self.content_box)
        self.setup_BrightnessScreen()
        # Set slider to backend value on init
        if self.controller:
            try:
                backend_val = self.controller.get_light_level()
                self.brightness_slider.setValue(backend_val)
            except Exception as e:
                print(f"[CCBrightnessPage] Error getting light level from backend: {e}")

    def help_pressed(self):
        """
        Shows the help screen overlay for this page
        """
        self.help_overlay.show()
        self.help_overlay.raise_()
        
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
        self._reset_lights()
        if self.parent and hasattr(self.parent, "back_pressed"):
            self.parent.back_pressed()

    def mapping_confirmed(self):
        print("next was pressed")
        if self.parent and hasattr(self.parent, "next_pressed"):
            self.parent.next_pressed()

    def cancel_to_home(self):
        print("cancel was pressed")
        self._reset_lights()
        current = self.parent
        while current is not None:
            if hasattr(current, "show_home"):
                current.show_home()
                return
            if hasattr(current, "parent"):
                current = current.parent()
            else:
                current = None

    def _reset_lights(self):
        """Turn lights off so hardware doesn't stay at the preview brightness."""
        if self.controller and hasattr(self.controller, "light_controller"):
            lc = self.controller.light_controller
            if lc and hasattr(lc, "system_idle"):
                lc.system_idle()

    def default_button_pressed(self):
        """
        This function resets brightness to default value when default button is pressed
        """
        print("default button was pressed")
        self.reset_light_default()
        self.update_button_states()


    def setup_BrightnessScreen(self):
        """
        Creates the brightness slider card shown in the centre of the screen.
        Mirrors the slider logic from LightControlsWidget for consistency.
        """
       
        #Brightness label
        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap("resources/custom_brightness_assets/brightnesslogo.png")
        self.logo_label.setPixmap(self.logo_pixmap.scaled(
            58, 57, 
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

        self.logo_label.setGeometry(483, 286, 58, 57)
        self.logo_label.setStyleSheet("background: transparent;")
       


        #White background

        self.sliderCard = QLabel(self)
        self.sliderCard.setStyleSheet("""
                background-color: white;
                border-radius: 18px;
            """)

        self.sliderCard.setGeometry(199, 271, 627, 173)
        self.sliderCard.setAlignment(Qt.AlignCenter)

        self.logo_label.raise_() #make sure sits on background

        ##=========MINUS Button
        self.minus_btn = QPushButton("",self)
        self.minus_btn.setGeometry(225,343,23,44)
        self.minus_btn.setIcon(QIcon("resources/custom_brightness_assets/minus.png"))
        self.minus_btn.setIconSize(QSize(23, 44))
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
        self.minus_btn.clicked.connect(self.dec_brightness)

        self.minus_ripple = QLabel("",self)
        self.minus_ripple.setGeometry(225,343,23,44)
        self.minus_ripple.setStyleSheet("background:  rgba(255,255,255,100); border-radius: 24px")
        self.minus_ripple.hide()

        ##=============PLUS Button
        self.plus_btn = QPushButton("",self)
        self.plus_btn.setGeometry(771,337,23,44)
        self.plus_btn.setIcon(QIcon("resources/custom_brightness_assets/plus.png"))
        self.plus_btn.setIconSize(QSize(23, 44))
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
                    background: rgba(255, 255, 255, 60);  /* similar to selected/pressed look */
                    border-radius: 24px;
                }
        """)
        self.plus_btn.clicked.connect(self.inc_brightness)

        self.plus_ripple = QLabel("",self)
        self.plus_ripple.setGeometry(771,337,23,44)
        self.plus_ripple.setStyleSheet("background:  rgba(255,255,255,100); border-radius: 24px")
        self.plus_ripple.hide()

        ##=====SLIDER============
        self.brightness_slider = ReadOnlySlider(Qt.Orientation.Horizontal, self)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setSingleStep(10)
        self.brightness_slider.setPageStep(10)
        self.brightness_slider.setTickInterval(10)
        self.brightness_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.brightness_slider.setValue(50)    #default midpoint
        self.brightness_slider.setGeometry(225, 384, 575, 44)
        self.brightness_slider.setStyleSheet(
        """
        QSlider::groove:horizontal {
            height: 8px;
            background: #D3D9DE;
            border-radius: 4px;
        }
        QSlider::sub-page:horizontal {
            background: #0474BA;
            border-radius: 4px;
        }
        QSlider::add-page:horizontal {
            background: #D3D9DE;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #FFFFFF;
            border: 2px solid #0474BA;
            width: 18px;
            margin: -6px 0;
            border-radius: 9px;
        }
        QSlider::handle:horizontal:hover {
            background: #F3F9FD;
        }
        QSlider::tick-mark:horizontal {
            background: #2F3B45;
            width: 1px;
            height: 6px;
        }
        """)
        self.brightness_slider.valueChanged.connect(self.brightness_changed)
        self.update_button_states()

    

  

    def brightness_changed(self, value: int):
        """
        This function handles brightness updates and snaps values to 10-point increments.
        Sends the snapped value to the controller.

        Args:
            value: the raw slider value to be snapped and applied
        """
        val = max(0, min(100, int(round(value/10.0)*10)))
        if val != value:
            self.brightness_slider.blockSignals(True)
            self.brightness_slider.setValue(val)
            self.brightness_slider.blockSignals(False)
        if self.controller:
            try:
                self.controller.set_light_level(val)
                self.controller.display_light_level(val)
                print(f"[CustomCycle] Set brightness to backend: {val}")
            except Exception as e:
                print(f"[CCBrightnessPage] Error setting/displaying light level: {e}")


    def dec_brightness(self):
        """
        This button ensures brightness is decreased when clicked minus
        Also handles ripple effect and greying out
        """
        self.show_ripple("minus")
        new_val = max(0, self.brightness_slider.value() - 10)
        self.brightness_slider.setValue(new_val)
        if self.controller:
            try:
                self.controller.set_light_level(new_val)
                self.controller.display_light_level(new_val)
            except Exception as e:
                print(f"[CCBrightnessPage] Error setting/displaying light level: {e}")
        self.update_button_states()

    def inc_brightness(self):
        """
        This button ensures brightness is increased when clicked plus
        Also handles ripple effect and greying out
        """
        self.show_ripple("plus")
        new_val = min(100, self.brightness_slider.value() + 10)
        self.brightness_slider.setValue(new_val)
        if self.controller:
            try:
                self.controller.set_light_level(new_val)
                self.controller.display_light_level(new_val)
            except Exception as e:
                print(f"[CCBrightnessPage] Error setting/displaying light level: {e}")
        self.update_button_states()

    def reset_light_default(self):
        """
        This function sets the deafult value when default is pressed
        """
        self.brightness_slider.setValue(50)

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

    def update_button_states(self):
        """
        This function ensures the minus plus buttons greyed out when hits limit
        """
        val = self.brightness_slider.value()
        self.minus_btn.setEnabled(val > 0)    # grey out minus at 0
        self.plus_btn.setEnabled(val < 100)   # grey out plus at 100

