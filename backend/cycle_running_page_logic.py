"""Running-cycle page controller.

Provides a 1-second countdown timer that emits time_signal_in_s for the
frontend TimerWidget, and delegates hardware start/stop to CycleController
on each lifecycle event (start, pause, resume, stop, completion).
"""

from PySide6.QtCore import (
    QTimer,
    Signal,
    QObject
)


class CycleRunningPageLogic(QObject):
    """Backend logic for the cycle-running page.

    Owns a 1-second QTimer for the UI countdown and calls CycleController
    to trigger hardware (lights/sounds) at the appropriate moments.

    Signals:
        time_signal_in_s (int): Remaining seconds (>0), -1 for cancelled,
            0 for completed.
    """

    time_signal_in_s = Signal(int)

    def __init__(self, cycle_controller=None, parent=None):
        """Initialise the running-page logic.

        Args:
            cycle_controller (CycleController, optional): Bridge to hardware.
                If None, the logic still works but skips hardware calls.
            parent (QObject, optional): Qt parent for ownership.
        """
        super().__init__(parent)
        self.parent = parent
        self.cycle_controller = cycle_controller
        self.cur_cycle = None
        self.rem_time_ms = None
        self.timer = None

    def start_cycle(self, cycle_id: int, rem_time_s: int):
        """Start a cycle countdown and activate hardware.

        Args:
            cycle_id (int): Identifier of the cycle to run.
            rem_time_s (int): Cycle duration in seconds.
        """
        self.rem_time_ms = rem_time_s * 1000

        if self.cycle_controller is not None:
            self.cycle_controller.start_cycle()

        if self.timer:
            self.timer.stop()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_timer)
        self.timer.start(1000)

        self.time_signal_in_s.emit(rem_time_s)

    def pause_cycle(self):
        """Pause the countdown timer and stop hardware (lights/sound).

        Returns:
            bool: Always True.
        """
        if self.timer:
            self.timer.stop()

        if self.cycle_controller is not None:
            self.cycle_controller.stop_cycle()

        self.time_signal_in_s.emit(-1)
        return True

    def resume_cycle(self):
        """Resume the countdown and re-activate hardware.

        Does nothing if there is no remaining time.
        """
        if not self.rem_time_ms or self.rem_time_ms <= 0:
            return

        if self.cycle_controller is not None:
            self.cycle_controller.start_cycle()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_timer)
        self.timer.start(1000)

    def stop_cycle(self):
        """Stop the cycle entirely, reset timer, and deactivate hardware."""
        if self.timer:
            self.timer.stop()
            self.timer = None

        if self.cycle_controller is not None:
            self.cycle_controller.stop_cycle()

        self.rem_time_ms = None
        self.time_signal_in_s.emit(-1)

    def _update_timer(self):
        if self.rem_time_ms > 0:
            self.rem_time_ms -= 1000
            self.time_signal_in_s.emit(self.rem_time_ms // 1000)

            if self.rem_time_ms <= 0:
                self._finish_cycle()
        else:
            self._finish_cycle()

    def _finish_cycle(self):
        if self.timer:
            self.timer.stop()
        if self.cycle_controller is not None:
            self.cycle_controller.stop_cycle()
        self.time_signal_in_s.emit(0)