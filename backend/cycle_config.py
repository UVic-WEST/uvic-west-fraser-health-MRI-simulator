"""Data model for a single MRI simulation cycle.

A CycleConfig holds the cycle metadata (id, name, duration) and an ordered
list of CycleActions that define when lights and sounds should trigger
during playback. Supports JSON serialisation for saving/loading cycles.
"""

from dataclasses import dataclass, field
from typing import List
from backend.cycle_action import CycleAction, ActionType

@dataclass
class CycleConfig:
    """
    required attributes and configuration for a single MRI simulation cycle
    attributes:
        cycle_id: unique identifier for MRI simulation cycle
        cycle_name: name for display on UI
        cycle_duration_ms: total duration of cycle in milliseconds
        actions: list of timestamped (by milliseconds) actions to execute in the cycle
    """
    cycle_id: int
    cycle_name: str
    cycle_duration_ms: int
    light_configuration: int
    actions: List[CycleAction] = field(default_factory=list)

    def __post_init__(self):
        """verify duration and that action durations fit within cycle."""
        if self.cycle_duration_ms <= 0:
            raise ValueError(
                f"total duration of {self.cycle_name} must be positive, got {self.cycle_duration_ms}ms"
            )
     
        for action in self.actions:
            if action.timestamp_ms > self.cycle_duration_ms:
                raise ValueError(
                    f"action at {action.timestamp_ms}ms exceeds cycle duration "
                    f"of {self.cycle_duration_ms}ms"
                )

        # sort actions by timestamp_ms
        self.actions.sort(key=lambda a: a.timestamp_ms)


    @property
    def cycle_duration_sec(self) -> float:
        """get cycle duration in seconds"""
        return self.cycle_duration_ms / 1000.0

    def add_action(self, action: CycleAction):
        """
        add an action to the MRI simulation cycle
        args: 
            action: CycleAction to add
        Raises: 
            ValueError: if action timestamp exceeds cycle duration
        """
        if action.timestamp_ms > self.cycle_duration_ms:
            raise ValueError(
                f"cannot add action at {action.timestamp_ms}ms: "
                f"exceeds cycle duration of {self.cycle_id} of {self.cycle_duration_ms}ms"
            )
        self.actions.append(action)
        self.actions.sort(key=lambda a: a.timestamp_ms)

    def get_actions_at(self, timestamp_ms: int, window_ms: int = 100) -> List[CycleAction]:
        """
        get all actions within the specified window of a given timestamp
        args:
            timestamp_ms: target timestamp
            window_ms: time window (default 100ms for one clock tick)
        returns: 
            list of actions within time window
        """
        return [
            action for action in self.actions
            if abs(action.timestamp_ms - timestamp_ms) < window_ms
        ]

    def to_dict(self):
        return {
            "id": self.cycle_id,
            "name": self.cycle_name,
            "duration_ms": self.cycle_duration_ms,
            "light_configuration": self.light_configuration,
            "actions": [
                {
                    "timestamp": action.timestamp_ms,
                    "type": action.action_type.value,
                    "params": action.parameters
                }
                for action in self.actions
            ]
        }

    @classmethod
    def from_dict(cls, data: dict):
        actions = [
            CycleAction(
                timestamp_ms=a["timestamp"],
                action_type=ActionType(a["type"]),  # safer
                parameters=a.get("params", {})
            )
            for a in data.get("actions", [])
        ]

        return cls(
            cycle_id=data["id"],
            cycle_name=data["name"],
            cycle_duration_ms=data["duration_ms"],
            light_configuration=data.get("light_configuration", 50),
            actions=actions
        )
    
    def __repr__(self):
        return (
            f"CycleConfig(id='{self.cycle_id}', "
            f"cycle_name='{self.cycle_name}', "
            f"duration={self.cycle_duration_sec}s, "
            f"actions={len(self.actions)})"
        )
