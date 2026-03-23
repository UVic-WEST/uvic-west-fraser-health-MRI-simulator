from PySide6.QtCore import QObject, Signal
from typing import List, Tuple
import json
from backend.sound_group import SoundGroup

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
  # duration_changed = Signal(int)
  # sounds_changed = Signal()
  light_level_set = Signal(int)
  sample_playing = Signal(int)

  cycle_id: int
  cycle_name: str
  cycle_dur_s: int = 180
  sound_list: List[Tuple[int, str]] = field(default_factory=list)
  light_level: int = 50
  sound_set: bool = False

  def __init__(self, cycle_id: int, cycle_name: str, cycle_dur_s: int = 180, light_level: int = 50, sound_set: bool = False, sound_list: Lists[Tuple[int, str]] | None = None):
    super().__init__()
    
    self.cycle_id = cycle_id
    self.cycle_name = cycle_name
    self.cycle_dur_s = cycle_dur_s
    self.light_level = light_level
    self.sound_set = sound_set
    self.sound_list = sound_list or []

    self._validate()
    
  
  def validate(self):
    """Validates custom cycle components."""
    if not (60 <= self.cycle_dur_s <= 900):
      raise ValueError("Cycle duration must be within 60s-900s (1min-15min), inclusive")

    if not (0 <= self.light_level <= 100) or self.light_level % 10 != 0:
      raise ValueError("Light level must be within 0–100, inclusive, and in steps of 10")

    if not (1 <= len(sound_list) <= 8):
      raise ValueError("Must have between 1 and 8 sound groupings per custom cycle")

    self.sound_list.sort(key=lambda x: x[0])
  
  # ---------------------------------------------------------------------------
  # duration methods for custom cycle creation
  # ---------------------------------------------------------------------------
  def get_duration(self):
      """ Gets current duration of custom cycle in seconds.
      
      RETURNS: cycle_dur_s (int)
      """
      return self.cycle_dur_s
    

  def set_duration(self, new_cycle_dur_s: int):
    if not (60 <= self.cycle_dur_s <= 900):
      raise ValueError("Cycle duration must be within 60s-900s (1min-15min), inclusive")
      
    self.cycle_dur_s = new_cycle_dur_s
    # self.duration_changed.emit(new_cycle_dur_s)
    return True

  # ---------------------------------------------------------------------------
  # light methods for custom cycle creation
  # ---------------------------------------------------------------------------
  def get_light_level(self):
    return self.light_level
    

  def set_light_level(self, new_light_level):
    if not (0 <= self.light_level <= 100) or self.light_level % 10 != 0:
      raise ValueError("Light level must be within 0–100, inclusive, and in steps of 10")
      
    self.light_level = new_light_level
    # self.light_level_changed.emit(new_light_level)
    return True
    

  def display_light_level(self, light_level: int):
    return
    

  # ---------------------------------------------------------------------------
  # sound group methods for custom cycle creation
  # ---------------------------------------------------------------------------
  def get_total_groups(self):
    return len(self.sound_list), sound_set
    

  def set_total_groups(self, new_total_groups):
    if not (1 <= new_total_groups <= 8):
      raise ValueError("Must have between 1 and 8 sound groupings per custom cycle")

    current = len(self.sound_list)

    # Case 1: Too many groups so trim sound_list
    if new_total_groups < current:
        self.sound_list = self.sound_list[:new_total_groups]

    # Case 2: Too few groups so add to sound_list
    elif new_total_groups > current:
        for i in range(current, new_total_groups):
            new_group = SoundGroup(
                group_id=i + 1,
                group_volume=50,
                sound_ids=[0]  # placeholder (must satisfy 1–3 rule)
            )
            self.sound_list.append(new_group)

    return True
      

  # ---------------------------------------------------------------------------
  # sound to group mapping methods for custom cycle creation
  # ---------------------------------------------------------------------------
  def get_sounds_in_group(self, group_id: int):
    return

  def set_sounds_in_group(self, group_id: int, sounds: List[]int):
    return True

  def set_volume_for_group(self, new_group_volume):
    return True

  def play_group_sample(self, group_id):
    return

  def confirm_sounds_in_each_group(self):
    return True
    

  # ---------------------------------------------------------------------------
  # save set custom cycle to json file
  # ---------------------------------------------------------------------------
  def save_to_json(self):
    return




