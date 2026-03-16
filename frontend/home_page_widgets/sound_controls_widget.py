from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QSlider,
    QSizePolicy,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QPen

SOUND_DROPDOWN_COLOUR = "#FAF5F5"
SOUND_PANEL_BUTTON_COLOUR = SOUND_DROPDOWN_COLOUR
SOUND_SELECTED_BUTTON_COLOUR = "#2E9B41"
SOUND_PANEL_COLS = 4
SOUND_NAMES = ["Sound 1", "Sound 2", "Sound 3", "Sound 4", "Sound 5", "Sound 6", "Sound 7", "Sound 8"]


class _ReadOnlySlider(QSlider):
    """Visual slider that ignores direct user interaction."""

    def mousePressEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()

    def wheelEvent(self, event):
        event.ignore()

    def keyPressEvent(self, event):
        event.ignore()


class SoundControlsWidget(QWidget):
    sound_selected = Signal(str)
    volume_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._expanded = False
        self._selected_sound = None
        self._sound_buttons = {}

        # outer layout — header on top, collapsible buttons below
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ── header button ──
        self.header_button = QPushButton("Sound Controls")
        self.header_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header_button.setFont(QFont("Ubuntu", 16))
        self._apply_header_style(expanded=False)
        self._arrow_icon = QIcon(QPixmap("resources/frontend_common_assets/blacktriangle.png"))
        self._close_icon = self._build_close_icon()
        self.header_button.setIcon(self._arrow_icon)
        self.header_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        main_layout.addWidget(self.header_button)

        # ── collapsible buttons area ──
        self._buttons_widget = QWidget()
        self._buttons_widget.setObjectName("sound_controls_panel")
        self._buttons_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._buttons_widget.setStyleSheet("""
            QWidget#sound_controls_panel {
                background-color: white;
                border-left: 2px solid #0474BA;
                border-right: 2px solid #0474BA;
                border-bottom: 2px solid #0474BA;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
            }
        """)
        panel_layout = QVBoxLayout(self._buttons_widget)
        panel_layout.setSpacing(12)
        panel_layout.setContentsMargins(12, 12, 12, 12)

        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(10)

        for i, name in enumerate(SOUND_NAMES):
            btn = QPushButton(name)
            btn.setFont(QFont("Ubuntu", 14))
            btn.setStyleSheet(self._sound_button_stylesheet(is_selected=False))
            btn.clicked.connect(lambda checked, n=name: self._on_sound_button_clicked(n))
            self._sound_buttons[name] = btn
            buttons_layout.addWidget(btn, i // SOUND_PANEL_COLS, i % SOUND_PANEL_COLS)

        panel_layout.addLayout(buttons_layout)

        # volume controls underneath sound buttons: '-' | slider | '+'
        volume_row = QHBoxLayout()
        volume_row.setSpacing(8)
        volume_row.setContentsMargins(0, 4, 0, 0)

        self.decrease_volume_button = QPushButton("-")
        self.decrease_volume_button.setFont(QFont("Ubuntu", 18, QFont.Weight.Bold))
        self.decrease_volume_button.setFixedSize(44, 34)
        self.decrease_volume_button.setStyleSheet("""
            QPushButton {
                background-color: #0474BA;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #035a8e;
            }
            QPushButton:pressed {
                background-color: #024a74;
            }
        """)

        self.increase_volume_button = QPushButton("+")
        self.increase_volume_button.setFont(QFont("Ubuntu", 18, QFont.Weight.Bold))
        self.increase_volume_button.setFixedSize(44, 34)
        self.increase_volume_button.setStyleSheet("""
            QPushButton {
                background-color: #0474BA;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #035a8e;
            }
            QPushButton:pressed {
                background-color: #024a74;
            }
        """)

        self.volume_slider = _ReadOnlySlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setSingleStep(10)
        self.volume_slider.setPageStep(10)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)

        self.decrease_volume_button.clicked.connect(self._decrease_volume)
        self.increase_volume_button.clicked.connect(self._increase_volume)

        volume_row.addWidget(self.decrease_volume_button)
        volume_row.addWidget(self.volume_slider)
        volume_row.addWidget(self.increase_volume_button)
        panel_layout.addLayout(volume_row)

        self._buttons_widget.hide()
        main_layout.addWidget(self._buttons_widget)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header_button.clicked.connect(self._toggle_panel)

    def _apply_header_style(self, expanded: bool):
        if expanded:
            # top of an open box: only top border + left/right, rounded top corners only
            self.header_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {SOUND_DROPDOWN_COLOUR};
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
                    background-color: {SOUND_DROPDOWN_COLOUR};
                    color: black;
                    border: 2px solid #0474BA;
                    border-radius: 12px;
                    padding: 4px 10px;
                    text-align: left;
                }}
            """)

    def _toggle_panel(self):
        self._expanded = not self._expanded
        self._apply_header_style(expanded=self._expanded)
        self._buttons_widget.setVisible(self._expanded)
        self.header_button.setIcon(self._close_icon if self._expanded else self._arrow_icon)

    def _build_close_icon(self) -> QIcon:
        """Create a simple x icon for the expanded panel state."""
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

    def _sound_button_stylesheet(self, is_selected: bool) -> str:
        base_colour = SOUND_SELECTED_BUTTON_COLOUR if is_selected else SOUND_PANEL_BUTTON_COLOUR
        hover_colour = "#237A33" if is_selected else "#EDEDED"
        text_colour = "white" if is_selected else "black"
        border_style = "none" if is_selected else "1px solid #CFCFCF"
        return f"""
            QPushButton {{
                background-color: {base_colour};
                color: {text_colour};
                border: {border_style};
                border-radius: 10px;
                padding: 10px 16px;
            }}
            QPushButton:hover {{
                background-color: {hover_colour};
            }}
        """

    def _refresh_sound_button_styles(self):
        for name, btn in self._sound_buttons.items():
            btn.setStyleSheet(self._sound_button_stylesheet(is_selected=(name == self._selected_sound)))

    def _on_sound_button_clicked(self, sound_name):
        if self._selected_sound == sound_name:
            # Clicking the active sound turns it off.
            self._selected_sound = None
            self._refresh_sound_button_styles()
            print("Sound turned off:", sound_name)
            self.sound_selected.emit("")
            return

        self._selected_sound = sound_name
        self._refresh_sound_button_styles()
        print("Sound selected:", sound_name)
        self.sound_selected.emit(sound_name)

    def _on_volume_changed(self, value: int):
        # Snap to 10-point increments even when dragging.
        snapped = max(0, min(100, int(round(value / 10.0) * 10)))
        if snapped != value:
            self.volume_slider.blockSignals(True)
            self.volume_slider.setValue(snapped)
            self.volume_slider.blockSignals(False)
        print("Sound volume changed:", snapped)
        self.volume_changed.emit(snapped)

    def _decrease_volume(self):
        self.volume_slider.setValue(max(0, self.volume_slider.value() - 10))

    def _increase_volume(self):
        self.volume_slider.setValue(min(100, self.volume_slider.value() + 10))
