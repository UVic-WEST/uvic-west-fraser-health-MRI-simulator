from dataclasses import dataclass, field
from typing import List
from backend.sound_config import SoundConfig

@dataclass
class SoundGroupConfig:
    """
    Represents a group of sounds to be played together during a cycle.

    Attributes:
        group_id: unique ID for the group
        group_volume: volume for all sounds in the group (0–100)
        sounds: list of SoundConfig objects in the group
    """
    group_id: int
    group_volume: int = 50 # default group volume
    sounds: List[SoundConfig] = field(default_factory=list)

    def validate(self):
        if not (0 <= self.group_volume <= 100):
            raise ValueError(f"Group {self.group_id} volume must be 0–100")
        if not (1 <= len(self.sounds) <= 3):
            raise ValueError(f"Group {self.group_id} must have 1–3 sounds")