"""Data model for a single sound track used in a cycle.

Stores the file path, duration, and volume level for one audio clip
that SoundPlayer can play during an MRI simulation.
"""

from dataclasses import dataclass


@dataclass
class SoundConfig:
    """Configuration for a single sound used in a cycle.

    Attributes:
        file_name (str): Path to the audio file (e.g. "mri_gradient.wav").
        duration (float): Playback duration in seconds.
        volume (int): Volume level from 0 to 100 (percentage). Defaults to 50.
    """

    file_name: str
    duration: float
    volume: int = 50

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
            f"duration={self.duration}, "
            f"volume={self.volume})"
        )