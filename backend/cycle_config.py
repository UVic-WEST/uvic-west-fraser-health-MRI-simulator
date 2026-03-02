# The CycleConfig class stores the total duration, global light settings, and list of SoundConfig objects for a single cycle

from dataclasses import dataclass, field
from sound_config import SoundConfig
from light_config import LightConfig

@dataclass
class CycleConfig:
    cycle_name: str
    cycle_duration: float   #in seconds
    light_settings: LightConfig
    sound_list: List[SoundConfig] = field(default_factory=list)

def __post_init__(self):
    """
    verifies that duration, light, and sound data are formatted correctly and values abide by cycle duration constraints

    (currently I am not sure of the SoundConfig components/attributes so I am simply assuming what will be present and will modify later)
    """
    for sound in self.sound_list:
        end_time = sound.start_time + sound.total_duration
        if end_time > self.cycle_duration:
            raise ValueError(f"end time of {sound.sound_name} ({end_time}s) surpasses total duration of {self.cycle_name} ({self.cycle_duration}s)")

    if self.cycle_duration <= 0:
        raise ValueError(f"total duration of {self.cycle_name} must be positive")

def get_sounds(self):
    cycle_sounds = []
    for sound in self.sound_list:
        end_time = sound.start_time + sound.total_duration
        if end_time <= self.cycle_duration:
            sound_info = f"{sound.sound_name}: {sound.total_duration}s"
            cycle_sounds.append(sound_info)
    return cycle_sounds

def get_light_info(self):
    return ("{self.light_settings.intensity}, {self.light_settings.frequency}")

def __repr__(self):
    """returns string representation of given cycle"""
    return (f"CycleConfig info for {self.cycle_name}: \n"
            f"\ttotal duration: {self.cycle_duration}\n"
            f"\tsounds used: {self.get_sounds()}\n"
            f"\tlight info: {self.get_light_info()\n")

"""
I will add functions to modify cycle:

def add_sound(self, sound_config)

def delete_sound(self, sound_name)

"""
        
