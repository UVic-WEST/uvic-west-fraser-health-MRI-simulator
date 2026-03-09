# The CycleConfig class stores the total duration, global light settings, and list of SoundConfig objects for a single cycle

from dataclasses import dataclass, field
from typing import List

from backend.sound_config import SoundConfig
from backend.light_config import LightConfig


@dataclass
class CycleConfig:
    cycle_name: str
    cycle_duration: float  # in seconds
    light_settings: LightConfig
    sound_list: List[SoundConfig] = field(default_factory=list)

    def __post_init__(self):
        """Verify duration and that sound durations fit within cycle."""
        if self.cycle_duration <= 0:
            raise ValueError(
                f"total duration of {self.cycle_name} must be positive, got {self.cycle_duration}"
            )
        total_sound_time = sum(s.duration for s in self.sound_list)
        if total_sound_time > self.cycle_duration:
            raise ValueError(
                f"total sound duration ({total_sound_time}s) exceeds cycle duration "
                f"({self.cycle_duration}s) for {self.cycle_name}"
            )

    def get_sounds(self):
        """Return list of sound info strings for this cycle."""
        return [
            f"{s.file_name}: {s.duration}s" for s in self.sound_list
        ]

    def get_light_info(self):
        """Return light settings summary string."""
        return f"{self.light_settings.intensity}, {self.light_settings.frequency}"

    def __repr__(self):
        return (
            f"CycleConfig info for {self.cycle_name}:\n"
            f"\ttotal duration: {self.cycle_duration}\n"
            f"\tsounds used: {self.get_sounds()}\n"
            f"\tlight info: {self.get_light_info()}\n"
        )

"""
I will add functions to modify cycle:

def add_sound(self, sound_config)

def delete_sound(self, sound_name)

"""
        
