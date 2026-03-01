# The LightConfig class stores the name, intensity, and frequency (if pulsing lights) for a single light setting

from dataclasses import dataclass
from typing import Optional

@dataclass
class LightConfig:
  """light settings for a single cycle"""
  sound_name: str
  sound_intensity: float   #0.0-1.0 (to adjust percentage of full brightness)
  sound_frequency: Optional[float] = None   #in Hz; used if lights are pulsing

  def __post_init__(self):
    """
    verify that the light data is formatted correctly and the values are reasonable
    """
    if 0.0 <= self.sound_intensity <= 1.0:
      raise ValueError("instensity is out of range: must be between 0.0 and 1.0 (inclusive)")
    if self.sound_frequency is not None and self.frequency <= 0:
      raise ValueError("frequency must be positive")

  def __repr__(self):
    """return string representation of light data"""
    
