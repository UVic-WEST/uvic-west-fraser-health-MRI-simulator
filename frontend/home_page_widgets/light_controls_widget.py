from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QSizePolicy,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QPen
from frontend.helpers import ReadOnlySlider

LIGHT_DROPDOWN_COLOUR = "#FAF5F5"

class LightControlsWidget(QWidget):
    brightness_changed = Signal(int)
    light_power_changed = Signal(bool)

    def __init__(self, controller, parent=None):
        """
        This function builds the Light Controls widget and initializes its state

        Args:
            controller (ManualLightController): controller for manual light logic
            parent (QWidget): the parent widget for this controls container
        """
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._expanded = False
        self._light_is_on = False
        self.controller = controller

        # outer layout - header on top, collapsible brightness controls below
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # header button
        self.header_button = QPushButton("Light Controls")
        self.header_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header_button.setFont(QFont("Ubuntu", 16))
        self._apply_header_style(expanded=False)
        self._arrow_icon = QIcon(QPixmap("resources/frontend_common_assets/blacktriangle.png"))
        self._close_icon = self._build_close_icon()
        self.header_button.setIcon(self._arrow_icon)
        self.header_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        main_layout.addWidget(self.header_button)

        # collapsible controls area
        self._controls_widget = QWidget()
        self._controls_widget.setObjectName("light_controls_panel")
        self._controls_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._controls_widget.setStyleSheet("""
            QWidget#light_controls_panel {
                background-color: white;
                border-left: 2px solid #0474BA;
                border-right: 2px solid #0474BA;
                border-bottom: 2px solid #0474BA;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
            }
        """)
        controls_layout = QVBoxLayout(self._controls_widget)
        controls_layout.setSpacing(12)
        controls_layout.setContentsMargins(12, 12, 12, 12)

        # brightness controls: '-' | slider | '+'
        brightness_row = QHBoxLayout()
        brightness_row.setSpacing(8)
        brightness_row.setContentsMargins(0, 4, 0, 0)

        # single ON/OFF toggle button aligned with slider controls
        self.light_power_button = QPushButton()
        self.light_power_button.setFont(QFont("Ubuntu", 13, QFont.Weight.Bold))
        self.light_power_button.setFixedHeight(36)
        self.light_power_button.setMinimumWidth(72)
        self.light_power_button.clicked.connect(self._toggle_light_power)
        self._update_light_power_button_style()

        self.decrease_brightness_button = QPushButton("-")
        self.decrease_brightness_button.setFont(QFont("Ubuntu", 18, QFont.Weight.Bold))
        self.decrease_brightness_button.setFixedSize(44, 34)
        self.decrease_brightness_button.setStyleSheet("""
            QPushButton {
                background-color: #0474BA;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:pressed {
                background-color: #024a74;
            }
        """)

        self.increase_brightness_button = QPushButton("+")
        self.increase_brightness_button.setFont(QFont("Ubuntu", 18, QFont.Weight.Bold))
        self.increase_brightness_button.setFixedSize(44, 34)
        self.increase_brightness_button.setStyleSheet("""
            QPushButton {
                background-color: #0474BA;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:pressed {
                background-color: #024a74;
            }
        """)

        self.brightness_slider = ReadOnlySlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setSingleStep(10)
        self.brightness_slider.setPageStep(10)
        self.brightness_slider.setTickInterval(10)
        self.brightness_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.brightness_slider.setValue(50)

        self.decrease_brightness_button.clicked.connect(self._decrease_brightness)
        self.increase_brightness_button.clicked.connect(self._increase_brightness)
        self.brightness_slider.valueChanged.connect(self._on_brightness_changed)

        brightness_row.addWidget(self.light_power_button)
        brightness_row.addWidget(self.decrease_brightness_button)
        brightness_row.addWidget(self.brightness_slider)
        brightness_row.addWidget(self.increase_brightness_button)
        controls_layout.addLayout(brightness_row)

        self._controls_widget.hide()
        main_layout.addWidget(self._controls_widget)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header_button.clicked.connect(self._toggle_panel)

    def _apply_header_style(self, expanded: bool):
        """
        This function updates the header button style based on panel state

        Args:
            expanded: whether the light controls panel is expanded
        """
        if expanded:
            self.header_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {LIGHT_DROPDOWN_COLOUR};
                    color: black;
                    border-top: 2px solid #0474BA;
                    border-left: 2px solid #0474BA;
                    border-right: 2px solid #0474BA;
                    border-bottom: none;
                    border-top-left-radius: 12px;
                    border-top-right-radius: 12px;
                    border-bottom-left-radius: 0px;
                    border-bottom-right-radius: 0px;
                    padding: 4px 10px;
                    text-align: left;
                }}
            """)
        else:
            self.header_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {LIGHT_DROPDOWN_COLOUR};
                    color: black;
                    border: 2px solid #0474BA;
                    border-radius: 12px;
                    padding: 4px 10px;
                    text-align: left;
                }}
            """)

    def _toggle_panel(self):
        """
        This function toggles the expanded/collapsed state of the controls panel
        """
        self._expanded = not self._expanded
        self._apply_header_style(expanded=self._expanded)
        self._controls_widget.setVisible(self._expanded)
        self.header_button.setIcon(self._close_icon if self._expanded else self._arrow_icon)

    def _build_close_icon(self) -> QIcon:
        """
        This function creates and returns the close (x) icon

        Returns:
            icon: the close icon for the expanded header button
        """
        pixmap = QPixmap(12, 12)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(2, 2, 10, 10)
        painter.drawLine(10, 2, 2, 10)
        painter.end()
        return QIcon(pixmap)

    def _update_light_power_button_style(self):
        """
        This function updates the light power button text and style
        """
        if self._light_is_on:
            self.light_power_button.setText("OFF")
            self.light_power_button.setStyleSheet("""
                QPushButton {
                    background-color: #D9534F;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 6px 12px;
                }
                QPushButton:pressed {
                    background-color: #A72824;
                }
            """)
        else:
            self.light_power_button.setText("ON")
            self.light_power_button.setStyleSheet("""
                QPushButton {
                    background-color: #2E9B41;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 6px 12px;
                }
                QPushButton:pressed {
                    background-color: #1D682B;
                }
            """)

    def _set_light_power(self, is_on: bool):
        """
        This function sets the light power state and emits its signal

        Args:
            is_on: True to set lights on, False to set lights off
        """
        self._light_is_on = is_on
        self._update_light_power_button_style()
        print("Light power changed:", "ON" if self._light_is_on else "OFF")
        self.light_power_changed.emit(self._light_is_on)

    def _toggle_light_power(self):
        """
        This function toggles the current light power state
        """
        self._set_light_power(not self._light_is_on)

    def _on_brightness_changed(self, value: int):
        """
        This function handles brightness updates and snaps values to 10-point increments

        Args:
            value: the requested slider brightness value
        """
        snapped = max(0, min(100, int(round(value / 10.0) * 10)))
        if snapped != value:
            self.brightness_slider.blockSignals(True)
            self.brightness_slider.setValue(snapped)
            self.brightness_slider.blockSignals(False)
        print("Light brightness changed:", snapped)
        self.brightness_changed.emit(snapped)

    def _decrease_brightness(self):
        """
        This function decreases brightness by 10
        """
        self.brightness_slider.setValue(max(0, self.brightness_slider.value() - 10))

    def _increase_brightness(self):
        """
        This function increases brightness by 10
        """
        self.brightness_slider.setValue(min(100, self.brightness_slider.value() + 10))
