"""Data model for a single MRI simulation cycle.

A CycleConfig holds the cycle metadata (id, name, duration) and an ordered
list of CycleActions that define when lights and sounds should trigger
during playback. Supports JSON serialisation for saving/loading cycles.
"""

from __future__ import annotations

import os
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, TypedDict

from backend.cycle_action import CycleAction, ActionType


class SoundGroupMappingEntry(TypedDict):
    """One sound group as derived from simultaneous SOUND_START actions."""

    sound_names: List[str]
    volume: int

@dataclass
class CycleConfig:
    """
    required attributes and configuration for a single MRI simulation cycle
    attributes:
        cycle_id: unique identifier for MRI simulation cycle
        cycle_name: name for display on UI
        cycle_duration_ms: total duration of cycle in milliseconds
        light_configuration: brightness / light level (0–100)
        actions: list of timestamped (by milliseconds) actions to execute in the cycle

    Convenience getters: ``get_cycle_name``, ``get_duration_ms``, ``get_duration_sec``,
    ``get_brightness``, ``get_lights_on``, ``get_volume``, ``get_sound_group_mapping``,
    ``get_total_groups``.
    """
    cycle_id: int
    cycle_name: str
    cycle_duration_ms: int
    light_configuration: int
    lights_on: bool = True
    volume: int = 50
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

        if not (0 <= self.volume <= 100):
            raise ValueError(f"volume must be 0–100, got {self.volume}")

        # sort actions by timestamp_ms
        self.actions.sort(key=lambda a: a.timestamp_ms)


    @property
    def cycle_duration_sec(self) -> float:
        """get cycle duration in seconds"""
        return self.cycle_duration_ms / 1000.0

    def get_cycle_name(self) -> str:
        """Display name of the cycle."""
        return self.cycle_name

    def get_duration_ms(self) -> int:
        """Total cycle duration in milliseconds."""
        return self.cycle_duration_ms

    def get_duration_sec(self) -> float:
        """Total cycle duration in seconds."""
        return self.cycle_duration_sec

    def get_brightness(self) -> int:
        """Light level / brightness (0–100), stored as ``light_configuration``."""
        return self.light_configuration

    def get_lights_on(self) -> bool:
        """Whether cycle lighting is enabled (JSON ``lights.on``)."""
        return self.lights_on

    def get_volume(self) -> int:
        """Default / master sound volume for the cycle (0–100), JSON ``volume``."""
        return self.volume

    def get_sound_group_mapping(self) -> Dict[int, SoundGroupMappingEntry]:
        """Sound groups derived from simultaneous ``SOUND_START`` actions at each timestamp.

        Keys are 1-based group indices in chronological order. Each value has
        ``sound_names`` (basenames of ``file_name`` parameters) and ``volume``
        (from the first start action in that group, default 50).
        """
        by_ts: Dict[int, List[CycleAction]] = defaultdict(list)
        for action in self.actions:
            if action.action_type == ActionType.SOUND_START:
                by_ts[action.timestamp_ms].append(action)

        result: Dict[int, SoundGroupMappingEntry] = {}
        for group_id, ts in enumerate(sorted(by_ts.keys()), start=1):
            starts = by_ts[ts]
            sound_names: List[str] = []
            volume = 50
            for a in starts:
                p = a.parameters
                fn = p.get("file_name")
                if fn is not None:
                    sound_names.append(os.path.basename(str(fn)))
                if "volume" in p:
                    volume = int(p["volume"])
            entry: SoundGroupMappingEntry = {
                "sound_names": sound_names,
                "volume": volume,
            }
            result[group_id] = entry
        return result

    def get_total_groups(self) -> int:
        """Number of sound groups (distinct SOUND_START time clusters)."""
        return len(self.get_sound_group_mapping())

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


    def get_num_sound_groups(self) -> int:
        """Returns number of sound groups for an instance of CycleConfig."""
        return sum(1 for action in self.actions if action.action_type == ActionType.SOUND_START)


    def to_dict(self):
        return {
            "id": self.cycle_id,
            "name": self.cycle_name,
            "duration_ms": self.cycle_duration_ms,
            "lights": {
                "on": self.lights_on,
                "brightness": self.light_configuration,
            },
            "volume": self.volume,
            "light_configuration": self.light_configuration,
            "actions": [
                {
                    "timestamp": action.timestamp_ms,
                    "type": action.action_type.value,
                    "params": action.parameters
                }
                for action in self.actions
            ],
        }

    @classmethod
    def from_dict(cls, data: dict):
        actions = [
            CycleAction(
                timestamp_ms=a["timestamp"],
                action_type=ActionType(a["type"]),  # safer
                parameters=a.get("params", {}),
            )
            for a in data.get("actions", [])
        ]

        lights = data.get("lights") or {}
        brightness = data.get("light_configuration", 50)
        lights_on = True
        if isinstance(lights, dict) and lights:
            lights_on = bool(lights.get("on", True))
            if "brightness" in lights:
                brightness = int(lights["brightness"])

        volume = int(data.get("volume", 50))

        return cls(
            cycle_id=data["id"],
            cycle_name=data["name"],
            cycle_duration_ms=data["duration_ms"],
            light_configuration=brightness,
            lights_on=lights_on,
            volume=volume,
            actions=actions,
        )
    
    def __repr__(self):
        return (
            f"CycleConfig(id='{self.cycle_id}', "
            f"cycle_name='{self.cycle_name}', "
            f"duration={self.cycle_duration_sec}s, "
            f"actions={len(self.actions)})"
        )
