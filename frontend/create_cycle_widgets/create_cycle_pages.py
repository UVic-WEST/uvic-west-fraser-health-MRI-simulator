from PySide6.QtWidgets import (
    QWidget,
    QStackedLayout,
)

from frontend.create_cycle_widgets.cc_duration_widgets.cc_duration import CCDurationPage
from frontend.create_cycle_widgets.cc_groups_widgets.cc_groups import CCGroupsPage
from frontend.create_cycle_widgets.cc_brightness_widgets.cc_brightness import CCBrightnessPage
from frontend.create_cycle_widgets.cc_sound_group_mapping_widgets.cc_sound_group_mapping import CCSoundGroupMappingPage
from frontend.create_cycle_widgets.cc_summary_widgets.cc_summary import CCSummary

class CreateCycleRouter(QWidget):
    def __init__(self, parent=None):
        """
        CreateCycleRouter (QWidget) handles the flow for creating a new cycle.
        It instantiates the following classes upon access (called by the app router)
            1. cc_controller (ADD NAME OF PAGE HERE)
            2. cc_duration_page (CCDurationPage)
            3. cc_groups_page (CCGroupsPage)
            4. cc_brightness_page (CCBrightnessPage)
            5. cc_sound_group_mapping_page (CCSoundGroupMappingPage)
            6. cc_summary_page (CCSummary)
        [2-6] is also the flow of the create cycle process, which can be traversed at user will.

        Args:
            parent (QWidget): parent of this widget instance, in this case AppRouter
        """

        super().__init__(parent)
        
        #controller refreshes
        self.cc_controller = None 

        #Create page attributes, these refresh for new create cycle flow
        self.cc_duration_page = None
        self.cc_groups_page = None
        self.cc_brightness_page = None
        self.cc_sound_group_mapping_page = None
        self.cc_summary_page = None


    def create_new_cycle(self):
        """
        Refreshes the controller and pages when starting a new create cycle process. Called by the parent.
        """
        from backend.create_cycle_logic import CreateCycleLogic
        from backend.cycle_controller import CycleController
        from backend.cycle_config import CycleConfig

        parent = self.parent()
        cycle_controller = getattr(parent, 'cycle_controller', None)
        self.cc_controller = CreateCycleLogic(cycle_id=0, cycle_name="New Custom Cycle", cycle_controller=cycle_controller)

        self.cc_duration_page = CCDurationPage(self.cc_controller, self)
        self.cc_groups_page = CCGroupsPage(self.cc_controller, self)
        self.cc_brightness_page = CCBrightnessPage(self.cc_controller, self)
        self.cc_sound_group_mapping_page = None  # Delay instantiation
        self.cc_summary_page = CCSummary(self.cc_controller, self)

        self.reset_layout()

    def reset_layout(self):
        """
        Sets the layout of the router when a new create cycle process is started
        """
        self.main_layout = QStackedLayout()

        self.main_layout.addWidget(self.cc_duration_page)
        self.main_layout.addWidget(self.cc_groups_page)
        self.main_layout.addWidget(self.cc_brightness_page)
        # Insert a placeholder for the sound group mapping page
        self.main_layout.addWidget(QWidget())  # Placeholder
        self.main_layout.addWidget(self.cc_summary_page)

        self.setLayout(self.main_layout)

    def _ensure_sound_group_mapping_page(self):
        """
        Instantiates and inserts the sound group mapping page if not already done.
        """
        if self.cc_sound_group_mapping_page is None:
            self.cc_sound_group_mapping_page = CCSoundGroupMappingPage(self.cc_controller, self)
            # Replace the placeholder with the real widget
            self.main_layout.insertWidget(3, self.cc_sound_group_mapping_page)
            # Remove the old placeholder (now at index 4)
            placeholder = self.main_layout.widget(4)
            self.main_layout.removeWidget(placeholder)
            placeholder.deleteLater()

    def next_pressed(self):
        """
        Reroutes to the next page of the create cycle process. Called by child widgets.
        """
        next_page_index = self.main_layout.currentIndex() + 1
        # If navigating to the sound group mapping page, ensure it's created and refreshed
        if next_page_index == 3:
            self._ensure_sound_group_mapping_page()
            if self.cc_sound_group_mapping_page is not None:
                self.cc_sound_group_mapping_page.refresh_groups_from_backend()
        self.main_layout.setCurrentIndex(next_page_index)

    def back_pressed(self):
        """
        Reroutes to the previous page of the create cycle process. Called by child widgets.
        """
        back_page_index = (self.main_layout.currentIndex()) - 1 
        self.main_layout.setCurrentIndex(back_page_index)
