from unittest.mock import patch

from backend.cycle_action import CycleAction, ActionType
from backend.cycle_config import CycleConfig
from backend.sound_config import SoundConfig

#### start cycle behavior ###
def test_double_start():
    pass

def test_sound_player_failure(cycle_running_logic, mock_sound_player):
    """Playback failure does not abort the cycle (timer keeps running)."""
    mock_sound_player.play.return_value = (False, "Error")

    with patch.object(cycle_running_logic, "cycle_factory") as mock:
        mock.get_cycle_by_id.return_value = CycleConfig(1, "test cycle", 3000, 70, actions=[
            CycleAction(0, ActionType.SOUND_START, {"file_name": "test", "duration": 3000, "volume": 50}),
        ])

        cycle_running_logic.start_cycle(1)
        cycle_running_logic._update_timer()

    assert cycle_running_logic._active_cycle
    assert cycle_running_logic._active_timer

def test_light_controller_failure():
    """Current implementation never seems to indicate failure?"""
    pass

def test_active_cycle_on_success(cycle_running_logic):
    """Tests there is an active cycle when both SoundPlayer.play and LightController.change_lights are successful"""
    cycle_running_logic.start_cycle(1)
    assert cycle_running_logic._active_cycle
    assert cycle_running_logic.current_cycle != None

def test_active_timer_on_success(cycle_running_logic):
    """Tests timer is active on success"""
    cycle_running_logic.start_cycle(1)
    assert cycle_running_logic._active_timer

def test_sets_timer_on_success(cycle_running_logic):
    """Tests that timer is set with cycle configuration value"""
    cycle_running_logic.start_cycle(1)
    cycle_running_logic.timer.start.assert_called_once()

### full cycle and timer behavior ###
def test_timer_decrements_time(cycle_running_logic, qtbot, mock_cycle_factory):
    """Tests that timer updates"""
    cycle_running_logic.current_cycle = mock_cycle_factory.get_cycle_by_id(1)
    cycle_running_logic.rem_time_ms = 3000
    with qtbot.waitSignal(cycle_running_logic.time_signal_in_s, timeout=1000) as blocker:
        cycle_running_logic._update_timer()
    
    # Assert that the signal was emitted with the expected value
    assert blocker.args == [2] # If rem_time_ms went from 3000 to 2000
    assert cycle_running_logic.rem_time_ms < 3000

def test_cycle_stops_at_zero(cycle_running_logic, qtbot, mock_cycle_factory):
    """"""
    cycle_running_logic.current_cycle = mock_cycle_factory.get_cycle_by_id(1)
    cycle_running_logic.rem_time_ms = 100
    with qtbot.waitSignal(cycle_running_logic.time_signal_in_s, timeout=2000) as blocker:
        cycle_running_logic._update_timer()
    
    # Assert that the signal was emitted with 0ms
    assert blocker.args == [0]
    assert cycle_running_logic.rem_time_ms == 0
    cycle_running_logic.timer.stop.assert_called_once()

def test_passes_single_light_action(cycle_running_logic):
    cycle_running_logic.start_cycle(1)
    cycle_running_logic._update_timer()
    cycle_running_logic.light_controller.change_lights.assert_called_once_with(0.7)

def test_passes_single_sound_action(cycle_running_logic):
    with patch.object(cycle_running_logic, "cycle_factory") as mock:
        sound_config = {"sound_id": 1, "file_name": "test", "duration": 1000, "volume": 50}
        mock.get_cycle_by_id.return_value = CycleConfig(1, "test cycle", 3000, 70, actions=[
            CycleAction(0, ActionType.SOUND_START, sound_config)
        ])
        cycle_running_logic.start_cycle(1)
        cycle_running_logic._update_timer()
    cycle_running_logic.sound_player.play.assert_called_once_with(SoundConfig("test", 1, 1000, 50))

def test_stops_sound_action(cycle_running_logic):
    with patch.object(cycle_running_logic, "cycle_factory") as mock:
        sound_config = {"file_name": "test", "duration": 1000, "volume": 50}
        mock.get_cycle_by_id.return_value = CycleConfig(1, "test cycle", 3000, 70, actions=[
            CycleAction(0, ActionType.SOUND_START, sound_config),
            CycleAction(100, ActionType.SOUND_STOP, {}),
        ])
        cycle_running_logic.start_cycle(1)

        cycle_running_logic._update_timer()
        cycle_running_logic._update_timer()

    cycle_running_logic.sound_player.stop.assert_called_once()
    
def test_passes_multiple_actions_in_order(cycle_running_logic):
    with patch.object(cycle_running_logic, "cycle_factory") as mock:
        sound_config = {"sound_id": 1, "file_name": "test", "duration": 1000, "volume": 50}
        mock.get_cycle_by_id.return_value = CycleConfig(1, "test cycle", 3000, 70, actions=[
            CycleAction(0, ActionType.SOUND_START, sound_config),
            CycleAction(100, ActionType.SOUND_START, sound_config)
        ])
        cycle_running_logic.start_cycle(1)
        cycle_running_logic.light_controller.change_lights.assert_called_once_with(0.7)

        cycle_running_logic._update_timer()
        cycle_running_logic.sound_player.play.assert_called_once_with(SoundConfig("test", 1, 1000, 50))

        cycle_running_logic._update_timer()
        cycle_running_logic.sound_player.play.assert_called_with(SoundConfig("test", 1, 1000, 50))

def test_no_active_cycle_on_finish(cycle_running_logic, mock_cycle_factory):
    cycle_running_logic.current_cycle = mock_cycle_factory.get_cycle_by_id(1)
    cycle_running_logic._finish_cycle()
    assert not cycle_running_logic._active_cycle

def test_stops_sound_on_finished(cycle_running_logic):
    cycle_running_logic._finish_cycle()
    cycle_running_logic.sound_player.stop.assert_called_once()

def test_sets_lights_to_idle_on_finished(cycle_running_logic):
    cycle_running_logic._finish_cycle()
    cycle_running_logic.light_controller.system_idle.assert_called_once()

##### PAUSING AND RESUMING ####
def test_pause_stops_timer_progress(cycle_running_logic):
    cycle_running_logic.start_cycle(1)

    cycle_running_logic.pause_cycle()
    assert not cycle_running_logic._active_timer

def test_pause_retains_cycle_config(cycle_running_logic):
    cycle_running_logic.start_cycle(1)
    cycle_running_logic.pause_cycle()

    assert cycle_running_logic._active_cycle

def test_pause_notifies_lower_layer(cycle_running_logic):
    cycle_running_logic.start_cycle(1)

    cycle_running_logic.pause_cycle()

    cycle_running_logic.light_controller.system_idle.assert_called_once()
    cycle_running_logic.sound_player.stop.assert_called_once()

def test_resumes_restarts_timer_progress(cycle_running_logic):
    cycle_running_logic.start_cycle(1)

    cycle_running_logic.pause_cycle()
    cycle_running_logic.resume_cycle()

    assert cycle_running_logic._active_timer

def test_next_action_is_dispatched_after_resume(cycle_running_logic):
    with patch.object(cycle_running_logic, "cycle_factory") as mock:
        first_sound = {"sound_id": 1, "file_name": "first", "duration": 1000, "volume": 50}
        second_sound = {"sound_id": 2, "file_name": "second", "duration": 1000, "volume": 50}
        mock.get_cycle_by_id.return_value = CycleConfig(1, "test cycle", 3000, 70, actions=[
            CycleAction(0, ActionType.SOUND_START, first_sound),
            CycleAction(150, ActionType.SOUND_START, second_sound)
        ])
        cycle_running_logic.start_cycle(1)
        cycle_running_logic._update_timer()
        cycle_running_logic.pause_cycle()
        cycle_running_logic.resume_cycle()

        cycle_running_logic.sound_player.play.reset_mock()
        cycle_running_logic._update_timer()
    cycle_running_logic.sound_player.play.assert_called_with(SoundConfig("second", 2, 1000, 50))

def test_stop_after_pause_resets_state(cycle_running_logic):
    cycle_running_logic.start_cycle(1)
    cycle_running_logic.pause_cycle()
    cycle_running_logic.stop_cycle()

    assert not cycle_running_logic._active_cycle
    assert not cycle_running_logic._active_timer

#### STOPPING BEHAVIOR ####
def test_stop_notifies_lower_layer(cycle_running_logic):
    cycle_running_logic.start_cycle(1)
    cycle_running_logic.stop_cycle()

    cycle_running_logic.light_controller.system_idle.assert_called_once()
    cycle_running_logic.sound_player.stop.assert_called_once()

def test_stop_resets_internal_state(cycle_running_logic):
    cycle_running_logic.start_cycle(1)
    cycle_running_logic.stop_cycle()

    assert not cycle_running_logic._active_cycle
    assert not cycle_running_logic._active_timer
