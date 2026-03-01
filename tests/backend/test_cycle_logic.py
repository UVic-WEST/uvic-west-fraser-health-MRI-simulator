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

def test_send_emit_cycle_started_signal(cycle_logic, fake_controller):
    """
    Tests that cycle logic passes success response to UI layer upon receiving signal
    from lower layer that cycle was started.
    """
    success = cycle_logic.play()
    fake_controller.started.emit()
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

def test_not_emit_cycle_signal_after_failure(cycle_logic, fake_controller):
    """
    Tests that cycle logic sends 'false' response to UI layer after receiving signal from
    lower layer that there was a failure when starting the cycle.
    """
    success = cycle_logic.play()
    fake_controller.failed.emit()
    assert not success

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

def test_timer_is_started_after_controller_success(cycle_logic, fake_controller):
    cycle_logic.play()
    fake_controller.started.emit()
    assert cycle_logic.timer != None
    # TODO: check if an assertion like this exists
    # assert cycle_logic.start_timer().is_called

def test_total_time_is_set_after_start(cycle_logic, fake_controller):
    cycle_logic.play()
    fake_controller.started.emit()
    assert cycle_logic.total_duration_sec > 0

def test_running_state_after_controller_started(cycle_logic, fake_controller, app_state):
    """
    Tests that app state is set to running after a successful request to
    play a cycle.
    """
    cycle_logic.play()
    # mock start signal from lower layer
    fake_controller.started.emit()
    assert app_state.get_state() == "RUNNING"

def test_timer_advances_time(cycle_logic, qtbot):
    """
    Tests that cycle logic timer progresses.
    """
    cycle_logic.play()
    qtbot.wait(150)
    assert cycle_logic.elapsed_ms > 0

def test_cycle_finished_signal_emitted(cycle_logic, qtbot):
    """
    Tests that cycle logic emits signal to UI that a cycle has finished running.
    """
    # notifies UI layer when cycle has finished running
    cycle_logic.play()
    # mock time passing
    qtbot.wait(150)
    assert cycle_logic.stop_signal.emitted()

def test_idle_state_after_cycle_finishes(cycle_logic, app_state, qtbot):
    """
    Tests app state is set back to IDLE after a cycle finishes running.
    """
    cycle_logic.play()
    # mock time passing
    qtbot.wait(150)
    assert app_state.get_state() == "IDLE"

def test_cycle_logic_resets_after_cycle_finishes(cycle_logic):
    """
    Tests that cycle logic goes back to initial state after a cycle finishes running.
    """
    cycle_logic.play()

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

def test_cycle_logic_resets_after_stop(cycle_logic):
    """
    Tests that cycle returns to initial state after receiving call to stop().
    """
    cycle_logic.play()
    cycle_logic.stop()

    # Initial state
    assert cycle_logic.timer == None
    assert cycle_logic.elapsed_ms == 0
    assert cycle_logic.total_duration_sec == 0