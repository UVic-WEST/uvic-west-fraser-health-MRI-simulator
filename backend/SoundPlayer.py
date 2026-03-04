from backend.sound_config import SoundConfig


class SoundPlayer:
    """
    Handles sound playback requests.

    This class will eventually communicate with the Raspberry Pi OS
    audio system (Layer 2). For now, those calls are stubbed.
    """

    def __init__(self):
        self.current_sound: SoundConfig | None = None
        self.current_volume: float = 1.0

    def play(self, sound: SoundConfig):
        """
        Play a sound using the configuration provided.
        Stub for Layer 2 communication.
        """
        self.current_sound = sound

        # STUB: send play command to Raspberry Pi audio system
        print(f"[STUB] Playing {sound.file_name} at volume {sound.volume}")

    def pause(self):
        """
        Pause current sound.
        Stub for Layer 2 communication.
        """
        # STUB
        print("[STUB] Pausing sound")

    def stop(self):
        """
        Stop current sound.
        Stub for Layer 2 communication.
        """
        # STUB
        print("[STUB] Stopping sound")

    def set_volume(self, volume: float):
        """
        Change playback volume.
        Stub for Layer 2 communication.
        """
        if not (0.0 <= volume <= 1.0):
            raise ValueError("volume must be between 0.0 and 1.0")

        self.current_volume = volume

        # STUB
        print(f"[STUB] Setting volume to {volume}")