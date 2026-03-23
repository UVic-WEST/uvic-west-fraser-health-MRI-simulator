from dataclasses import dataclass, field

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
  num_sounds: int
  group_volume: int

  def __post_init__(self):
    """Validates configuration of a group of sounds to be played in a custom cycle."""
    if not (1 <= num_sounds <= 3):
      raise ValueError("A group of sounds must contain 1, 2, or 3 sounds")

    if not (0 <= group_volume <= 100):
      raise ValueError("Volume level for a group of sounds must be within 0-100, inclusive")


  def get_group_id(self):
    return self.group_id


  def set_group_id(self, new_group_id):
    self.group_id = new_group_id
  

  def get_num_sounds(self):
    return self.num_sounds
  

  def set_num_sounds(self, new_num_sounds):
    self.num_sounds = new_num_sounds
  

  def get_group_volume(self):
    return self.group_volume
  

  def set_group_volume(self, new_volume):
    self.group_volume = new_volume
