from PySide6.QtCore import (
    QTimer,
    Signal,
    QObject
)

class CycleRunningPageLogic(QObject):

    time_signal_in_s = Signal(int)

    '''
    Right now this class stubs basic functionality between the cycle running page UI in frontend and backend.
    '''
    def __init__(self, parent=None):

        super().__init__(parent)
        self.parent = parent
        self.cur_cycle = None
        self.rem_time_ms = None
        self.timer = None

    def start_cycle(self, cycle_id:int, rem_time_s:int): 
        '''
        right now frontend will send the cycle ID until the cycle class is made
        later the cycle class will include duration time which should be extracted by backend automatically
        '''
        self.rem_time_ms = rem_time_s * 1000
        #logic to start the cycle goes here, but the fronend needs an instance of
        # QTimer to display our countdown, for actual implementation change this QTimer back as the timer
        # with the proper set duration.
        if self.timer:
            self.timer.stop()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.time_signal_in_s.emit(rem_time_s)
    
    def pause_cycle(self):
        if self.timer:
            self.timer.stop()
            self.time_signal_in_s.emit(-1)
        return True
    
    def resume_cycle(self):
        if self.rem_time_ms and self.rem_time_ms > 0:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_timer)
            self.timer.start(1000)
    
    def stop_cycle(self):
        if self.timer:
            self.timer.stop()
            self.timer = None
        self.rem_time_ms = None
        self.time_signal_in_s.emit(-1)
    
    def update_timer(self):
        '''
        this function is for basic timer functionality. remove when actual timer gets connected
        what it does: every second emit that a second has passed for the timer in the frontend
        and send the remaining time in seconds
        '''
        if self.rem_time_ms > 0:
            self.rem_time_ms -= 1000
            self.time_signal_in_s.emit(self.rem_time_ms // 1000)
        else:
            if self.timer:
                self.timer.stop()
            self.time_signal_in_s.emit(0) #completed timer