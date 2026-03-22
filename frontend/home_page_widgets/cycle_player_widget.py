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

    def __init__(self, parent=None):
        """
        This function builds the cycle player widget and its controls

        Args:
            parent: the parent widget for this container
        """
        #setup
        super().__init__(parent)
        self.parent = parent
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(PLAY_SQUARE_DROPDOWN_GAP_PX)
        self.main_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.cur_cycle = None
        
        #####################
        #####################
        #####################
        # Dummy cycle list for testing
        # Will need to be replaced!!!!
        self.available_cycles = ["Cycle 1", "Cycle 2", "Cycle 3"]

        #setting up widgets
        #setup for play square widget
        self.play_square_widget = PlaySquareWidget(self)
        self.main_layout.addWidget(self.play_square_widget)

        # setup for cycle selector dropdown and custom cycle button
        self.cycle_selector_widget = CycleSelectorWidget(self.available_cycles, self)
        self.main_layout.addWidget(self.cycle_selector_widget)

        # Keep this container tightly wrapped to its content to avoid extra vertical slack.
        self.setFixedWidth(353)
        self.setFixedHeight(
            self.play_square_widget.height() +
            self.cycle_selector_widget.height() +
            PLAY_SQUARE_DROPDOWN_GAP_PX  # Gap between play square and selector widget
        )

        #setting layout
        self.setLayout(self.main_layout)

        #connect dropdown selection to update cycle
        self.cycle_selector_widget.cycle_selected.connect(self.on_cycle_selected)
        self.cycle_selector_widget.custom_cycle_requested.connect(self.open_custom_cycle_warning)
        
        #initialize with first cycle selected
        self.on_cycle_selected(self.cycle_selector_widget.get_selected_cycle())
    
    #called when user selects a cycle from the dropdown
    def on_cycle_selected(self, cycle_name):
        """
        This function updates the selected cycle from the dropdown

        Args:
            cycle_name: the cycle name selected by the user
        """
        self.cur_cycle = cycle_name
        print("Current cycle updated to:", cycle_name)  
        self.parent.set_cur_cycle(cycle_name)
        self.play_square_widget.update_selected_cycle(cycle_name)

    def play_selected_cycle(self):
        """
        This function tells the parent widget to play the selected cycle
        """
        self.parent.play_selected_cycle()

    def open_custom_cycle_warning(self):
        """
        This function requests opening the custom cycle warning page
        """
        self.parent.show_custom_cycle_warning()

