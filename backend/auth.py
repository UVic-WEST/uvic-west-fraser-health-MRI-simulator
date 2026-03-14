# The Auth class handles the the PIN validation logic, timeout logic after three failed login attempts, and logout logic.

from PyQt6.QtCore import QTimer

class Auth:
    """
    required attributes and functions to set and reset attribute values depending on stage of login attempt by user
    attributes:
        correct_pin: PIN that will authenticate user (str)
        can_attempt_login: whether or not user can attempt to login (bool)
        is_authenticated: whether or not user successfully signed in after entering PIN (bool)
        remaining_attempts: number of PIN entry attempts left for user before 30s timeout begins (int)
    """
    
    def __init__(self, correct_pin):
        """
        verifies PIN length is correct (four digits) and sets initial attribute values for authentication process
        """
        if len(correct_pin) != 4:
            raise ValueError("PIN must be four digits long")
        
        self.correct_pin = correct_pin
        self.can_attempt_login = True  # whether a user can attempt to login or not
        self.is_authenticated = False # whether PIN entered is the correct PIN
        self.remaining_attempts = 3  # sign in attempts remaining before 30 second timeout
    
    
    def login(self, pin):
        """
        checks that pin is the correct PIN and user is successfully signed in if so
        o/w, user has ability to reattempt PIN entry twice before login() initiates 30s timeout
        """
        # user already logged in
        if self.is_authenticated:
            return True

        # account still locked so cannot attempt login
        if not self.can_attempt_login:
            return False

        # correct PIN entered
        if pin == self.correct_pin:
            self.is_authenticated = True
            self.remaining_attempts = 3
            return True

        # incorrect PIN entered
        self.remaining_attempts -= 1
        if self.remaining_attempts == 0:
            self.can_attempt_login = False
            self.remaining_attempts = 3

            QTimer.singleShot(30000, self.unlock)

        return False

    
    def unlock(self):
        """unlocks authentication instance and resets relevant attributes so user can try signing in again"""
        self.can_attempt_login = True
        self.remaining_attempts = 3
        return

    
    def logout(self):
        """logs out of MRI simulator UI and resets relevant attributes so user can sign in again upon next use"""
        self.is_authenticated = False
        self.remaining_attempts = 3
        return
