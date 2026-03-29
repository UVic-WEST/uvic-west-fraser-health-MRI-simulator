from typing import List
from backend.cycle_config import CycleConfig
from backend.cycle_action import CycleAction, ActionType

class CycleFactory:
    """ provides predefined MRI simulation cycle configurations """
    
    def __init__(self):
        self._predefined_cycles: List[CycleConfig] = []
        self._load_cycles()

    def _load_cycles(self):
        """ load all predefined cycle configurations into the factory """
        self._predefined_cycles.append(self._create_cycle1())
        self._predefined_cycles.append(self._create_cycle2())
        # more cycles can be added here

        # create a mapping of cycle_id to CycleConfig for easy retrieval
        self._cycles = {cycle.cycle_id: cycle for cycle in self._predefined_cycles}
    
    def get_cycle_by_id(self, cycle_id: str) -> CycleConfig:
        """
        Retrieve a cycle configuration by its unique ID
        
        Raises:
            ValueError: If no cycle exists with the specified ID
        """
        
        try:
            return self._cycles[cycle_id] 
        except KeyError:
            raise ValueError(f"No cycle with id {cycle_id}")
    
    def get_cycle_by_index(self, index: int) -> CycleConfig:
        """
        Retrieve a cycle configuration by its index in the predefined list

        Raises:
            ValueError: If the index is out of range
        """
        
        try:
            return self._predefined_cycles[index]
        except IndexError:
            raise ValueError(f"No cycle at index {index}")

    def list_cycles(self):
        """ returns a list of all available predefined cycles """
        return list(self._cycles.values())

    # ---------------------------------------------------------------------------
    # private methods to create predefined cycles
    # these can be modified or expanded to create different cycles as needed
    # ---------------------------------------------------------------------------

    def _create_cycle1(self):
        return CycleConfig(
            cycle_id=1,
            cycle_name="Standard MRI",
            cycle_duration_ms=10000,
            light_configuration=50,
            actions=[
                CycleAction(1000, ActionType.SOUND_START, {"file_name": "Default", "duration": 2000, "volume": 50}),
                CycleAction(4500, ActionType.SOUND_STOP, {})
            ]
        )

    def _create_cycle2(self):
        return CycleConfig(
            cycle_id=2,
            cycle_name="Fast MRI",
            cycle_duration_ms=5000,
            light_configuration=50,
            actions=[
                CycleAction(500, ActionType.SOUND_START, {"volume": 50}),
                CycleAction(2000, ActionType.SOUND_STOP, {}),
            ]
        )
    
    # create more cycles as needed