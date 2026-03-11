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
# Signal emissions ? might be needed for UI layer , not neceaasry i guess
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

# ======================
# Cycle Pause Behaviour
# ======================
def test_pause_calls_lower_layer(cycle_logic, fake_controller):
    """
    Tests that cycle logic sends instruction to lower layer.

    TODO: I am assuming lower layer does not have a separate PAUSE function
    """
    cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
    fake_controller.started.emit()

    cycle_logic.pause()
    assert fake_controller.stop_called

def test_pause_stops_timer_progress(cycle_logic, fake_controller, qtbot):
    """
    Tests that timer stops progressing after pause has been called.
    """
    cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
    fake_controller.started.emit()

    cycle_logic.pause()
    time_elapsed = cycle_logic.elapsed_ms

    qtbot.wait(100)

    # Elapsed time has not increased if cycle has not been resumed
    assert cycle_logic.elapsed_ms == time_elapsed

def test_pause_sets_paused_state(cycle_logic, fake_controller, app_state):
    """
    Tests that the application state is set to PAUSED.
    """
    cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
    fake_controller.started.emit()

    cycle_logic.pause()
    assert app_state.get_state() == "PAUSED"

def test_pause_does_not_reset(cycle_logic, fake_controller):
    """
    Tests that cycle logic's internal state is not reset when paused.
    """
    cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
    fake_controller.started.emit()

    cycle_logic.pause()
    assert not cycle_logic.timer == None
    assert not cycle_logic.elapsed_ms == 0
    assert not cycle_logic.total_duration_sec == 0

# ======================
# Cycle Resume Behaviour
# ======================
def test_cannot_resume_running_cycle(cycle_logic, fake_controller):
    """
    Tests that cycle must be in PAUSED state in order to be resumed.

    TODO: I am assuming lower layer won't have a separate function for resume, and layer
    2 will simply call layer 3's start with updated values?
    """
    cycle_logic.play()
    assert fake_controller.start_called

    # force fake controller start_called to be false
    fake_controller.start_called = False

    cycle_logic.resume()
    assert not fake_controller.start_called

def test_resume_calls_lower_layer(cycle_logic, fake_controller):
    """
    Tests that cycle logic passes instruction to lower layer.
    """
    cycle_logic.play()
    cycle_logic.pause()

    cycle_logic.resume()

    assert fake_controller.start_called

def test_resume_returns_true_on_success(cycle_logic):
    """
    Tests that resume() returns True when it successfully issues a resume request.
    """
    success = cycle_logic.resume()
    assert success

def test_state_paused_after_control_failed(cycle_logic, app_state, fake_controller):
    """
    Tests that app state is not set to running after receiving signal from lower layer
    that there was a failure when resuming the cycle.
    """
    cycle_logic.play(duration_sec=1.0)
    cycle_logic.pause()
    cycle_logic.resume()
    fake_controller.failed.emit()
    assert not app_state.get_state() == "RUNNING"
    assert app_state.get_state() == "PAUSED"

def test_cycle_logic_maintains_state_after_failure(cycle_logic, fake_controller):
    """
    Tests that cycle logic maintain its previous internal state after a failure (i.e., info related to the cycle
    currently running)

    TODO: do we want to maintain state after a failure, and allow for retries, or should we reset upon a failure.
    """
    cycle_logic.start()
    cycle_logic.pause()

    paused_timer = cycle_logic.timer
    paused_elapsed_ms = cycle_logic.elapsed_ms
    paused_total_duration_sec = cycle_logic.total_duration_sec

    cycle_logic.resume()
    fake_controller.failed.emit()

    # PAUSED STATE
    assert cycle_logic.timer == paused_timer
    assert cycle_logic.elapsed_ms == paused_elapsed_ms
    assert cycle_logic.total_duration_sec == paused_total_duration_sec

def test_resume_resumes_timer_progression(cycle_logic, fake_controller, qtbot):
    """
    Tests that timer continues progressing after the running cycle has been resumed.
    """
    # play and pause
    cycle_logic.play(duration_sec=1.0)
    fake_controller.started.emit()

    qtbot.wait(100)
    cycle_logic.pause()

    # get time elapsed so far
    elapsed_after_pause = cycle_logic.elapsed_ms

    # resume
    cycle_logic.resume()
    fake_controller.started.emit()
    qtbot.wait(100)

    # assert elapsed time has changed
    assert cycle_logic.elapsed_ms > elapsed_after_pause

def test_resume_sets_running_state(cycle_logic, fake_controller, app_state):
    """
    Tests that the application state is set back to running after a successful resume request.
    """
    cycle_logic.play(duration_sec=1.0)
    fake_controller.started.emit()

    assert app_state.get_state() == "RUNNING"

def test_resume_finishes_after_resume(cycle_logic, fake_controller, qtbot):
    """
    Tests that cycle finishes after being resumed.
    """
    # play and pause
    cycle_logic.play(duration_sec=1.0)
    fake_controller.started.emit()

    qtbot.wait(100)
    cycle_logic.pause()

    # resume
    with qtbot.waitSignal(cycle_logic.cycle_finished, timeout=1000):
        cycle_logic.resume()
        fake_controller.started.emit()

    assert cycle_logic.timer == None
    assert cycle_logic.elapsed_ms == 0
    assert cycle_logic.total_duration_sec == 0

def test_pause_resume_multiple_times(cycle_logic, fake_controller, app_state):
    """
    Tests that a cycle can be paused and resumed more than once.
    """
    cycle_logic.play(duration_sec=CYCLE_DURATION_SEC)
    fake_controller.started.emit()

    for _ in range(3):
        # pause
        cycle_logic.pause()
        assert app_state.get_state() == "PAUSED"

        # resume
        cycle_logic.resume()
        fake_controller.started.emit()
        assert app_state.get_state() == "RUNNING"

def test_pause_resume_state_transition(cycle_logic, fake_controller, app_state):
    """
    Tests that the application state transitions correctly from
    RUNNING -> PAUSED -> RUNNING when pause and resume are called.
    """
    cycle_logic.play(duration_sec=1.0)
    fake_controller.started.emit()

    # Cycle should now be running
    assert app_state.get_state() == "RUNNING"

    # Pause the cycle
    cycle_logic.pause()
    assert app_state.get_state() == "PAUSED"

    # Resume the cycle
    cycle_logic.resume()
    fake_controller.started.emit()

    assert app_state.get_state() == "RUNNING"

    def test_stop_during_paused_state(cycle_logic, fake_controller, app_state):
    """
    Tests that calling stop() while the cycle is paused resets the cycle
    and returns the application state to IDLE.
    """
    cycle_logic.play(duration_sec=1.0)
    fake_controller.started.emit()

    # Pause the cycle
    cycle_logic.pause()
    assert app_state.get_state() == "PAUSED"

    # Stop the cycle
    cycle_logic.stop()

    # State should return to IDLE
    assert app_state.get_state() == "IDLE"

    # Cycle logic should reset to initial state
    assert cycle_logic.timer is None
    assert cycle_logic.elapsed_ms == 0
    assert cycle_logic.total_duration_sec == 0