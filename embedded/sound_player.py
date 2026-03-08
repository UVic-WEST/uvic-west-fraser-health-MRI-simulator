import subprocess 
from backend.sound_config import SoundConfig

class SoundPlayer:
    """
    Handles sound playback requests.

    This class will eventually communicate with the Raspberry Pi OS
    audio system (Layer 2). For now, those calls are stubbed.
    """

    def __init__(self):
        self.current_sound = None # Currently playing sound 
        self.current_volume = 0 # Session-specific sound volume 

    def play(self, sound: SoundConfig) -> str:
        """
            Play a sound using the configuration provided.

            Stub for Layer 2 communication.
            **Untested** hardware implementation
        """
        self.current_sound = sound
        self.current_volume = sound.volume

        try:
            subprocess.run(["amixer", "sset", "PCM,0", f"{self.current_volume}%"], check=True, capture_output=True)
            subprocess.run(["aplay", self.current_sound.file_name], check=True, capture_output=True)

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else e
            return f"Failed to play sound, error: {error_msg}"

        return f"Playing sound {self.current_sound.file_name} at {self.current_volume}%"

    def stop(self) -> str:
        """
            Stops all sound playing (aplay) processes.
        
            Stub for Layer 2 communication.
            **Untested** hardware implementation
        """
        self.current_sound = None
        
        try:
            subprocess.run(["killall", "aplay"], check=True, capture_output=True)

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else e
            return f"Failed to stop sound, error: {error_msg}"
            
        return "Stopped current sound"


    def incr_volume(self) -> str:
        """
            Increment volume of currently playing sound by 10%
        
            Stub for Layer 2 communication.
            **Untested** hardware implementation
        """
        if not self.current_sound:
            return "No sound is currently playing"
        
        self.current_volume = min(100, self.current_volume + 10)

        try:
            subprocess.run(["amixer", "sset", "PCM,0", f"{self.current_volume}%"], check=True, capture_output=True)
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else e
            return f"Failed to increment sound, error: {error_msg}"
        
        return f"Set volume to {self.current_volume}%"


    def decr_volume(self) -> str:
        """
            Decrement volume of currently playing sound by 10%
        
            Stub for Layer 2 communication.
            **Untested** hardware implementation
        """
        if not self.current_sound:
            return "No sound is currently playing"
        
        self.current_volume = max(0, self.current_volume - 10)
        
        try:
            subprocess.run(["amixer", "sset", "PCM,0", f"{self.current_volume}%"], check=True, capture_output=True)
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else e
            return f"Failed to decrement sound, error: {error_msg}"
        

        return f"Set volume to {self.current_volume}%"