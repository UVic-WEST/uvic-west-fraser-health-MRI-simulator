from sound import Sound

class SoundPlayer:
    """
    Sound player 

    Communicates directly to the raspberry pi's output audio 
    """
    def __init__(self):
        self.current_sound = None

    def play(self, sound: Sound):
        # start sound playing process
        self.current_sound = sound
        formatted_volume = sound.volume * 100
        return ("Playing sound %s at %d") % (self.current_sound.path, formatted_volume)

    def stop(self):
        # kill sound playing process
        self.current_sound = None
        return "Stopped current sound"


    def incr_volume(self):
        # increment volume
        if not self.current_sound:
            return "No sound is currently playing"
        
        self.current_sound.volume = max(1.0, self.current_sound.volume + 0.1)
        return f"Set volume to {self.current_sound.volume}"


    def decr_volume(self):
        # decrement volume 
        if not self.current_sound:
            return "No sound is currently playing"
        
        self.current_sound.volume = min(0, self.current_sound.volume - 0.1)
        return f"Set volume to {self.current_sound.volume}"