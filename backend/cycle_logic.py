from PySide6.QtCore import QObject, Signal, QTimer

TICK_INTERVAL_MS = 100


class CycleLogic(QObject):
    """Manages the simulation timeline: tracks elapsed time against total
    duration and emits signals so the UI layer can update progress, remaining
    time, and cycle-finished state."""

    progress_changed = Signal(float)
    time_changed = Signal(int)
    cycle_finished = Signal()
    resumed = Signal()

    def __init__(self, app_state, controller):
        super().__init__()
        self.app_state = app_state
        super().__init__()
        self.app_state = app_state
        self.controller = controller

        self.timer = None
        self.elapsed_ms = 0
        self.total_duration_sec = 0
        self._pending = False

        self.controller.started.connect(self._on_started)
        self.controller.failed.connect(self._on_failed)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def play(self, duration_sec=0):
        """Request the lower-layer controller to start a cycle.
        Returns True if the request was issued, False if a cycle is already
        active or pending."""
        if self.app_state.get_state() == "RUNNING" or self._pending:
            return False

        self._pending = True
        self.total_duration_sec = duration_sec
        self.controller.start_cycle()
        return True

    def start(self, duration_sec=0):
        """Alias for play()."""
        return self.play(duration_sec)

    def stop(self):
        """Stop the running cycle, tell the lower layer, and reset."""
        self.controller.stop_cycle()
        self._reset()
        self.app_state.set_state("IDLE")

    def pause(self):
        """Pause the running cycle. Stops the timer but preserves elapsed
        time and duration so the cycle can be resumed."""
        if self.timer is not None:
            self.timer.stop()
        self.controller.stop_cycle()
        self.app_state.set_state("PAUSED")

    def resume(self):
        """Resume a paused cycle without restarting it."""
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

        progress = min(self.elapsed_ms / total_ms, 1.0) if total_ms > 0 else 0.0
        self.progress_changed.emit(progress)
        self.time_changed.emit(self.elapsed_ms)

        if total_ms > 0 and self.elapsed_ms >= total_ms:
            self._complete()

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
