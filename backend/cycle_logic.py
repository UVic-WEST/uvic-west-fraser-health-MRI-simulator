from PySide6.QtCore import QObject, Signal, QTimer
from backend.cycle_factory import CycleFactory
from backend.cycle_config import CycleConfig


TICK_INTERVAL_MS = 100


class CycleLogic(QObject):
    """ Manages the simulation timeline: tracks elapsed time against total
    duration and emits signals so the UI layer can update progress, remaining
    time, and cycle-finished state. """

    progress_changed = Signal(float)
    time_changed = Signal(int)
    cycle_finished = Signal()
    resumed = Signal()
    paused = Signal()

    def __init__(self, app_state, controller):
        super().__init__()
        self.app_state = app_state
        self.controller = controller
        self.cycle_factory = CycleFactory()

        self.current_cycle: CycleConfig | None = None  # loaded cycle
        self.timer = None
        self.elapsed_ms = 0
        self.total_duration_sec = 0
        self._pending = False
        self._cycle_config = None
        self._last_action_check_ms = 0

        self.controller.started.connect(self._on_started)
        self.controller.failed.connect(self._on_failed)

    def load_cycle_by_id(self, cycle_id: str):
        """ Load a predefined cycle from the factory by its ID """
        self.current_cycle = self.cycle_factory.get_cycle_by_id(cycle_id)
        self.total_duration_sec = self.current_cycle.cycle_duration_sec
        self.elapsed_ms = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def play(self, duration_sec=0, cycle_config=None):
        """Request the lower-layer controller to start a cycle.
        Returns True if the request was issued, False if a cycle is already
        active or pending.

        Args:
            duration_sec: cycle duration (used if cycle_config is not provided)
            cycle_config: optional CycleConfig with timestamped actions
        """
        if self.app_state.get_state() == "RUNNING" or self._pending:
            return False

        self._pending = True
        self._cycle_config = cycle_config
        self._last_action_check_ms = 0

        if cycle_config is not None:
            self.total_duration_sec = cycle_config.cycle_duration_sec
        else:
            self.total_duration_sec = duration_sec

        self.controller.start_cycle()
        return True

    def start(self, duration_sec=0):
        """ alias for play() """
        return self.play(duration_sec)

    def stop(self):
        """ stop the running cycle, tell the lower layer, and reset """
        self.controller.stop_cycle()
        self._reset()
        self.app_state.set_state("IDLE")

    def pause(self):
        """ pause the running cycle """
        if self.app_state.get_state() != "RUNNING":
            return
        
        if self.timer is not None:
            self.timer.stop()
            
        self.controller.stop_cycle()
        self.app_state.set_state("PAUSED")
        self.paused.emit()

    def resume(self):
        """ resume a paused cycle without restarting it """
        if self.app_state.get_state() != "PAUSED":
            return False

        self._pending = True
        self.controller.start_cycle() # lower layer resumes (audio/light)
        return True
    
    # ------------------------------------------------------------------
    # Controller signal handlers
    # ------------------------------------------------------------------

    def _on_started(self):
        self._pending = False
        
        if self.app_state.get_state() == "PAUSED":
            self.resumed.emit()
            
        self.app_state.set_state("RUNNING")
        self._start_timer()

    def _on_failed(self):
        self._pending = False
        if self.app_state.get_state() == "RUNNING":
            self._reset()
            self.app_state.set_state("IDLE")

    # ------------------------------------------------------------------
    # Timer internals
    # ------------------------------------------------------------------

    def _start_timer(self):
        if self.timer is None:
            self.timer = QTimer(self)
            self.timer.setInterval(TICK_INTERVAL_MS)
            self.timer.timeout.connect(self._tick)
        
        self.timer.start()
        
        if self.elapsed_ms == 0:
            self._tick()

    def _tick(self):
        self.elapsed_ms += TICK_INTERVAL_MS
        total_ms = int(self.total_duration_sec * 1000)

        # emit progress for UI
        progress = min(self.elapsed_ms / total_ms, 1.0) if total_ms > 0 else 0.0
        self.progress_changed.emit(progress)
        self.time_changed.emit(self.elapsed_ms)
        
        # execute actions whose time has come
        if self.current_cycle:
            for action in self.current_cycle.actions:
                if action.is_execution_time(self.elapsed_ms, self.elapsed_ms - TICK_INTERVAL_MS):
                    self.controller.execute_action(action)
        
        # complete cycle if done
        if total_ms > 0 and self.elapsed_ms >= total_ms:
            self._complete()

    def _dispatch_actions(self):
        """Check for CycleActions due in the current tick window and dispatch them."""
        if self._cycle_config is None:
            return
        if not hasattr(self.controller, 'dispatch_action'):
            return

        actions = self._cycle_config.get_actions_at(
            self.elapsed_ms, window_ms=TICK_INTERVAL_MS
        )
        for action in actions:
            if action.is_execution_time(self.elapsed_ms, self._last_action_check_ms):
                self.controller.dispatch_action(action)

        self._last_action_check_ms = self.elapsed_ms

    def _complete(self):
        self.cycle_finished.emit()
        self._reset()
        self.app_state.set_state("IDLE")

    def _reset(self):
        if self.timer is not None:
            self.timer.stop()
        self.timer = None
        self.elapsed_ms = 0
        self.total_duration_sec = 0
        self._pending = False
        self._cycle_config = None
        self._last_action_check_ms = 0