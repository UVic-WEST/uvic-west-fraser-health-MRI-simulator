"""Authentication module for the MRI simulator.

Handles PIN validation, login attempt tracking, automatic lockout after
three failed attempts (15-second timeout), and logout/reset logic.
"""

from PySide6.QtCore import QObject, Signal, QTimer


class Auth:
    """Manages user authentication state for the MRI simulator.

    Attributes:
        correct_pin (str): The four-digit PIN required to authenticate.
        can_attempt_login (bool): Whether the user is allowed to attempt login
            (False during lockout period).
        is_authenticated (bool): Whether the user is currently signed in.
        remaining_attempts (int): Number of PIN entry attempts remaining before
            the 15-second lockout is triggered.
    """

    def __init__(self, correct_pin):
        """Initialise Auth with the correct PIN.

        Args:
            correct_pin (str): A four-digit string used as the valid PIN.

        Raises:
            ValueError: If correct_pin is not exactly four characters.
        """
        if len(correct_pin) != 4:
            raise ValueError("PIN must be four digits long")
        
        self.correct_pin = correct_pin
        self.can_attempt_login = True  # whether a user can attempt to login or not
        self.is_authenticated = False # whether PIN entered is the correct PIN
        self.remaining_attempts = 3  # sign in attempts remaining before 15 second timeout
    
    
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

            QTimer.singleShot(15000, self.unlock)

        return False

    
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
