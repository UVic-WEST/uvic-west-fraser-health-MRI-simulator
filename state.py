class AppStateMachine:
    _state = "IDLE"

    def __init__(self):
        self._state = "IDLE"
    
    def set_state(self, new_state):
        # TODO: validate state
        self._state = new_state
    
    def get_state(self):
        return self._state