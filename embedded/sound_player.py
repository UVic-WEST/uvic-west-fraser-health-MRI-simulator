import pygame.mixer
from backend.sound_config import SoundConfig

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()
pygame.mixer.set_num_channels(3)

class SoundPlayer:
    """
    Handles sound playback requests using pygame.mixer

    Communicates directly with Raspberry Pi audio output to drive 
    speaker playback. Supports up to 3 simultaneous looping sounds
    which play indefinitely until stop() is called
    """

    def __init__(self):
        self.current_volume = 50

    def play(self, sound: SoundConfig) -> tuple:
        """Play a sound using the configuration provided."""
        try:
            pygame_sound = pygame.mixer.Sound(sound.file_name)
            pygame_sound.set_volume(sound.volume / 100.0)

            channel = pygame.mixer.find_channel()
            if channel is None:
                return False, "No free channels available"

            channel.play(pygame_sound, loops=-1)

        except (FileNotFoundError, pygame.error) as e:
            return False, f"Failed to play sound, error: {str(e)}"

        return True, f"Playing sound {sound.file_name} at {sound.volume}%"

    def stop(self) -> str:
        """Stop all currently sound playing processes"""
        pygame.mixer.stop()
        return "Stopped all sounds"

    def incr_volume(self) -> str:
        """Increment volume of currently playing sounds by 10%."""
        if not pygame.mixer.get_busy():
            return "No sound is currently playing"

        self.current_volume = min(100, self.current_volume + 10)
        for i in range(pygame.mixer.get_num_channels()):
            channel = pygame.mixer.Channel(i)
            if channel.get_busy():
                channel.set_volume(self.current_volume / 100.0)

        return f"Set volume to {self.current_volume}%"

    def decr_volume(self) -> str:
        """Decrement volume of currently playing sounds by 10%."""
        if not pygame.mixer.get_busy():
            return "No sound is currently playing"

        self.current_volume = max(0, self.current_volume - 10)
        for i in range(pygame.mixer.get_num_channels()):
            channel = pygame.mixer.Channel(i)
            if channel.get_busy():
                channel.set_volume(self.current_volume / 100.0)

        return f"Set volume to {self.current_volume}%"


if __name__ == "__main__": # Use for isolated hardware testing
    player = SoundPlayer()

    file_name = input("Enter sound file path: ").strip()
    volume = int(input("Enter volume (0-100): ").strip())

    sound = SoundConfig(file_name=file_name, sound_id=10, duration=10.0, volume=volume)
    success, message = player.play(sound)
    print(message)

    print("Commands: + (incr volume), - (decr volume), s (stop), q (quit)")
    try:
        while True:
            cmd = input("> ").strip()
            if cmd == "+":
                print(player.incr_volume())
            elif cmd == "-":
                print(player.decr_volume())
            elif cmd == "s":
                print(player.stop())
            elif cmd == "q":
                player.stop()
                break
            else:
                print("Unknown command")
    except KeyboardInterrupt:
        print("\nInterrupted, stopping sounds...")
        player.stop()