# The LightConfig class stores the name, intensity, and frequency (if pulsing lights) for a single light setting

from dataclasses import dataclass
from typing import Optional

@dataclass
class LightConfig:
  """light settings for a single cycle"""
  light_name: str
  intensity: float   #0.0-1.0 (to adjust percentage of full brightness)
  frequency: Optional[float] = None   #in Hz; used if lights are pulsing

  def __post_init__(self):
    """Verify that the light data is formatted correctly and the values are reasonable."""
    if not (0.0 <= self.intensity <= 1.0):
      raise ValueError("intensity must be between 0.0 and 1.0 (inclusive)")
    if self.frequency is not None and self.frequency <= 0:
      raise ValueError("frequency must be positive")

  def __repr__(self):
    """Return string representation of light data."""
    return (
      f"LightConfig info for {self.light_name}:\n"
      f"\tlight intensity: {self.intensity}\n"
      f"\tlight frequency: {self.frequency}\n"
    )
