from PySide6.QtWidgets import(
     QWidget, QLabel, QPushButton
)

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import (QFont,
    QPixmap, QIcon)


class CustomCyclePage(QWidget):

    def __init__(self,parent,controller):
        """
        Initializes the CustomCyclePage widget with a parent and controller.
        Initialize minutes and seconds
        Sets up window size, background, buttons and duration screen.
        Further call all the helper functions and link the logic
        """
        super().__init__()
        self.parent = parent 
        self.controller = controller 

        self.minutes= 3
        self.seconds = 0

        self.setFixedSize(1024,600)
        self.set_background()
        self.set_logicbuttons()
        self.setup_DurationScreen()
        self.on_page_enter()

        #---------------Background
    def set_background(self):
        """
        This functions sets the background and layout of screen
        
        """
        self.bg_label = QLabel(self)
        self.bg_pixmap = QPixmap("../resources/timeduration_assets/timetemplate.png")

        self.bg_label.setPixmap(self.bg_pixmap.scaled(
            self.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        ))

        self.bg_label.setGeometry(0,0,self.width(),self.height())
        self.bg_label.lower()


        
    def set_logicbuttons(self):
        """
        This function handles logic for making all control buttons clickable ad setting their positions
        """
        # # next button
        self.next_btn = QPushButton("",self)
        self.next_btn.setGeometry(860,532.3,131,46.37) 
        self.next_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 30);
                border-radius: 25px;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 60);
                border-radius: 25px;
            }
        """)
        self.next_btn.clicked.connect(self.go_next)

        
        
        
        #default button
        self.default_btn = QPushButton("",self)
        self.default_btn.setGeometry(714,532.3,131,46.37)
        self.default_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 30);
                border-radius: 25px;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 60);
                border-radius: 25px;
            }
        """)
        self.default_btn.clicked.connect(self.set_default)

        #cancel button
        self.cancel_btn = QPushButton("",self)
        self.cancel_btn.setGeometry(20,22.26,131,46.37)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 30);
                border-radius: 25px;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 60);
                border-radius: 25px;
            }
        """)
        self.cancel_btn.clicked.connect(self.reset_customization)

        #help button
        self.help_btn = QPushButton("",self)
        self.help_btn.setGeometry(164,23.18,49,45.44)
        self.help_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 30);
                border-radius: 25px;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 60);
                border-radius: 25px;
            }
        """)
        self.help_btn.clicked.connect(self.go_help)



        ##positionin



    def setup_DurationScreen(self):
        """
        This function sets the main screen orientation of time screen
        It habdles time box, label, plus/minus buttons
        """

        self.durationText = QLabel("Enter Cycle Duration", self)
        self.durationText.setGeometry(328,199,415,76)
        self.durationText.setStyleSheet("Font-Family: Ubuntu; font-size: 44px; color: black")
        self.durationText.setAlignment(Qt.AlignCenter)


        self.time_label = QLabel("03:00",self)
        self.time_label.setGeometry(366,291,307,94)
        self.time_label.setStyleSheet("background-color: white; color: green; border: 2px solid #34C759; border-radius: 8px; font-size: 52px; font-family: 'Digital Numbers';" )
        self.time_label.setAlignment(Qt.AlignCenter)
        # self.time_label.setText(f"{self.minutes:02}:{self.seconds:02}") 
        #02 means two digits
        
        self.minus_btn = QPushButton("",self)
        self.minus_btn.setGeometry(280,314,48,48)
        self.minus_btn.setIcon(QIcon("../resources/timeduration_assets/minus_sign.png"))
        self.minus_btn.setIconSize(QSize(48,48))
        self.minus_btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    border-radius: 24px;
                                     
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 30);
                    border-radius: 24px;
                }
                QPushButton:pressed {
                    background: rgba(255, 255, 255, 60);
                    border-radius: 24px;
                }
        """)
        self.minus_btn.clicked.connect(self.dec_time)


        
        self.minus_ripple = QLabel("",self)
        self.minus_ripple.setGeometry(280,314,48,48)
        self.minus_ripple.setStyleSheet("background:  rgba(255,255,255,100); border-radius: 24px")
        self.minus_ripple.hide()

        self.plus_btn = QPushButton("",self)
        self.plus_btn.setGeometry(682,314,48,48)
        self.plus_btn.setIcon(QIcon("../resources/timeduration_assets/plus_sign.png"))
        self.plus_btn.setIconSize(QSize(48,48))
        self.plus_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 24px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 30);
                border-radius: 24px;
                
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 30);
                border-radius: 24px;
            }
        """)

        self.plus_btn.clicked.connect(self.inc_time)


        self.plus_ripple = QLabel("",self)
        self.plus_ripple.setGeometry(682,314,48,48)
        self.plus_ripple.setStyleSheet("background:  rgba(255,255,255,100); border-radius: 24px")
        self.plus_ripple.hide()




    #Place holders

    def go_next(self):
        """
        This function handles the logic to land on next page
        """
        print("next clicked")

    

    def set_default(self):
        """
        This function sets default cycle time to 3 minutes
        """
        self.minutes=3
        self.seconds=0
        self.cycledisplayScreen()
        self.check_boundaries()
        print("default clicked")

    def reset_customization(self):
        """
        This function cancels the customization and reset to default
        """
        print("reset")

    def go_help(self):
        """
        This function handle when help button is clicked user is taken to the help screen
        """
        print("help")

    def inc_time(self):
        """
        This function helps increase the time 
        The increment is done by 30 seconds
        """
        self.show_ripple("plus")
        self.seconds+=30
        if self.seconds==60:
            self.minutes+=1 
            self.seconds=0
        self.cycledisplayScreen()
        self.check_boundaries()
        print("add time")
        
    def dec_time(self):
        """
        This function helps decrease the time 
        The decrement is done by 30 seconds
        """
        self.show_ripple("minus")
        self.seconds-=30
        if self.seconds<0:
            self.minutes-=1
            self.seconds=30
        self.cycledisplayScreen()
        self.check_boundaries()
        print("minus time")

    def show_ripple(self,btn_type):
        """
        This function is used to create a ripple effect arouund plus and minus buttons when clicked

        btn_type: The argument keeps teh track of which button is clicked
        """
        if btn_type=="plus":
            self.plus_ripple.show()
            self.plus_ripple.raise_()
            QTimer.singleShot(200, self.plus_ripple.hide)
        else:
            self.minus_ripple.show()
            self.minus_ripple.raise_()
            QTimer.singleShot(200, self.minus_ripple.hide)
       


    def check_boundaries(self):
        """
        This function helps check the boundary
        This ensures the greying out of minus button when time is 1 MINUTE prohibiting access to reduce time 
        since that's a minimum limit 
        Similarly, greying out of plus button when time screen shows 15 MINUTES since that is s max time limit a user can set
        """
        if self.minutes==1 and self.seconds==00:
            self.minus_btn.setEnabled(False) #grey and unclickable
        elif self.minutes ==15 and self.seconds ==00:
            self.plus_btn.setEnabled(False)
        else:
            self.minus_btn.setEnabled(True)
            self.plus_btn.setEnabled(True)
            

    def cycledisplayScreen(self):
        """
        This function displays the time on time screen box
        """
        self.time_label.setText(f"{self.minutes:02}:{self.seconds:02}") 

    def on_page_enter(self):
        """
        This function takes the time from controller and converts the duration into 
        minutes and seconds format before displaying
        """
       
        total_dur = 180

        self.minutes = total_dur//60
        self.seconds = total_dur %60

        self.cycledisplayScreen()
        self.check_boundaries()

# """
# added only for testing my testing

# """
# if __name__ == "__main__":
#     import sys
#     from PySide6.QtWidgets import QApplication
    
#     app = QApplication(sys.argv)
#     window = CustomCyclePage(None,None)
#     window.show()
#     sys.exit(app.exec())

 
