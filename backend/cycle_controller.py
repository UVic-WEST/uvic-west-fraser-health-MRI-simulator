"""Bridge between Layer 2 (backend logic) and Layer 3 (hardware controllers).

CycleController wraps the LightController and SoundPlayer so that the
backend cycle logic can issue high-level commands (start, stop, dispatch
action) without knowing the details of the hardware interface.
"""

from PySide6.QtCore import QObject, Signal
from backend.cycle_action import ActionType


class CycleController(QObject):
    """Hardware abstraction layer for cycle playback.

    Wraps LightController and SoundPlayer from the embedded layer.
    CycleLogic calls start_cycle()/stop_cycle() and listens for
    started/failed signals. During playback, dispatch_action() routes
    individual CycleActions to the appropriate hardware controller.

    Signals:
        started (): Emitted when hardware initialisation succeeds.
        failed (): Emitted when hardware initialisation fails.
    """

    started = Signal()
    failed = Signal()

    def __init__(self, light_controller, sound_player, parent=None):
        """Initialise with references to the Layer 3 hardware controllers.

        Args:
            light_controller (LightController): Controls LED strip brightness.
            sound_player (SoundPlayer): Controls audio playback via aplay/amixer.
            parent (QObject, optional): Qt parent for ownership.
        """
        super().__init__(parent)
        self.light_controller = light_controller
        self.sound_player = sound_player
        self._running = False

    def start_cycle(self):
        """Start the hardware for a cycle (lights to idle, prepare audio)."""
        try:
            self.light_controller.system_idle()
            self._running = True
            self.started.emit()
        except Exception:
            self.failed.emit()

    def stop_cycle(self):
        """Stop all hardware — silence audio and reset lights."""
        self._running = False
        self.sound_player.stop()
        self.light_controller.system_idle()

    def dispatch_action(self, action):
        """Execute a single CycleAction against the hardware layer.

        Called by CycleLogic on each tick for actions whose timestamp
        falls within the current tick window.
        """
        if not self._running:
            return

        action_type = action.action_type
        params = action.parameters

        if action_type == ActionType.SOUND_START:
            from backend.sound_config import SoundConfig
            sound = SoundConfig(
                file_name=params.get("file_name", ""),
                duration=params.get("duration", 0),
                volume=params.get("volume", 50),
            )
            self.sound_player.play(sound)

        elif action_type == ActionType.SOUND_STOP:
            self.sound_player.stop()

        elif action_type == ActionType.LIGHT_ON:
            brightness = params.get("brightness", 0.5)
            self.light_controller.change_lights(brightness)

        elif action_type == ActionType.LIGHT_OFF:
            self.light_controller.system_idle()

        elif action_type == ActionType.LIGHT_RESET:
            self.light_controller.system_idle()

        elif action_type == ActionType.SOUND_RESET:
            self.sound_player.stop()