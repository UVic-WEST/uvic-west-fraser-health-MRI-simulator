from PySide6.QtCore import (
    QObject
)
from .led_strip import LEDStrip
class LightController(QObject):
    '''
    This is the controller for turning on lights and changing their brighness throughtout the MRI
    cycle running experience. 

    I have this as a Qobject to prevent resource competition. If you are using this controller
    have it passed in to your code from FE/app_router.py to wherever your code is in the repo.
    It's stored as a variable self.light_controller.

    eg: app_router.py -> cycle_running_logic.py -> your_file.py
    '''
    BASE_BRIGHTNESS = .1

    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.locked = False
        self.strip = LEDStrip()
        self.system_idle()

    def system_idle(self):
        '''
        Function to prepare turning on the lights when booting up the system or want lights to be at 
        baseline after a cycle
        '''
        self.locked = False
        #send signal to ELEC code to turn on light
        #send signal to ELEC code to turn brightness to 0 or to baseline light level
        self.strip.set_white(self.BASE_BRIGHTNESS)
        return True

    def change_lights(self, brightness:float):
        '''
        Change the light brightness/intensity. 
        brightness: float, from [0.0 - 1] in 0.1 increments.
        CALL THIS FUNCTION'S .system_idle() FUNC WHEN FINISHED WITH ROUTINE.
        '''
        assert (brightness <= 1 and brightness >= 0), "Brightness not within proper range."
        #Changed this b/c I want to be able to use this function in a loop and not have to worry about the resource being locked.
        assert (self.locked is False), "This resource is in use." 
        self.locked = True

        #to ask: will this require a fork?
        #send signal to elec to change light level of lights
        self.strip.set_white(brightness)

        self.locked = False

        return True # it's connected
    
    def system_off(self):
        '''
        possible function to connect with e-stop or on/off switch
        '''
        #call to elec to shut off lights?
        self.strip.power_off()

