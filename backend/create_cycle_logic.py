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
        return self.cycle_duration

    def set_duration(self, value):
        # check if value is between 1 second and 15 minutes (900 seconds)
        if 1 <= value <= 15 * 60:
            self.cycle_duration = value
            return True
        return False
    
    # --------------------------------------------------
    # LIGHT LEVEL
    # --------------------------------------------------
    def set_light_level(self, value):
        if 0 <= value <= 100:
            self.light_level = value
            return True
        return False
    
    def get_light_level(self):
        return self.light_level
    
    def display_light_level(self, light_level):
        # asks the backend to turn on the lights so need to communicate to embedded to turn light on at that level
        # placeholder (later connect to hardware)
        # look at code at for how it being done manually???
        return light_level

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------
    def validate_cycle(self) -> bool:
        return True  # Placeholder for actual validation logic (e.g., check if duration is set, groups are configured, etc.)
    
    # --------------------------------------------------
    # FINALIZE + SAVE CYCLE
    # --------------------------------------------------
    def save(self):
        """ Build and save the cycle """
        if not self.validate_cycle():
            return None

        # create cycle object
        new_id = CycleRepository.get_next_id()
        new_name = self._generate_cycle_name(new_id)

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
    
    # helper function to generate a cycle name based on the cycle ID
    def _generate_cycle_name(self, cycle_id: int) -> str:
        return f"Cycle {cycle_id}"
    
    