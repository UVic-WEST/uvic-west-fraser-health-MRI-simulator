from PySide6.QtCore import QObject, Signal
from dataclasses import dataclass, field
from typing import List
import json
from backend/cycle_config.py CycleConfig

@dataclass
class CreateCycleLogic(QObject):
  """
  Bridges between L1 (CreateCyclePages) and L2 to create, display, and save a custom cycle to json file.

  ATTRIBUTES:
    cycle_id (int): unique identifier for custom MRI simulation cycle
    cycle_name (str): name for display on UI
    cycle_dur_s (int): total duration of cycle in seconds 
    sound_list (list): list of sounds chosen for custom cycle soted in ascending order based on sound id
    light_level (int): light intensity from 0 to 100 (inclusive) in increments of 10
    sound_set (bool): whether or not sounds have been set to the custom cycle
    """

  cycle_id: int
  cycle_name: str
  cycle_dur_s: int 
  sound_list: List[(int, str)] = field(default_factory=list)
  light_level: int
  sound_set: bool

  def __post_init__(self):
    """Validates custom cycle components and initializes custom cycle if all is validated."""
  
  # ---------------------------------------------------------------------------
  # duration methods for custom cycle creation
  # ---------------------------------------------------------------------------
  def get_duration(self):
      


  # ---------------------------------------------------------------------------
  # light methods for custom cycle creation
  # ---------------------------------------------------------------------------


  
  # ---------------------------------------------------------------------------
  # sound methods for custom cycle creation
  # ---------------------------------------------------------------------------

