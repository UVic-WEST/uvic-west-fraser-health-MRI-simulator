from backend.cycle_config import CycleConfig
from backend.cycle_repository import CycleRepository


class CreateCycleLogic:
    def __init__(self, cycle_duration: int = 300, light_level: int = 50):
        self.cycle_duration = cycle_duration # seconds
        self.light_level = light_level
    
    # --------------------------------------------------
    # DURATION
    # --------------------------------------------------
    def get_duration(self):
        """Return current duration in seconds."""
        return self.cycle_duration

    def set_duration(self, value):
        """
        Set cycle duration.

        Constraints:
        - 1 to 15 minutes (60-900 seconds)
        """
        if 1 <= value <= 15 * 60:
            self.cycle_duration = value
            return True
        return False
    
    # --------------------------------------------------
    # LIGHT LEVEL
    # --------------------------------------------------
    def get_light_level(self):
        """Return current light level."""
        return self.light_level
    
    def set_light_level(self, value: int):
        """
        Set light level.

        Constraints:
        - 0-100
        - increments of 10
        """
        if not isinstance(value, int):
            raise ValueError("Light level must be int")  # internal error

        if 0 <= value <= 100 and value % 10 == 0:
            self.light_level = value
            return True

        return False  # user input validation
    
    def display_light_level(self, light_level):
        # validate type
        if not isinstance(light_level, int):
            raise ValueError("Light level must be an integer")

        # validate range + increments
        if not (0 <= light_level <= 100 and light_level % 10 == 0):
            return False

        # convert 0-100 to 0.0-1.0
        brightness = light_level / 100.0

        # send to hardware (L3 via controller)
        if self.cycle_controller:
            self.cycle_controller.light_controller.change_lights(brightness)

        return True

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------
    def validate_cycle(self) -> bool:
        """Ensure all required fields are valid before saving."""
        return (
            isinstance(self.cycle_duration, int)
            and 60 <= self.cycle_duration <= 900
            and isinstance(self.light_level, int)
            and 0 <= self.light_level <= 100
            and self.light_level % 10 == 0
        )
    
    # --------------------------------------------------
    # FINALIZE + SAVE CYCLE
    # --------------------------------------------------
    def save(self):
        """
        Build and persist the cycle.

        Returns:
            CycleConfig if successful, None otherwise
        """
        if not self.validate_cycle():
            return None

        # generate ID + name
        new_id = CycleRepository.get_next_id()
        new_name = self._generate_cycle_name(new_id)

        # build cycle config
        cycle = CycleConfig(
            cycle_id=new_id,
            cycle_name=new_name,
            cycle_duration_ms=self.cycle_duration * 1000,
            actions=[]  # sound stuff add later
        )
        
        # save it
        cycles = CycleRepository.load_all()
        cycles.append(cycle)
        CycleRepository.save_all(cycles)

        return cycle
    
    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------
    def _generate_cycle_name(self, cycle_id: int) -> str:
        """Generate default cycle name based on ID."""
        return f"Cycle {cycle_id}"
    
    