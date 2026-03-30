from PySide6.QtCore import QObject, Signal
from typing import List, Tuple
from dataclasses import dataclass, field, asdict
import json

DEFAULT_LIGHT_LEVEL = 50
DEFAULT_SOUND_LEVEL = 50
DEFAULT_NUM_GROUPS = 4
DEFAULT_CYCLE_DURATION_S = 300 # default duration (in seconds) of custom cycle is 300s (5 min)


class CreateCycleLogic(QObject):
  """
  Bridges between L1 (CreateCyclePages) and L2 to create, display, and save a custom cycle to json file.

  ATTRIBUTES:
    cycle_id (int): unique identifier for custom MRI simulation cycle
    cycle_name (str): name for display on UI
    cycle_dur_s (int): total duration of cycle in seconds 
    light_level (int): light intensity from 0 to 100 (inclusive) in increments of 10
    sound_set (bool): whether or not sounds have been set to the custom cycle
    group_list (List[SoundGroup]): list of groups of SoundGroup instances to be played during custom cycle
    available_sounds (List[(int, str)]): list of tuples, (sound_id, sound_name), each representing a sound available in system to select for custom cycle
  """
  #---------------------------------------------------------------------------
  # internal SoundGroup dataclass
  # ---------------------------------------------------------------------------
  @dataclass
  class SoundGroup:
    """
    Handles configuration of sound groups to be played during a custom cycle

    ATTRIBUTES:
      group_id (int): unique identifier for a group of sounds
      group_volume (int): single volume level set for a group of sounds; must be within 0-100, inclusive
      sound_ids (List[int]): list of sound ids for sounds to be played in custom cycle
    """
    group_id: int
    group_volume: int = DEFAULT_SOUND_LEVEL
    sound_ids: List[int] = field(default_factory=list)

  
  #---------------------------------------------------------------------------
  # signals to emit to communicate with frontend
  # ---------------------------------------------------------------------------
  light_level_set = Signal(int)
  duration_set = Signal(int)
  volume_set = Signal(int)
  sample_playing = Signal(int)
  groups_changed = Signal(int)


  def __init__(self, cycle_id: int, cycle_name: str, cycle_dur_s: int = DEFAULT_CYCLE_DURATION_s, light_level: int = DEFAULT_LIGHT_LEVEL, sound_set: bool = False, group_list: List["CreateCycleLogic.SoundGroup"] | None = None):
    super().__init__()
    
    self.cycle_id = cycle_id
    self.cycle_name = cycle_name
    self.cycle_dur_s = cycle_dur_s
    self.light_level = light_level
    self.sound_set = sound_set
    self.group_list = group_list or []

    # list of available sounds; hardcoded for now with assumption that there are 8 available sounds in system
    self.available_sounds: List[Tuple[int, str]] = [
      (1, "Sound 1"),
      (2, "Sound 2"),
      (3, "Sound 3"),
      (4, "Sound 4"),
      (5, "Sound 5"),
      (6, "Sound 6"),
      (7, "Sound 7"),
      (8, "Sound 8"),
    ]


  #---------------------------------------------------------------------------
  # get list of all sounds available in system
  # ---------------------------------------------------------------------------
  def get_sounds(self) -> List[Tuple[int, str]]:
    return sorted(self.available_sounds, key=lambda x: x[0])
  

  #---------------------------------------------------------------------------
  # helper function to search for sound group in selected cycle sounds given group_id
  # --------------------------------------------------------------------------
  def _get_group(self, group_id: int) -> "SoundGroup":
    for group in self.group_list:
        if group.group_id == group_id:
            return group
    raise ValueError(f"Group {group_id} not found")
  

  #---------------------------------------------------------------------------
  # global validation
  # ---------------------------------------------------------------------------
  def validate_cycle(self) -> Tuple[bool, List[str]]:
    """
    Validates the configuration of entire custom cycle once creation is deemed complete by user.

    RETURNS:
        (is_valid, list_of_errors)
    """
    errors = []

    # cycle name
    if not self.cycle_name or not self.cycle_name.strip():
        errors.append("Cycle name cannot be empty")

    # duration
    if not (60 <= self.cycle_dur_s <= 900) or self.cycle_dur_s % 30 != 0:
        errors.append("Cycle duration must be 60–900 seconds in steps of 30")

    # light level
    if not (0 <= self.light_level <= 100) or self.light_level % 10 != 0:
        errors.append("Light level must be 0–100 in steps of 10")

    # sound groups exist
    if len(self.group_list) == 0:
        errors.append("At least one sound group is required")

    # group-level validation
    for group in self.group_list:
        if not (0 <= group.group_volume <= 100):
            errors.append(f"Group {group.group_id}: volume must be 0–100")

        if not (1 <= len(group.sound_ids) <= 3):
            errors.append(f"Group {group.group_id}: must have 1–3 sounds")

        # ensure sound IDs are valid
        valid_sound_ids = {sid for sid, _ in self.available_sounds}
        invalid = [sid for sid in group.sound_ids if sid not in valid_sound_ids]
        if invalid:
            errors.append(f"Group {group.group_id}: invalid sound IDs {invalid}")

    return (len(errors) == 0, errors)
  
  
  # ---------------------------------------------------------------------------
  # duration methods for custom cycle creation
  # ---------------------------------------------------------------------------
  def get_duration(self) -> int:
      return self.cycle_dur_s
    

  def set_duration(self, new_cycle_dur_s: int) -> bool:
    """
    Validates that new_cycle_dur_s is within the set values [60, 900] and, if so, sets duration of custom cycle to new_cycle_dur_s.

    ARGUMENTS:
      new_cycle_dur_ms: duration to which custom cycle is set

    RETURNS:
      True (for validation)

    RAISES:
      ValueError: if new_cycle_dur_s not within [60, 900] seconds or if new_cycle_dur_s not multiple of 30

    EMITS: signal that the duration, in seconds, of custom cycle has been set to new_cycle_dur_s
    """
    if not (60 <= new_cycle_dur_s <= 900) or new_cycle_dur_s % 30 != 0:
      raise ValueError("Cycle duration must be within 60s-900s (1min-15min), inclusive, and in steps of 30s")
      
    self.cycle_dur_s = new_cycle_dur_s
    self.duration_set.emit(new_cycle_dur_s)
    return True
  

  # ---------------------------------------------------------------------------
  # light methods for custom cycle creation
  # ---------------------------------------------------------------------------
  def get_light_level(self) -> int:
    return self.light_level
    

  def set_light_level(self, new_light_level: int) -> bool:
    """
    Validates that new_light_level is within the set values [0, 100] and, if so, sets light level of custom cycle to new_light_level.

    ARGUMENTS:
      new_light_level: light intensity to which custom cycle light level is set

    RETURNS:
      True (for validation)

    RAISES:
      ValueError: if new_light_level not within [0, 100] or if new_light_level not multiple of 10

    EMITS: signal that light level of custom cycle has been set to new_light_level

    """
    if not (0 <= new_light_level <= 100) or new_light_level % 10 != 0:
      raise ValueError("Light level must be within 0–100, inclusive, and in steps of 10")
      
    self.light_level = new_light_level
    self.light_level_set.emit(new_light_level)
    return True
    

  def display_light_level(self, light_level: int) -> bool:
    self.light_level_set.emit(light_level)
    return True
  
  
  def reset_light_default(self):
     self.set_light_level(DEFAULT_LIGHT_LEVEL)


  # ---------------------------------------------------------------------------
  # sound group methods for custom cycle creation
  # ---------------------------------------------------------------------------
  def get_total_groups(self) -> Tuple[int, bool]:
    if not self.sound_set:
      return DEFAULT_NUM_GROUPS, self.sound_set  # default values if sounds have not been set yet
    
    return len(self.group_list), self.sound_set
    

  def set_total_groups(self, new_total_groups: int) -> bool:
    """
    Validates that new_total_groups is within the set values [1, 8] and, if so, sets number of groups of custom cycle to new_total_groups.

    ARGUMENTS:
      new_total_groups: number of sound groups to be played during custom cycle

    RETURNS:
      True (for validation)

    RAISES:
      ValueError: if new_total_groups not within [1, 8]

    EMITS: signal that number of sound groups of custom cycle has been set to new_total_groups
    """
    if not (1 <= new_total_groups <= 8):
      raise ValueError("Total groups must be between 1 and 8")

    current = len(self.group_list)

    # Case 1: Reduce number of groups
    if new_total_groups < current:
      self.group_list = self.group_list[:new_total_groups]

    # Case 2: Increase number of groups
    elif new_total_groups > current:
      for i in range(current, new_total_groups):
        self.group_list.append(
          CreateCycleLogic.SoundGroup(
            group_id = i + 1,
            group_volume = DEFAULT_SOUND_LEVEL,
            sound_ids = []  # empty for now (UI will fill)
          )
        )

    # Re-index group IDs
    for i, group in enumerate(self.group_list):
        group.group_id = i + 1

    self.groups_changed.emit(new_total_groups)     
    return True
  

  def reset_group_default(self):
     self.set_total_groups(DEFAULT_NUM_GROUPS)
      

  # ---------------------------------------------------------------------------
  # sound to group mapping methods for custom cycle creation
  # ---------------------------------------------------------------------------
  def get_sounds_in_group(self, group_id: int):
    """
    Gets a list of sounds belonging to a group if group with group_id is in the list of groups to be played during custom cycle.

    ARGUMENTS:
      group_id: unique identifier of the sound group from which sounds are wanted

    RETURNS:
      group.sound_ids: a list of sound ids for each sound within the group identified by group_id

    RAISES:
      ValueError: from _get_group(self, group_id) if group not found in list of groups to be played during custom cycle
    """
    group = self._get_group(group_id)  # _get_group(self, group_id) validates that group_id is in group list to be played during cycle
    return group.sound_ids if group.sound_ids else None
    

  def set_sounds_in_group(self, group_id: int, sound_list: List[int]) -> bool:
    """
    Given a group_id, sets the sounds for this group to be played during custom cycle.

    ARGUMENTS: 
      group_id: unique identifier of the sound group for which sounds are to be chosen
      sound_list: the list of sounds to be put into the group identified by group_id

    RETURNS:
      True (for validation)

    RAISES:
      ValueError: if number of sounds in sound_list chosen for group with group_id is not within [1, 3]
      ValueError: from _get_group(self, group_id) if group not found in list of groups to be played during custom cycle
    """
    if not (1 <= len(sound_list) <= 3):
        raise ValueError("Each group must have 1–3 sounds")

    group = self._get_group(group_id)
    group.sound_ids = list(sound_list)
    return True
  

  def set_volume_for_group(self, group_id: int, new_group_volume: int) -> bool:
    """
    Validates that new_group_volume is within the set values [0, 100] and, if so, sets the volume of the group identified by group_id to new_group_volume.

    ARGUMENTS:
      group_id: unique identifier of the sound group for which sounds are to be chosen
      new_group_volume: volume level to which group identified by group_id is set

    RETURNS:
      True (for validation)

    RAISES:
      ValueError: if new_group_volume not within [0, 100]
      ValueError: from _get_group(self, group_id) if group not found in list of groups to be played during custom cycle

    EMITS: signal that the volume gor the group identified by group_id has been set to new_group_volume
    """
    if not (0 <= new_group_volume <= 100):
        raise ValueError("Volume must be within 0–100, inclusive")

    group = self._get_group(group_id)
    group.group_volume = new_group_volume
    self.volume_set.emit(new_group_volume)
    return True
  

  def play_group_sample(self, group_id: int) -> bool:
    group = self._get_group(group_id)

    if not group.sound_ids:
        return False

    self.sample_playing.emit(group_id)
    return True
  

  def sound_mapping_accessed(self):
     self.sound_set = True


  def confirm_sounds_in_each_group(self):
    return all(1 <= len(group.sound_ids) <= 3 for group in self.group_list)
  
  
  def reset_volume_default(self, group_id):
     self.set_volume_for_group(group_id, DEFAULT_SOUND_LEVEL)
    
  # ---------------------------------------------------------------------------
  # save/load set custom cycle data to json file
  # ---------------------------------------------------------------------------
  def save_cycle(self):
    return
