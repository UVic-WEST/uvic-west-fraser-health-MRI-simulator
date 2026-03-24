"""Data model for a single timestamped action within an MRI simulation cycle.

Each CycleAction stores when the action should fire (timestamp_ms), what
kind of action it is (ActionType), and any parameters needed to execute it
(e.g. brightness level, sound file name, volume).
"""

from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum


class ActionType(Enum):
    """Enumeration of supported cycle action types.

    Used by CycleController.dispatch_action() to route each action to the
    correct hardware controller (LightController or SoundPlayer).
    """

    SOUND_START = "sound_start"
    SOUND_STOP = "sound_stop"
    SOUND_RESET = "sound_reset"
    LIGHT_ON = "light_on"
    LIGHT_OFF = "light_off"
    LIGHT_RESET = "light_reset"


@dataclass
class CycleAction:
    """A single timestamped action within a cycle.

    Attributes:
        timestamp_ms (int): When to execute relative to cycle start (ms).
        action_type (ActionType): The type of action to perform.
        parameters (Dict[str, Any]): Action-specific parameters
            (e.g. {"brightness": 0.8} for LIGHT_ON, {"file_name": "mri.wav",
            "duration": 5.0, "volume": 50} for SOUND_START).
    """
    timestamp_ms: int
    action_type: ActionType
    parameters: Dict[str, Any]

    def __post_init__(self):
        """Validate and normalise action data.

        Converts string action_type values to ActionType enum members.

        Raises:
            ValueError: If timestamp_ms is negative.
            ValueError: If action_type is empty.
            ValueError: If parameters is not a dictionary.
        """
        if isinstance(self.action_type, str):
            self.action_type = ActionType(self.action_type)

        if self.timestamp_ms < 0:
            raise ValueError("timestamp_ms must be non-negative")
        if not self.action_type:
            raise ValueError("action_type must be non-empty")
        if not isinstance(self.parameters, dict):
            raise ValueError("parameters must be a dictionary")

    def is_execution_time(self, current_ms: int, last_check_ms: int) -> bool:
        """Check whether this action should fire in the current tick window.

        Args:
            current_ms (int): Current elapsed time in milliseconds.
            last_check_ms (int): Elapsed time at the previous tick.

        Returns:
            bool: True if timestamp_ms falls in (last_check_ms, current_ms].
        """
        return last_check_ms < self.timestamp_ms <= current_ms

    def __repr__(self):
        return (
            f"CycleAction(timestamp_ms={self.timestamp_ms}, "
            f"action_type='{self.action_type}', "
            f"parameters={self.parameters})"
        )

