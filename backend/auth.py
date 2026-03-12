from dataclasses import dataclass

class Auth:
    """
    Handles the authentication of the MRI simulator.
    """
    def __post_init__(self, correct_pin):
        self._correct_pin = correct_pin
        
        can_attempt_login = True  # whether a user can attempt to login or not
        is_authenticated = False # whether PIN entered is the correct PIN
        remaining_attempts = 3  # sign in attempts remaining before 30 second timeout

        if len(correct_pin) != 4:
            raise ValueError(f"PIN must be four digits long")

    
    def login(self, pin):
        
        return

    
    def logout(self):
        return
