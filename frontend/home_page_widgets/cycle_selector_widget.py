from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
    QStyledItemDelegate,
    QStyle,
)
from PySide6.QtCore import QPoint, Signal, Qt, QRect, QEvent
from PySide6.QtGui import QFont, QMouseEvent, QPainter

from frontend.home_page_widgets.custom_cycle_button import CustomCycleButton

CYCLE_OPTIONS_DROPDOWN_COLOUR = "#FAF5F5"
DROPDOWN_BUTTON_GAP_PX = 20
DELETE_ICON_ROLE = Qt.UserRole + 1


class CycleItemDelegate(QStyledItemDelegate):
    """Paint dropdown rows with an optional right-aligned trash icon."""

    def paint(self, painter: QPainter, option, index):
        super().paint(painter, option, index)
        if not bool(index.data(DELETE_ICON_ROLE)):
            return

        icon = option.widget.style().standardIcon(QStyle.SP_TrashIcon)
        icon_rect = self._icon_rect(option.rect)
        icon.paint(painter, icon_rect)

    @staticmethod
    def _icon_rect(item_rect: QRect) -> QRect:
        icon_size = 16
        right_padding = 12
        x = item_rect.right() - right_padding - icon_size
        y = item_rect.top() + (item_rect.height() - icon_size) // 2
        return QRect(x, y, icon_size, icon_size)


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
    cycle_delete_requested = Signal(int)

    def __init__(self, cycles, parent=None):
        """
        Args:
            cycles: list of (cycle_id, cycle_name) tuples
            parent: parent widget
        """
        super().__init__(parent)
        self.parent = parent
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
        self.cycle_selector.setItemDelegate(CycleItemDelegate(self.cycle_selector))
        self.cycle_selector.view().viewport().installEventFilter(self)
        self.set_cycles(cycles)
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
        self.cycle_delete_requested.connect(self._on_delete_requested)

    def _should_show_delete_icon(self, cycle_id: int) -> bool:
        """
        Return whether a cycle row should show the delete icon.

        Only custom cycles with ID 4 and above are deletable, and only when
        more than three cycles exist.
        """
        return len(self.cycles) > 3 and cycle_id >= 4

    def set_cycles(self, cycles):
        """
        Replace the dropdown contents and rebuild row metadata/icons.

        Args:
            cycles: list of (cycle_id, cycle_name) tuples
        """
        self.cycles = cycles
        self.id_to_name = {cid: name for cid, name in cycles}
        self.name_to_id = {name: cid for cid, name in cycles}

        self.cycle_selector.blockSignals(True)
        self.cycle_selector.clear()
        for cid, name in cycles:
            self.cycle_selector.addItem(name, cid)
            row = self.cycle_selector.count() - 1
            self.cycle_selector.setItemData(row, self._should_show_delete_icon(cid), DELETE_ICON_ROLE)
        if self.cycle_selector.count() > 0:
            self.cycle_selector.setCurrentIndex(0)
        self.cycle_selector.blockSignals(False)

    def eventFilter(self, watched, event):
        """
        Intercept dropdown clicks so trash icons can trigger delete requests.
        """
        if watched is self.cycle_selector.view().viewport() and event.type() == QEvent.MouseButtonPress:
            mouse_event = event
            if isinstance(mouse_event, QMouseEvent):
                index = self.cycle_selector.view().indexAt(mouse_event.position().toPoint())
                if index.isValid() and bool(index.data(DELETE_ICON_ROLE)):
                    icon_rect = CycleItemDelegate._icon_rect(self.cycle_selector.view().visualRect(index))
                    if icon_rect.contains(mouse_event.position().toPoint()):
                        cycle_id = int(index.data(Qt.UserRole))
                        self.cycle_delete_requested.emit(cycle_id)
                        self.cycle_selector.hidePopup()
                        return True
        return super().eventFilter(watched, event)

    def _on_delete_requested(self, cycle_id: int):
        """
        Forward a delete request to the parent container.

        Args:
            cycle_id: the cycle ID chosen for deletion
        """
        if self.parent and hasattr(self.parent, "request_cycle_delete"):
            self.parent.request_cycle_delete(cycle_id)

    def _on_cycle_selected(self, cycle_name):
        """
        Emits the selected cycle's ID (not just name)
        """
        cycle_id = self.name_to_id.get(cycle_name, None)
        if cycle_id:
            self.parent.on_cycle_selected(cycle_id)

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
        self.parent.open_custom_cycle_warning()
