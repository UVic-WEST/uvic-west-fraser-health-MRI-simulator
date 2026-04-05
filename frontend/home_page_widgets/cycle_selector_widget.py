from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
)
from PySide6.QtCore import QPoint, Signal
from PySide6.QtGui import QFont

from frontend.home_page_widgets.custom_cycle_button import CustomCycleButton

CYCLE_OPTIONS_DROPDOWN_COLOUR = "#FAF5F5"
DROPDOWN_BUTTON_GAP_PX = 20


class FixedComboBox(QComboBox):
    """
    This class builds a combo box (AKA DROPDOWN) with a fixed popup position

    Args:
        None
    """

    def showPopup(self):
        """
        This function shows the combo box popup below the widget
        """
        super().showPopup()
        popup = self.view().window()
        if popup:
            popup.move(self.mapToGlobal(QPoint(0, self.height())))


class CycleSelectorWidget(QWidget):
    """
    This class builds the cycle selector widget and custom cycle button

    Args:
        available_cycles: the cycle names shown in the dropdown
        parent: the parent widget for this container
    """

    cycle_selected = Signal(str)

    def __init__(self, cycles, parent=None):
        """
        Args:
            cycles: list of (cycle_id, cycle_name) tuples
            parent: parent widget
        """
        super().__init__(parent)
        self.cycles = cycles  # List of (cycle_id, cycle_name)
        self.id_to_name = {cid: name for cid, name in cycles}
        self.name_to_id = {name: cid for cid, name in cycles}

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(DROPDOWN_BUTTON_GAP_PX)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.cycle_selector = FixedComboBox()
        self.cycle_selector.setFixedWidth(353)
        self.cycle_selector.setFont(QFont("Ubuntu", 16))
        self.cycle_selector.setStyleSheet(f"""
            QComboBox {{
                background-color: {CYCLE_OPTIONS_DROPDOWN_COLOUR};
                color: black;
                border: 1px solid #0474BA;
                border-radius: 16px;
                padding: 4px 10px;
            }}
            QComboBox QAbstractItemView {{
                color: black;
                background: white;
                selection-color: black;
                selection-background-color: #d9d9d9;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 22px;
                color: black;
            }}
            QComboBox::down-arrow {{
                image: url(resources/frontend_common_assets/blacktriangle.png);
                width: 12px;
                height: 8px;
            }}
        """)
        # Add cycle names to dropdown
        for cid, name in cycles:
            self.cycle_selector.addItem(name, cid)
        self.cycle_selector.setCurrentIndex(0)
        self.main_layout.addWidget(self.cycle_selector)

        self.custom_cycle_button = CustomCycleButton(self)
        self.main_layout.addWidget(self.custom_cycle_button)

        self.setFixedWidth(353)
        self.setFixedHeight(
            self.cycle_selector.sizeHint().height() +
            self.custom_cycle_button.height() +
            DROPDOWN_BUTTON_GAP_PX
        )

        self.cycle_selector.currentTextChanged.connect(self._on_cycle_selected)
        self.custom_cycle_button.custom_cycle_requested.connect(self._on_custom_cycle_requested)

    def _on_cycle_selected(self, cycle_name):
        """
        Emits the selected cycle's ID (not just name)
        """
        cycle_id = self.name_to_id.get(cycle_name, None)
        if cycle_id:
            self.cycle_selected.emit(str(cycle_id))

    def get_selected_cycle_id(self):
        """
        Returns the currently selected cycle's ID
        """
        name = self.cycle_selector.currentText()
        return self.name_to_id.get(name, None)

    def _on_custom_cycle_requested(self):
        """
        This function emits when the custom cycle button is pressed

        Args:
            None
        """
        self.parent().open_custom_cycle_warning()
