from dataclasses import dataclass, field
from typing import List

@dataclass
class SoundGroup:
  """
  Configures a grouping of sounds to play during a custom MRI simulation cycle. An instance of SoundGroup is 
  used is an entry in the sound_list list attribute in CreateCycleLogic class.

  ATTRIBUTES:
    group_id (int): unique identifier for a group of sounds
    num_sounds (int): number of sounds in a group; must be within 1-3, inclusive
    group_volume (int): single volume level set for a group of sounds; must be within 0-100, inclusive
  """
  group_id: int
  group_volume: int
  sound_ids: List[int] = field(default_factory=list)

  def __post_init__(self):
    """Validates configuration of a group of sounds to be played in a custom cycle."""
    if not (1 <= len(self.sound_ids) <= 3):
      raise ValueError("A group of sounds must contain 1-3 sounds, inclusive")

    if not (0 <= self.group_volume <= 100):
      raise ValueError("Volume level for a group of sounds must be within 0-100, inclusive")

  # ------------------------------------------------------------------
  # Setters
  # ------------------------------------------------------------------
  def set_group_id(self, new_group_id):
    self.group_id = new_group_id
  
  def set_num_sounds(self, new_num_sounds):
    self.num_sounds = new_num_sound
  
  def set_group_volume(self, new_volume):
    self.group_volume = new_volume

  # ------------------------------------------------------------------
  # Getters
  # ------------------------------------------------------------------
  def get_group_id(self):
    return self.group_id

  def get_num_sounds(self):
    return len(self.sound_ids)

  def get_group_volume(self):
    return self.group_volume
  
  # ------------------------------------------------------------------
  # sound group modification methods
  # ------------------------------------------------------------------
  def add_sound(self, new_sound_id):
    if len(sound_ids) >= 3:
      raise ValueError(f"A group cannot contain more then 3 sounds: group {self.group_id} already "
                       f"contains {len(self.sound_ids)} sounds")

    if new_sound_id in self.sound_ids:
            return  # avoid duplicates

    self.sound_ids.append(new_sound_id)
    

  def remove_sound(self, sound_id: int):
    if len(self.sound_ids) == 0:
      raise ValueError("A group must have at least 1 sound")

    if sound_id in self.sound_ids:
      self.sound_ids.remove(sound_id)
            
