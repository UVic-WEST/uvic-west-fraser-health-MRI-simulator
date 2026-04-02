"""Data model for a single sound track used in a cycle.

Stores the file path, duration, and volume level for one audio clip
that SoundPlayer can play during an MRI simulation.
"""

from dataclasses import dataclass


@dataclass
class SoundConfig: 
    """Stores configuration for a single sound used in a cycle."""

    file_name: str # file path of sound file 
    sound_id: int # unique identifier for a sound file
    duration: float # seconds
    volume: 50 # value from 0 - 100 (preset percentage of full volume, initally 50%)
    
    def __post_init__(self):
        """Validate sound config values.

        Raises:
            ValueError: If file_name is empty, duration is negative, or
                volume is outside the 0–100 range.
        """
        
        if not self.file_name:
            raise ValueError("file_name must be a non-empty string")
        
        if self.duration < 0:
            raise ValueError("duration must be between 1 and 100")
        
        if not (0 <= self.volume <= 100):
            raise ValueError("volume must be between 0 and 100")
    
    def __repr__(self) -> str:
        """String representation of sound config object"""
        
        return (
            f"SoundConfig({self.file_name}, "
            f"sound_id={self.sound_id}, "
            f"duration={self.duration}, "
            f"volume={self.volume})"
        )