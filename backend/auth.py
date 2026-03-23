"""Authentication module for the MRI simulator.

Handles PIN validation, login attempt tracking, automatic lockout after
three failed attempts (15-second timeout), and logout/reset logic.
"""

from PySide6.QtCore import QObject, Signal, QTimer

TIMEOUT_PERIOD = 15

class Auth(QObject):
    """
    required attributes and functions to set and reset attribute values depending on stage of login attempt by user
    attributes:
        correct_pin: PIN that will authenticate user (str)
        can_attempt_login: whether or not user can attempt to login (bool)
        is_authenticated: whether or not user successfully signed in after entering PIN (bool)
        remaining_attempts: number of PIN entry attempts left for user before 15 second timeout begins (int)
        timer: timer used for timed-out countdown logic
        time_rem_s: countdown value used for timed-out countdown logic
    """
    countdown = Signal(int)
    
    def __init__(self, correct_pin, parent):
        """
        verifies PIN length is correct (four digits) and sets initial attribute values for authentication process
        """
        super().__init__(parent)
        if len(correct_pin) != 4:
            raise ValueError("PIN must be four digits long")
        
        self.correct_pin = correct_pin
        self.can_attempt_login = True  # whether a user can attempt to login or not
        self.is_authenticated = False # whether PIN entered is the correct PIN
        self.remaining_attempts = 3  # sign in attempts remaining before 15 second timeout
        self.timer = None
        self.time_rem_s = 0

    def login(self, pin):
        """Attempt to authenticate with the given PIN.

        If the PIN matches, the user is authenticated. Otherwise the attempt
        counter decrements. After three consecutive failures a 15-second
        lockout is triggered via QTimer.

        Args:
            pin (str): The PIN entered by the user.

        Returns:
            bool: True if authentication succeeded, False otherwise.
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

            self.timer = QTimer(self)
            self.time_rem_s = TIMEOUT_PERIOD
            self.timer.timeout.connect(self._update_timer)
            self.timer.start(1000)
            return None
        return False
    
    def _update_timer(self):
        """updates the timeout countdown for the front end to use"""
        if self.time_rem_s > 0:
            self.time_rem_s -= 1
            self.countdown.emit(self.time_rem_s)
        else:
            self.timer.stop()
            self.unlock()

    
    def unlock(self):
        """Reset the lockout state so the user can attempt login again.

        Called automatically by QTimer after the 15-second lockout expires.
        """
        self.can_attempt_login = True
        self.remaining_attempts = 3
        return

    
    def logout(self):
        """Log the user out and reset authentication state.

        Resets is_authenticated to False and remaining_attempts to 3 so
        a fresh login flow can begin.
        """
        self.is_authenticated = False
        self.remaining_attempts = 3
        return
