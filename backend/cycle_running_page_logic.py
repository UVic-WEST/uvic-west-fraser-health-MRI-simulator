from PySide6.QtCore import (
    QTimer,
    Signal,
    QObject
)


class CycleRunningPageLogic(QObject):
    """Manages the running-cycle page: countdown timer for the UI and
    delegates hardware actions (lights, sounds) to CycleController."""

    time_signal_in_s = Signal(int)

    def __init__(self, cycle_controller=None, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.cycle_controller = cycle_controller
        self.cur_cycle = None
        self.rem_time_ms = None
        self.timer = None

    def start_cycle(self, cycle_id: int, rem_time_s: int):
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
        if self.timer:
            self.timer.stop()

        if self.cycle_controller is not None:
            self.cycle_controller.stop_cycle()

        self.time_signal_in_s.emit(-1)
        return True

    def resume_cycle(self):
        if not self.rem_time_ms or self.rem_time_ms <= 0:
            return

        if self.cycle_controller is not None:
            self.cycle_controller.start_cycle()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_timer)
        self.timer.start(1000)

    def stop_cycle(self):
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