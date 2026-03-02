from dataclasses import dataclass

@dataclass
class SoundConfig: 
    """Stores configuration for a single sound used in a cycle."""
    
    file_name: str
    enabled: bool 
    duration: float # seconds
    volume: float   # 0.0-1.0 (percentage of full volume)
    
    def __post_init__(self):
        """Validate sound config values"""
        
        if not self.file_name:
            raise ValueError("file_name must be a non-empty string")
        
        if self.duration < 0:
            raise ValueError("duration must be between 1 and 100")
        
        if not (0.0 <= self.volume <= 1.0):
            raise ValueError("volume must be between 0.0 and 1.0")
    
    def __repr__(self):
        return (
            f"SoundConfig({self.file_name}, "
            f"enabled={self.enabled}, "
            f"duration={self.duration}, "
            f"volume={self.volume})"
        )
    
