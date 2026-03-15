from PySide6.QtWidgets import(
    QWidget,
    QGridLayout,
    QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from frontend.home_page_widgets.cycle_player_widget import CyclePlayerWidget
from frontend.home_page_widgets.sign_out_button import SignOutButton

class HomePage(QWidget):
    def __init__(self, controller, parent=None):

        #Homepage setup
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.main_layout = QGridLayout()
        self.main_layout.setContentsMargins(40, 110, 40, 40)
        self.cur_cycle = None

        #setting up and organizing widgets
        self.play_widget = CyclePlayerWidget(self)
        self.main_layout.addWidget(self.play_widget, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(self.main_layout)

        #setting up sign out button (positioned absolutely in top left)
        self.sign_out_button = SignOutButton(self)
        self.sign_out_button.move(20, 20)
        self.sign_out_button.raise_()  # Bring to front

        #setting up logo (positioned absolutely so it doesn't affect layout)
        logo_path = 'resources/frontend_common_assets/west_logo.png'
        logo_pixmap = QPixmap(logo_path)
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setScaledContents(False)
        self.logo_label.adjustSize()
        self.logo_label.raise_()  # Bring to front
    
    def resizeEvent(self, event):
        """Reposition logo when widget is resized"""
        super().resizeEvent(event)
        # Position logo in top-right corner with padding
        self.logo_label.move(self.width() - self.logo_label.width() - 40, 20)

    def set_cur_cycle(self, cycle_name):
        self.cur_cycle = cycle_name

    # Backward-compatible alias while other callers are being updated.
    def set_selected_cycle(self, cycle_name):
        self.set_cur_cycle(cycle_name)
        
    def play_selected_cycle(self):
        print("Current cycle confirmed to play:", self.cur_cycle)
        self.parent.play_cycle(self.cur_cycle)
    
    def signout(self):
        '''
        when sign out button is pressed, user is signed out and sent to sign in page.
        '''
        self.parent.show_signin()