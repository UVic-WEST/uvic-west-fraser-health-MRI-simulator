class Sound:
    """
    Sound object 
    """
    
    def __init__(self, path: str, duration: float, volume: float):
        self.path = path # sound file path
        self.duration = duration # in seconds
        self.volume = volume # value from 0.0 to 1.0

    def __str__(self) -> str:
        return 'Sound "%s" playing for %f seconds at %f' % (self.path, self.duration, self.volume)