from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
    QLayout,
)
from PySide6.QtCore import QPoint
from PySide6.QtGui import QFont
from frontend.home_page_widgets.play_square_widget import PlaySquareWidget
from frontend.home_page_widgets.custom_cycle_button import CustomCycleButton

CYCLE_OPTIONS_DROPDOWN_COLOUR = "#FAF5F5"
PLAY_SQUARE_DROPDOWN_GAP_PX = 20


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

        #setup for cycle selector dropdown
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
        self.cycle_selector.addItems(self.available_cycles) ### may need to update if we change available_cycles
        self.cycle_selector.setCurrentIndex(0)  # Default to first cycle
        self.main_layout.addWidget(self.cycle_selector)

        #setup for create custom cycle button
        self.custom_cycle_button = CustomCycleButton(self)
        self.main_layout.addWidget(self.custom_cycle_button)

        # Keep this container tightly wrapped to its content to avoid extra vertical slack.
        self.setFixedWidth(353)
        self.setFixedHeight(
            self.play_square_widget.height() +
            self.cycle_selector.sizeHint().height() +
            self.custom_cycle_button.height() +
            (PLAY_SQUARE_DROPDOWN_GAP_PX * 2)  # Gap between play square and dropdown, and dropdown and button
        )

        #setting layout
        self.setLayout(self.main_layout)

        #connect dropdown selection to update cycle
        self.cycle_selector.currentTextChanged.connect(self.on_cycle_selected)
        
        #initialize with first cycle selected
        self.on_cycle_selected(self.available_cycles[0])
    
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

