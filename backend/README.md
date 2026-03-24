# Backend (Layer 2)

Backend logic for the MRI Simulator. This layer sits between the frontend UI (Layer 1) and the hardware controllers (Layer 3). It manages cycle timing, authentication, state transitions, and hardware delegation — all without direct knowledge of UI widgets or GPIO pins.

## Files

### `auth.py`
Handles PIN-based authentication for the simulator. Validates a four-digit PIN, tracks remaining login attempts, and triggers a 15-second lockout after three consecutive failures. Uses `QTimer.singleShot` for the lockout countdown.

### `cycle_logic.py`
The core "heartbeat" of a running cycle. Uses a 100ms `QTimer` to track elapsed time against total duration. Emits `progress_changed`, `time_changed`, and `cycle_finished` signals for the UI. Supports play, pause, resume, and stop. Dispatches timestamped `CycleAction`s to the hardware controller during playback.

### `cycle_controller.py`
Bridge between Layer 2 and Layer 3. Wraps `LightController` and `SoundPlayer` behind a single interface with `start_cycle()`, `stop_cycle()`, and `dispatch_action()`. Emits `started`/`failed` signals so `CycleLogic` can react to hardware status.

### `cycle_running_page_logic.py`
Backend controller for the cycle-running page. Owns a 1-second countdown timer that emits `time_signal_in_s` for the frontend `TimerWidget`. Delegates hardware start/stop to `CycleController` on each lifecycle event (start, pause, resume, stop, completion).

### `cycle_config.py`
Dataclass representing a single MRI simulation cycle. Stores cycle ID, name, duration (ms), and an ordered list of `CycleAction` objects. Includes `to_json()`/`from_json()` for saving and loading cycle configurations.

### `cycle_action.py`
Dataclass representing a single timestamped action within a cycle (e.g. "turn on lights at 0ms", "play sound at 1000ms"). Also defines the `ActionType` enum (`SOUND_START`, `SOUND_STOP`, `LIGHT_ON`, `LIGHT_OFF`, etc.).

### `cycle_factory.py`
Factory that provides predefined cycle configurations (e.g. Standard MRI, Fast MRI). Cycles are retrieved by ID or index. New presets are added by creating private `_create_cycleN()` methods.

### `sound_config.py`
Dataclass for a single sound track configuration. Stores file name, duration (seconds), and volume (0–100). Used by `SoundPlayer.play()` and by `CycleController` when dispatching `SOUND_START` actions.

### `home_page_logic.py`
Stub controller for the home page. Not yet implemented.

## Architecture

```
Frontend (Layer 1)          Backend (Layer 2)              Hardware (Layer 3)
─────────────────          ──────────────────              ──────────────────
TimerWidget         ←──    CycleRunningPageLogic    ──→    CycleController
                                                            ├── LightController
CycleRunningPage    ←──    CycleLogic               ──→    └── SoundPlayer
                                ↑
SignInPage           ←──   Auth
HomePage             ←──   HomePageLogic (stub)
```

Signals flow left (to UI), method calls flow right (to hardware).
