"""
CycleAction: represents a single timestamped action within a MRI simulation cycle

Stores when an action should occur (timestamp_ms), what type of
action it is (action_type), and any parameters needed to execute the
action (parameters)
"""
from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum

@dataclass
class CycleAction:
  """configures single timestamped (in milliseconds) action with a cycle"""
  timestamp_ms: int  #when to execute action in relation to cycle start (in milliseconds)
  #action_type: str  #strings such as "sound_start", "light_stop", "light_reset", etc.
  action_type: ActionType
  parameters: Dict[str, Any]  #parameters specific to action (if any)

  def __post_init__(self):
    """
    validate action data
  
    raises:
      ValueError: if timestamp_ms is negative
      ValueError: if action_type is empty string
      ValueError: if parameters is not a dictionary
    """
    # Convert string to enum
    if isinstance(self.action_type, str):
      self.action_type = ActionType(self.action_type)

    if self.timestamp_ms < 0:
      raise ValueError(
        "timestamp_ms must be non-negative"
      )
    if not self.action_type:
      raise ValueError(
        "action_type must be non-empty string"
      )
    if not isinstance(self.parameters, dict):
      raise ValueError(
        "parameters must be a dictionary"
      )


  def is_execution_time(self, current_ms: int, last_check_ms: int) -> bool:
    """
    check if action should execute between last check and current time

    args:
      current_ms: current elapsed time in milliseconds
      last_check_ms: last time checking if an action should be executed

    returns:
      True if action's timestamp is between last check and current time
    """
    return last_check_ms < self.timestamp_ms <= current_ms


  def __repr__(self):
    return (
      f"CycleAction(timestamp_ms={self.timestamp_ms}, "
      f"action_type='{self.action_type}', "
      f"parameters={self.parameters})"
    )


#class ActionType:
#  """constants for commonly used action types"""
#  SOUND_START = "sound_start"
#  SOUND_STOP = "sound_stop"
#  SOUND_RESET = "sound_reset"  #resets sound to safe decibel level
#  LIGHT_ON = "light_on"
#  LIGHT_OFF = "light_off"
#  LIGHT_RESET = "light_reset"  #resets light intensity to safe level
  
class ActionType(Enum):
    SOUND_START = "sound_start"
    SOUND_STOP = "sound_stop"
    SOUND_RESET = "sound_reset"
    LIGHT_ON = "light_on"
    LIGHT_OFF = "light_off"
    LIGHT_RESET = "light_reset"