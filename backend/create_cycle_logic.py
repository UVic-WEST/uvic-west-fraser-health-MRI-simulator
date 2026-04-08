from __future__ import annotations

from typing import List, Tuple

from backend.sound_config import SoundConfig
from backend.sound_group_config import SoundGroupConfig
from backend.cycle_action import CycleAction, ActionType
from backend.cycle_config import CycleConfig
from backend.cycle_repository import CycleRepository
from embedded.light_controller import LightController
from embedded.sound_player import SoundPlayer

DEFAULT_LIGHT_LEVEL = 50
DEFAULT_SOUND_LEVEL = 50
DEFAULT_NUM_GROUPS = 4
DEFAULT_CYCLE_DURATION = 300  # 5 minutes

class CreateCycleLogic:
    """Handles creation of custom MRI cycles (L2 logic)."""
    
    # ---------------- INIT ----------------
    def __init__(
        self,
        cycle_id: int,
        cycle_name: str,
        light_controller: LightController,
        sound_player: SoundPlayer,
    ):
        self.cycle_id = cycle_id
        self.cycle_name = cycle_name
        self.light_controller = light_controller
        self.sound_player = sound_player

        self.cycle_duration = DEFAULT_CYCLE_DURATION
        self.light_level = DEFAULT_LIGHT_LEVEL
        self.group_list: List[SoundGroupConfig] = []
        
        self.sound_set = False 

        # list of available sounds; hardcoded for now with assumption that there are 8 available sounds in system
        self.available_sounds: List[Tuple[int, str]] = [
        (1, "Pulse"),
        (2, "Drill(S)"),
        (3, "Drill(M)"),
        (4, "Beeps"),
        (5, "Scan"),
        (6, "Alarm"),
        (7, "Buzz"),
        (8, "Drill(L)"),
        ]
        
    # =========================================================
    # DURATION
    # =========================================================
    def get_duration(self):
        """Return current duration in seconds."""
        return self.cycle_duration

    def set_duration(self, value: int) -> bool:
        if not (60 <= value <= 900) or value % 30 != 0:
            raise ValueError("Duration must be 60-900 seconds in steps of 30")

        self.cycle_duration = value
        return True
    
    # =========================================================
    # LIGHT LEVEL
    # =========================================================
    def get_light_level(self) -> int:
        return self.light_level

    def set_light_level(self, value: int) -> bool:
        if not isinstance(value, int):
            raise ValueError("Light level must be int")

        if not (0 <= value <= 100) or value % 10 != 0:
            raise ValueError("Light level must be 0-100 in steps of 10")

        self.light_level = value
        return True

    def display_light_level(self, light_level: int) -> bool:
        """Preview brightness on hardware."""
        if not isinstance(light_level, int):
            raise ValueError("Light level must be int")

        if not (0 <= light_level <= 100) or light_level % 10 != 0:
            return False

        brightness = light_level / 100.0

        if self.light_controller:
            self.light_controller.change_lights(brightness)

        return True

    def reset_light_default(self):
        self.light_level = DEFAULT_LIGHT_LEVEL
        
    
    # ---------------------------------------------------------------------------
    # SOUND GROUPS
    # ---------------------------------------------------------------------------
    # previous version had get_total_groups and set_total_groups combined with sound mapping, but separating them to simplify logic and validation around total groups vs sounds in each group
    def get_total_groups(self) -> Tuple[int, bool]:
        """Return number of groups and whether sound mapping has been accessed."""
        # Always return the current group count, and whether sound mapping has been accessed
        return len(self.group_list) if self.group_list else DEFAULT_NUM_GROUPS, getattr(self, "sound_set", False)

    def set_total_groups(self, new_total_groups: int) -> bool:
        """
        Validates that new_total_groups is within the set values [1, 8] and, if so, sets number of groups of custom cycle to new_total_groups.

        ARGUMENTS:
        new_total_groups: number of sound groups to be played during custom cycle

        RETURNS:
        True (for validation)

        RAISES:
        ValueError: if new_total_groups not within [1, 8]
        """
        if not (1 <= new_total_groups <= 8):
            raise ValueError("Total groups must be between 1 and 8")

        current = len(self.group_list)

        # Reduce number of groups
        if new_total_groups < current:
            self.group_list = self.group_list[:new_total_groups]

        # Increase number of groups
        elif new_total_groups > current:
            for i in range(current, new_total_groups):
                self.group_list.append(
                    SoundGroupConfig(group_id=i + 1, group_volume=DEFAULT_SOUND_LEVEL)
                )

        # Reindex group IDs
        for i, group in enumerate(self.group_list):
            group.group_id = i + 1
        return True

    def reset_group_default(self):
        self.set_total_groups(DEFAULT_NUM_GROUPS)
      
    # =========================================================
    # SOUND MAPPING
    # =========================================================
        
    def get_sounds_in_group(self, group_id: int) -> List[SoundConfig] | None:
        print(f"[CreateCycleLogic.get_sounds_in_group] CALLED with group_id={group_id}")
        """
        Gets a list of sounds belonging to a group if group with group_id is in the list of groups to be played during custom cycle.

        ARGUMENTS:
        group_id: unique identifier of the sound group from which sounds are wanted

        RETURNS:
        group.sound_ids: a list of sound ids for each sound within the group identified by group_id

        RAISES:
        ValueError: from _get_group(self, group_id) if group not found in list of groups to be played during custom cycle
        """
        group = self._get_group(group_id)
        print(f"[CreateCycleLogic.get_sounds_in_group] returning sounds: {group.sounds if group.sounds else None}")
        return group.sounds if group.sounds else None
    
    def set_sounds_in_group(self, group_id: int, sounds: List[SoundConfig], allow_empty: bool = False) -> bool:
        print(f"[CreateCycleLogic.set_sounds_in_group] CALLED with group_id={group_id}, sounds={sounds}, allow_empty={allow_empty}")
        """
        Given a group_id, sets the sounds for this group to be played during custom cycle.

        ARGUMENTS: 
        group_id: unique identifier of the sound group for which sounds are to be chosen
        sound_list: the list of sounds to be put into the group identified by group_id
        allow_empty: if True, allows setting the group to have zero sounds (for default/reset)

        RETURNS:
        True (for validation)

        RAISES:
        ValueError: if number of sounds in sound_list chosen for group with group_id is not within [1, 3] (unless allow_empty is True)
        ValueError: from _get_group(self, group_id) if group not found in list of groups to be played during custom cycle
        """
        if not allow_empty and not (1 <= len(sounds) <= 3):
            print(f"[CreateCycleLogic.set_sounds_in_group] Invalid number of sounds: {len(sounds)}")
            raise ValueError("Each group must have 1–3 sounds")
        if allow_empty and len(sounds) == 0:
            print(f"[CreateCycleLogic.set_sounds_in_group] Allowing empty group {group_id}")
        group = self._get_group(group_id)
        print(f"[CreateCycleLogic.set_sounds_in_group] setting group {group_id} sounds to: {sounds}")
        group.sounds = sounds
        print(f"[CreateCycleLogic.set_sounds_in_group] Set group {group_id} sounds to: {group.sounds}")
        return True
    
    def set_volume_for_group(self, group_id: int, new_group_volume: int) -> bool:
        print(f"[CreateCycleLogic.set_volume_for_group] CALLED with group_id={group_id}, new_group_volume={new_group_volume}")
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
        """
        if not (0 <= new_group_volume <= 100):
            print(f"[CreateCycleLogic.set_volume_for_group] Invalid volume: {new_group_volume}")
            raise ValueError("Volume must be within 0-100")
        group = self._get_group(group_id)
        print(f"[CreateCycleLogic.set_volume_for_group] setting group {group_id} volume to: {new_group_volume}")
        group.group_volume = new_group_volume
        print(f"[CreateCycleLogic.set_volume_for_group] Set group {group_id} volume to: {group.group_volume}")
        return True

    def play_group_sample(self, group_id: int) -> bool:
        print(f"[CreateCycleLogic.play_group_sample] CALLED with group_id={group_id}")
        group = self._get_group(group_id)
        if not group.sounds:
            print(f"[CreateCycleLogic.play_group_sample] No sounds in group {group_id}")
            return False
        if self.sound_player:
            for sound in group.sounds:
                self.sound_player.play(sound)
        return True

    def sound_mapping_accessed(self):
        self.sound_set = True

    def confirm_sounds_in_each_group(self) -> bool:
        return all(1 <= len(group.sounds) <= 3 for group in self.group_list)
    
    def reset_volume_default(self, group_id: int):
        try:
            self.set_volume_for_group(group_id, DEFAULT_SOUND_LEVEL)
        except ValueError:
            pass
        
    #---------------------------------------------------------------------------
    # get list of all sounds available in system
    # ---------------------------------------------------------------------------
    def get_sounds(self) -> List[Tuple[int, str]]:
        return sorted(self.available_sounds, key=lambda x: x[0])
    

    #---------------------------------------------------------------------------
    # helper function to search for sound group in selected cycle sounds given group_id
    # --------------------------------------------------------------------------
    def _get_group(self, group_id: int) -> "SoundGroupConfig":
        for group in self.group_list:
            if group.group_id == group_id:
                return group
        raise ValueError(f"Group {group_id} not found")
  

    # =========================================================
    # VALIDATION
    # =========================================================
    def validate_cycle(self) -> Tuple[bool, List[str]]:
        errors = []

        # ---------------- NAME ----------------
        if not isinstance(self.cycle_name, str) or not self.cycle_name.strip():
            errors.append("Cycle name cannot be empty")

        # ---------------- DURATION ----------------
        if not isinstance(self.cycle_duration, int):
            errors.append("Duration must be an integer")
        elif not (60 <= self.cycle_duration <= 900):
            errors.append("Duration must be between 60 and 900 seconds")
        elif self.cycle_duration % 30 != 0:
            errors.append("Duration must be in increments of 30 seconds")

        # ---------------- LIGHT LEVEL ----------------
        if not isinstance(self.light_level, int):
            errors.append("Light level must be an integer")
        elif not (0 <= self.light_level <= 100):
            errors.append("Light level must be between 0 and 100")
        elif self.light_level % 10 != 0:
            errors.append("Light level must be in increments of 10")

        # ---------------- SOUND GROUPS ----------------
        if not self.group_list:
            errors.append("At least one sound group is required")
        else:
            for group in self.group_list:
                if not (0 <= group.group_volume <= 100):
                    errors.append(f"Group {group.group_id}: volume must be 0–100")

                if not group.sounds or not (1 <= len(group.sounds) <= 3):
                    errors.append(f"Group {group.group_id}: must have 1–3 sounds")

        return (len(errors) == 0, errors)
    
    # =========================================================
    # PRIVATE: GENERATE CYCLE ACTIONS
    # =========================================================
    def _generate_cycle_actions(self) -> List[CycleAction]:
        """
        Create timestamped actions for this cycle.
        
        - Splits total duration equally among all groups
        - Each group duration contains simultaneous SOUND_START for all its sounds
        - SOUND_STOP scheduled at the end of the group duration
        """
        actions: List[CycleAction] = []

        num_groups = len(self.group_list)
        if num_groups == 0:
            return actions  # nothing to schedule

        total_duration_ms = self.cycle_duration * 1000
        base_group_duration = total_duration_ms // num_groups
        remainder = total_duration_ms % num_groups  # leftover ms to add to last group

        current_time = 0

        for i, group in enumerate(self.group_list):
            group_duration = base_group_duration
            if i == num_groups - 1:
                # add remainder to last group to match total duration exactly
                group_duration += remainder

            # start all sounds in group simultaneously
            if group.sounds:
                for sound in group.sounds:
                    actions.append(
                        CycleAction(
                            timestamp_ms=current_time,
                            action_type=ActionType.SOUND_START,
                            parameters={
                                "file_name": sound.file_name,
                                "volume": group.group_volume,
                                "duration_ms": group_duration,
                            },
                        )
                    )
                # stop all sounds at the end of group duration
                for sound in group.sounds:
                    actions.append(
                        CycleAction(
                            timestamp_ms=current_time + group_duration,
                            action_type=ActionType.SOUND_STOP,
                            parameters={"file_name": sound.file_name},
                        )
                    )

            current_time += group_duration
        return actions

    # =========================================================
    # SAVE CYCLE
    # =========================================================
    def save_cycle(self) -> CycleConfig | None:
        """
        Validate cycle and save it with generated actions.
        Returns the saved CycleConfig, or None if validation fails.
        """
        is_valid, errors = self.validate_cycle()
        if not is_valid:
            print("Cycle validation failed:", errors)
            return None

        new_id = CycleRepository.get_next_id()
        new_name = f"Cycle {new_id}"

        actions = self._generate_cycle_actions()

        cycle_volume = (
            round(sum(g.group_volume for g in self.group_list) / len(self.group_list))
            if self.group_list
            else DEFAULT_SOUND_LEVEL
        )

        cycle = CycleConfig(
            cycle_id=new_id,
            cycle_name=new_name,
            cycle_duration_ms=self.cycle_duration * 1000,
            light_configuration=self.light_level,
            lights_on=True,
            volume=cycle_volume,
            actions=actions,
        )

        CycleRepository.add_cycle(cycle)
        return cycle