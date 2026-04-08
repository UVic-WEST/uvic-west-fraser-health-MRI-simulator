"""Running-cycle page controller.

Provides a 1-second countdown timer that emits time_signal_in_s for the
frontend TimerWidget, and delegates hardware start/stop to the embedded
controllers on each lifecycle event (start, pause, resume, stop, completion).
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import (
    QTimer,
    Signal,
    QObject
)
from backend.cycle_factory import CycleFactory
from backend.cycle_action import ActionType
from backend.sound_config import SoundConfig
from embedded.sound_player import SoundPlayer
from embedded.light_controller import LightController

class CycleRunningPageLogic(QObject):
    """Backend logic for the cycle-running page.

    Owns a 1-second QTimer for the UI countdown and calls CycleController
    to trigger hardware (lights/sounds) at the appropriate moments.

    Signals:
        time_signal_in_s (int): Remaining seconds (>0), -1 for cancelled,
            0 for completed.
        cycle_start_failed (str): Emitted when ``cycle_id`` is unknown or load fails;
            message is safe to show to the user.
    """

    time_signal_in_s = Signal(int)
    error_signal = Signal(bool)
    cycle_start_failed = Signal(str)

    def __init__(
        self,
        sound_player: SoundPlayer,
        light_controller: LightController,
        parent=None,
        cycle_factory: Optional[CycleFactory] = None,
    ):
        """
        This function initializes the CycleRunningPageLogic class, which contains the main logic
        for running cycles. This class is in charge of receiving requests from the frontend and forwarding
        the corresponding instructions to the hardware layer.

        Args:
            sound_player(SoundPlayer): lower-layer sound controller
            light_controller(LightController): lower-layer light controller
            parent (QObject, optional): Qt parent for ownership.
            cycle_factory (CycleFactory, optional): shared factory; default is a new ``CycleFactory``.

        Returns:
            None
        """
        super().__init__(parent)
        self.parent = parent

        # lower layer controllers
        self.sound_player = sound_player
        self.light_controller = light_controller
        self.cycle_factory = cycle_factory or CycleFactory()

        # internal state
        self.current_cycle = None
        self.rem_time_ms = 0
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._update_timer)
        self._last_emitted_s = None

    @property
    def _ms_elapsed(self):
        """Number of ms elapsed in the current cycle"""
        if (self.current_cycle):
            return self.current_cycle.cycle_duration_ms - self.rem_time_ms
        else:
            return 0

    @property
    def _rem_time_in_sec(self):
        """Number of seconds elapsed in the current cycle."""
        return self.rem_time_ms // 1000

    @property
    def _active_cycle(self):
        """Whether there class has a cycle."""
        return self.current_cycle != None
    
    @property
    def _active_timer(self):
        """Whether the class timer is currently active."""
        return self.timer.isActive()

    #### Public API ####
    def start_cycle(self, cycle_id: int):
        """
        This function
        - Gets the cycle configuration based on the cycle_id passed
        - Passes corresponding instructions to SoundPlayer and LightController
        - Starts a timer for the current cycle

        Args:
            cycle_id (int): the id of the cycle to find the configuration of

        Returns:
            None
        """
        if self._active_cycle:
            return

        try:
            self.current_cycle = self.cycle_factory.get_cycle_by_id(cycle_id=cycle_id)
        except ValueError as e:
            self.cycle_start_failed.emit(str(e))
            return

        self.rem_time_ms = self.current_cycle.cycle_duration_ms

        print("Starting cycle with duration", self.rem_time_ms)
        self._set_light_intensity()
        self.time_signal_in_s.emit(self._rem_time_in_sec)
        self.timer.start()

    def pause_cycle(self):
        """This function pauses the current cycle. It stops the timer and signals to lower layer that the
        cycle should be stopped, but does not reset internal state."""
        if not self._active_timer:
            return
    
        self.timer.stop()
        self._lower_layer_stop_cycle()

    def resume_cycle(self):
        """This functions resumes the current cycle."""
        if self._active_timer:
            return
        
        self._set_light_intensity()
        self.timer.start()

    def stop_cycle(self):
        """This function stops the current cycle."""
        if not self._active_cycle:
            return
        
        print("Stoping cycle...")
        self._finish_cycle()

    ### END PUBLIC API ###

    def _update_timer(self):
        """
        This function handles the timer logic within the class; it is called by the timer each 100ms.
        Updates internal timing variables and communicates each ellapsed second to the upper layer.

        Triggers _finish_cycle() when remaining time reaches 0.
        """
        if self.rem_time_ms > 0:
            self._dispatch_actions()
            self.rem_time_ms -= 100

            if self._rem_time_in_sec != self._last_emitted_s:
                self.time_signal_in_s.emit(self._rem_time_in_sec)
                self._last_emitted_s = self._rem_time_in_sec
        
        if self.rem_time_ms <= 0:
            self._finish_cycle()

    def _finish_cycle(self):
        """
        This function is called when the total time for the current cycle elapses.
        It emits signal that cycle has finished, forwards instructions to the lower layer, and resets internal state.
        """
        self.time_signal_in_s.emit(0)
        self._lower_layer_stop_cycle()
        self._reset()
        
    def _dispatch_actions(self):
        """
        This function determines which actions should be dispatched at a given moment.
        Communicates each action that should be dispatched within the current window to the lower layer controllers.
        """
        actions_to_dispatch = self.current_cycle.get_actions_at(self._ms_elapsed)
        for action in actions_to_dispatch: self._lower_layer_dispatch_sounds(action)
    
    def _reset(self):
        """
        This functions resets internal state when there is no active cycle.
        """
        self.current_cycle = None
        
        print("stopping timer...")
        self.timer.stop()

        self.rem_time_ms = 0

    #### lower layer communication functions ###

    def _set_light_intensity(self):
        """
        Passes instruction to lower-layer light controller to set the light brightness to the level specified
        by the cycle configuration. ``light_configuration`` is 0–100; ``LightController`` expects 0.0–1.0.
        """
        if not self.current_cycle.lights_on:
            self.light_controller.system_off()
            return
        brightness = self.current_cycle.light_configuration / 100.0
        self.light_controller.change_lights(brightness)

    def _lower_layer_stop_cycle(self):
        """Ensures that lights are set back to idle and sound stops."""
        self.light_controller.system_idle()
        self.sound_player.stop()

    def _lower_layer_dispatch_sounds(self, action):
        """Execute a single CycleAction against the hardware layer.

        Called by CycleLogic on each tick for actions whose timestamp
        falls within the current tick window.
        """
        if not self._active_cycle:
            return
        
        print("Dispatching action", action)
        
        action_type = action.action_type
        params = action.parameters

        if action_type == ActionType.SOUND_START:
            duration_sec = params.get("duration")
            if duration_sec is None and "duration_ms" in params:
                duration_sec = float(params["duration_ms"]) / 1000.0
            if duration_sec is None:
                duration_sec = 0.0
            sid = params.get("sound_id", 1)
            sound = SoundConfig(
                sound_id=int(sid) if sid is not None else 1,
                file_name=params.get("file_name", ""),
                duration=float(duration_sec),
                volume=params.get("volume", 50),
            )
            success, err_msg = self.sound_player.play(sound)

            if not success:
                print("Sound play failed :((((((  (cycle continues):", err_msg)
                self.error_signal.emit(True)

        elif action_type == ActionType.SOUND_STOP or action_type == ActionType.SOUND_RESET:
            self.sound_player.stop()