"""Manual sound controller (Layer 2).

Lets the user play up to 3 sounds simultaneously at a chosen volume,
outside of a running cycle. Reserves the Layer 3 SoundPlayer while
active and cuts all sounds when closed.
"""

import os
from typing import List, Tuple

from PySide6.QtCore import QObject, QTimer

from backend.sound_config import SoundConfig

SOUNDS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "resources", "sounds"
)


SUPPORTED_EXTENSIONS = (".wav", ".mp3")
MAX_SIMULTANEOUS_SOUNDS = 3

# Sample playback time limit in seconds
SAMPLE_PLAYBACK_SECONDS = 10


class ManualSoundController(QObject):
    """Backend logic for manual sound control on the home page.

    While active, the user can play up to 3 sounds at the same volume.
    When deactivated, all sounds are stopped and the Layer 3 SoundPlayer
    is released.

    Attributes:
        sound_player: Layer 3 SoundPlayer instance.
        is_active (bool): Whether the manual controller is currently in use.
        current_sounds (List[int]): IDs of currently playing sounds.
        current_volume (int): Volume for all playing sounds (0–100).
    """

    def __init__(self, sound_player, parent=None):
        """Initialise with a reference to the Layer 3 sound player.

        Args:
            sound_player (SoundPlayer): Layer 3 hardware controller.
            parent (QObject, optional): Qt parent for ownership.
        """
        super().__init__(parent)
        self.sound_player = sound_player
        self.is_active = False
        self.current_sounds: List[int] = []
        self.current_volume = 50
        self._sound_catalog = self._build_sound_catalog()
        self._sample_timer = None

    def _build_sound_catalog(self) -> List[Tuple[int, str]]:
        """Scan the sounds directory and build an (id, name) catalog.

        Returns:
            List of (sound_id, sound_name) tuples sorted by id ascending.
        """
        catalog: List[Tuple[int, str]] = []

        if not os.path.isdir(SOUNDS_DIR):
            return catalog

        for fname in os.listdir(SOUNDS_DIR):
            if not fname.lower().endswith(SUPPORTED_EXTENSIONS):
                continue

            name_part = os.path.splitext(fname)[0]
            parts = name_part.rsplit("_", 1)
            try:
                sound_id = int(parts[-1])
            except (ValueError, IndexError):
                continue

            catalog.append((sound_id, name_part))

        catalog.sort(key=lambda x: x[0])
        return catalog

    def get_sounds(self) -> List[Tuple[int, str]]:
        """Return the available sounds in the system.

        Returns:
            List of (sound_id, sound_name) tuples sorted by id ascending.
        """
        return list(self._sound_catalog)

    def set_manual_sound_controller_status(self, on: bool) -> bool:
        """Activate or deactivate the manual sound controller.

        When activated, the sound player is reserved. When deactivated,
        all sounds are stopped and the controller is released.

        Args:
            on (bool): True to activate, False to deactivate.

        Returns:
            bool: True if the operation succeeded.
        """
        if on:
            self.is_active = True
            self.current_sounds = []
            self.current_volume = 50
        else:
            self.is_active = False
            self.sound_player.stop()
            self.current_sounds = []
            self.current_volume = 50

        return True

    def play_sounds(self, sounds: List[int], volume: int) -> bool:
        """Play the specified sounds at the given volume.

        Stops any currently playing sounds first, then plays the new set.
        Called on every update from the UI (sound added/removed, volume changed).

        Args:
            sounds (List[int]): List of sound IDs to play (0–3 items).
            volume (int): Volume level from 0 to 100 in increments of 10.

        Returns:
            bool: True if the operation succeeded, False if inactive,
                too many sounds, or invalid volume.
        """
        if not self.is_active:
            return False

        if len(sounds) > MAX_SIMULTANEOUS_SOUNDS:
            return False

        if volume < 0 or volume > 100 or volume % 10 != 0:
            return False


        # Stop any previous timer
        if self._sample_timer is not None:
            self._sample_timer.stop()
            self._sample_timer.deleteLater()
            self._sample_timer = None

        self.sound_player.stop()

        self.current_sounds = list(sounds)
        self.current_volume = volume

        if not sounds:
            return True

        id_to_file = self._get_id_to_file_map()


        for sound_id in sounds:
            file_path = id_to_file.get(sound_id)
            if file_path is None:
                continue

            sound_config = SoundConfig(
                file_name=file_path,
                duration=0,
                volume=volume,
            )
            self.sound_player.play(sound_config)

        # Start a timer to stop playback after SAMPLE_PLAYBACK_SECONDS
        if sounds:
            self._sample_timer = QTimer(self)
            self._sample_timer.setSingleShot(True)
            self._sample_timer.timeout.connect(self.sound_player.stop)
            self._sample_timer.start(SAMPLE_PLAYBACK_SECONDS * 1000)

        return True

    def _get_id_to_file_map(self) -> dict:
        """Build a mapping of sound_id to file path.

        Prefers .wav files over .mp3 if both exist for the same id.

        Returns:
            dict: {sound_id: absolute_file_path}
        """
        id_to_file: dict = {}

        if not os.path.isdir(SOUNDS_DIR):
            return id_to_file

        for fname in sorted(os.listdir(SOUNDS_DIR)):
            if not fname.lower().endswith(SUPPORTED_EXTENSIONS):
                continue

            name_part = os.path.splitext(fname)[0]
            parts = name_part.rsplit("_", 1)
            try:
                sound_id = int(parts[-1])
            except (ValueError, IndexError):
                continue

            full_path = os.path.join(SOUNDS_DIR, fname)
            if sound_id not in id_to_file or fname.endswith(".wav"):
                id_to_file[sound_id] = full_path

        return id_to_file
