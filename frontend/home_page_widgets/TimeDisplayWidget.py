from PySide6.QtWidgets import ( # type: ignore
    QWidget,
    QLabel,
    QVBoxLayout
)
from PySide6.QtCore import Qt, QSize # type: ignore
from PySide6.QtGui import QPixmap # type: ignore
class TimeDisplayWidget(QWidget):
    """
    GUI implementation
    """
    def __init__(self,parent=None):
        super().__init__(parent)
        
        self.setFixedSize(395,141)

        self.setAttribute(Qt.WA_StyledBackground, True)  

        
        self.setStyleSheet("""
                           
            QWidget{
                        background-color: #FDFDFD;
                        border-radius: 15px;
                        border: 3px solid #34C759
            }
            QLabel{
                    background: transparent;
                    border: none;}
                        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)


        time_screen_asset = "resources/cycle_running_page_assets/timer_box.png"   
        time_pix = QPixmap(time_screen_asset)
        

        # self.time_text = QLabel("05:00")
        # self.time_text.setAlignment(Qt.AlignCenter)
        # self.time_text.setStyleSheet("font-size: 48px;font-family: 'Digital Numbers';color: #34C759;background:transparent;border:none;")
        # layout.addWidget(self.time_text)

        self.text = QLabel()
        self.text.setPixmap(time_pix)
        self.text.setAlignment(Qt.AlignCenter) 
        self.text.setStyleSheet("background: transparent; border: none;")  # add this
        layout.addWidget(self.text)
        
                # main_layout = QGridLayout()

        # self.time_label = QLabel("5:00")
        # self.time_label.setAlignment(Qt.AlignCenter)
        # self.time_label.setStyleSheet("""
        #         font-size: 48px;
        #         font-family: "Ubuntu";
        #         color: #34C759;
        #     """)
        
        # self.time_text = QLabel("MINUTES REMAINING")
        # self.time_text.setAlignment(Qt.AlignCenter)
        # self.time_text.setStyleSheet("""
        #          font-size: 48px;
        #         font-family: "Ubuntu";
        #         color: #34C759;
        #             """)
        
        # main_layout.addWidget(self.time_label,0,0)
        # main_layout.addWidget(self.time_text,1,0)

        # self.setLayout(main_layout)