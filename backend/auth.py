class Auth:
    """
    Handles the authentication of the MRI simulator.
    """
    # whether a user can attempt to login or not
    can_attempt_login = True
    is_authenticated = False
    remaining_attempts = 3

    def __init__(self, correct_pin):
        self._correct_pin = correct_pin

    def login(self, pin):
        return
    
    def logout(self):
        return