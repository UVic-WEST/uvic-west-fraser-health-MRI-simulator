from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLayout,
)
from frontend.home_page_widgets.play_square_widget import PlaySquareWidget
from frontend.home_page_widgets.cycle_selector_widget import CycleSelectorWidget

PLAY_SQUARE_DROPDOWN_GAP_PX = 20

class CyclePlayerWidget(QWidget):
    """
    This class builds the cycle player widget and its controls

    Args:
        parent: the parent widget for this container
    """

    def __init__(self, cycles, parent=None):
        """
        Args:
            cycles: list of (cycle_id, cycle_name) tuples
            parent: parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(PLAY_SQUARE_DROPDOWN_GAP_PX)
        self.main_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.cur_cycle_id = None

        # setup for play square widget
        self.play_square_widget = PlaySquareWidget(self)
        self.main_layout.addWidget(self.play_square_widget)

        # setup for cycle selector dropdown and custom cycle button
        self.cycle_selector_widget = CycleSelectorWidget(cycles, self)
        self.main_layout.addWidget(self.cycle_selector_widget)

        # Keep this container tightly wrapped to its content to avoid extra vertical slack.
        self.setFixedWidth(353)
        self.setFixedHeight(
            self.play_square_widget.height() +
            self.cycle_selector_widget.height() +
            PLAY_SQUARE_DROPDOWN_GAP_PX
        )

        self.setLayout(self.main_layout)

        # initialize with first cycle selected
        self.on_cycle_selected(self.cycle_selector_widget.get_selected_cycle_id())

    def on_cycle_selected(self, cycle_id):
        """
        This function updates the selected cycle from the dropdown
        Args:
            cycle_id: the cycle id selected by the user
        """
        self.cur_cycle_id = cycle_id
        print("Current cycle updated to ID:", cycle_id)
        self.parent.set_cur_cycle(cycle_id)
        self.play_square_widget.update_selected_cycle(cycle_id)

    def play_selected_cycle(self):
        self.parent.play_selected_cycle()

    def open_custom_cycle_warning(self):
        self.parent.show_custom_cycle_warning()

