# ======================
# Cycle Initial State
# ======================

def test_initial_state(cycle_logic, app_state):
    # Tests that no cycle is running initially
    assert app_state.get_state() == "IDLE"
    assert cycle_logic.timer == None
    assert cycle_logic.elapsed_ms == 0
    assert cycle_logic.total_duration_sec == 0

# ======================
# Cycle Start Behavior
# ======================

def test_play_calls_lower_layer(cycle_logic, fake_controller):
    """
    Tests that cycle logic passes instruction to lower layer to play a cycle.
    """
    cycle_logic.play()
    assert fake_controller.start_called

def test_no_double_start(cycle_logic, fake_controller):
    """
    Tests that cycle logic does not pass instruction to lower layer to
    play a cycle if one is already running.
    """
    cycle_logic.play()
    assert cycle_logic.controller.start_called

    # force fake controller's start_called to false
    fake_controller.start_called = False

    cycle_logic.play()
    assert not fake_controller.start_called

def test_play_returns_true_on_success(cycle_logic):
    """
    Tests that play() returns True when it successfully issues a start request.
    """
    success = cycle_logic.play()
    assert success

def test_state_not_running_after_control_failed(cycle_logic, app_state, fake_controller):
    """
    Tests that app state is not set to running after receiving signal from lower layer
    that there was a failure when starting the cycle.
    """
    cycle_logic.play()
    fake_controller.failed.emit()
    assert not app_state.get_state() == "RUNNING"
    assert app_state.get_state() == "IDLE"

def test_play_returns_false_after_failure_retry(cycle_logic, fake_controller):
    """
    Tests that after a failure, a second play() still works (not blocked).
    """
    cycle_logic.play()
    fake_controller.failed.emit()
    # After failure, CycleLogic should reset and allow a new play()
    success = cycle_logic.play()
    assert success

def test_cycle_logic_initial_state_after_failure(cycle_logic, fake_controller):
    cycle_logic.start()
    fake_controller.failed.emit()

    # INITIAL STATE
    assert cycle_logic.timer == None
    assert cycle_logic.elapsed_ms == 0
    assert cycle_logic.total_duration_sec == 0

# =======================
# Cycle Running Behaviour
# =======================

CYCLE_DURATION_SEC = 0.1  # 100 ms – keeps tests fast

def test_timer_is_started_after_controller_success(cycle_logic, fake_controller):
    cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
    fake_controller.started.emit()
    assert cycle_logic.timer != None

def test_total_time_is_set_after_start(cycle_logic, fake_controller):
    cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
    fake_controller.started.emit()
    assert cycle_logic.total_duration_sec > 0

def test_running_state_after_controller_started(cycle_logic, fake_controller, app_state):
    """
    Tests that app state is set to running after a successful request to
    play a cycle.
    """
    cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
    # mock start signal from lower layer
    fake_controller.started.emit()
    assert app_state.get_state() == "RUNNING"

def test_timer_advances_time(cycle_logic, fake_controller, qtbot):
    """
    Tests that cycle logic timer progresses.
    """
    cycle_logic.play(duration_sec=1.0)
    fake_controller.started.emit()
    qtbot.wait(250)
    assert cycle_logic.elapsed_ms > 0

def test_cycle_finished_signal_emitted(cycle_logic, fake_controller, qtbot):
    """
    Tests that cycle logic emits cycle_finished signal when a cycle completes.
    """
    with qtbot.waitSignal(cycle_logic.cycle_finished, timeout=1000):
        cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
        fake_controller.started.emit()

def test_idle_state_after_cycle_finishes(cycle_logic, app_state, fake_controller, qtbot):
    """
    Tests app state is set back to IDLE after a cycle finishes running.
    """
    with qtbot.waitSignal(cycle_logic.cycle_finished, timeout=1000):
        cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
        fake_controller.started.emit()
    assert app_state.get_state() == "IDLE"

def test_cycle_logic_resets_after_cycle_finishes(cycle_logic, fake_controller, qtbot):
    """
    Tests that cycle logic goes back to initial state after a cycle finishes running.
    """
    with qtbot.waitSignal(cycle_logic.cycle_finished, timeout=1000):
        cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
        fake_controller.started.emit()

    assert cycle_logic.timer == None
    assert cycle_logic.elapsed_ms == 0
    assert cycle_logic.total_duration_sec == 0

# ======================
# Cycle Stop Behaviour
# ======================
def test_stop_calls_lower_layer(cycle_logic, fake_controller):
    """
    Tests that cycle logic transmits instruction to stop cycle to the lower layer
    upon receiving call to stop().
    """
    cycle_logic.stop()
    assert fake_controller.stop_called

def test_idle_state_after_stop(cycle_logic, app_state):
    """
    Tests that app state is set back to IDLE after stop.
    """
    cycle_logic.stop()
    assert app_state.get_state() == "IDLE"

def test_cycle_logic_resets_after_stop(cycle_logic, fake_controller):
    """
    Tests that cycle returns to initial state after receiving call to stop().
    """
    cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
    fake_controller.started.emit()
    cycle_logic.stop()

    # Initial state
    assert cycle_logic.timer == None
    assert cycle_logic.elapsed_ms == 0
    assert cycle_logic.total_duration_sec == 0

# ======================
# Signal emissions
# ======================
def test_progress_changed_emitted(cycle_logic, fake_controller, qtbot):
    """
    Tests that progress_changed signal is emitted while the cycle runs.
    """
    with qtbot.waitSignal(cycle_logic.progress_changed, timeout=1000):
        cycle_logic.play(duration_sec=1.0)
        fake_controller.started.emit()

def test_time_changed_emitted(cycle_logic, fake_controller, qtbot):
    """
    Tests that time_changed signal is emitted while the cycle runs.
    """
    with qtbot.waitSignal(cycle_logic.time_changed, timeout=1000):
        cycle_logic.play(duration_sec=1.0)
        fake_controller.started.emit()
