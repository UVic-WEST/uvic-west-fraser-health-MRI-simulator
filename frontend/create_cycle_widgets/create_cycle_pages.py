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
        #CHANGE WHEN L2 HAS IMPLEMENTATION
        self.cc_controller = None 

        self.cc_duration_page = CCDurationPage(self.cc_controller,self)
        self.cc_groups_page = CCGroupsPage(self.cc_controller, self)
        self.cc_brightness_page = CCBrightnessPage(self.cc_controller, self)
        self.cc_sound_group_mapping_page = CCSoundGroupMappingPage(self.cc_controller, self)
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
        self.main_layout.addWidget(self.cc_sound_group_mapping_page)
        self.main_layout.addWidget(self.cc_summary_page)

        self.setLayout(self.main_layout)

    def next_pressed(self):
        """
        Reroutes to the next page of the create cycle process. Called by child widgets.
        """
        next_page_index = (self.main_layout.currentIndex()) + 1 
        self.main_layout.setCurrentIndex(next_page_index)

    def back_pressed(self):
        """
        Reroutes to the previous page of the create cycle process. Called by child widgets.
        """
        back_page_index = (self.main_layout.currentIndex()) - 1 
        self.main_layout.setCurrentIndex(back_page_index)
