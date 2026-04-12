# Backend (Layer 2)

Backend logic for the MRI Simulator. This layer sits between the frontend UI (Layer 1) and the hardware controllers (Layer 3). It manages cycle timing, authentication, state transitions, and hardware delegation — all without direct knowledge of UI widgets or GPIO pins.

## Files

### `auth.py`
Handles PIN-based authentication for the simulator. Validates a four-digit PIN, tracks remaining login attempts, and triggers a 15-second lockout after three consecutive failures. Uses a 1-second `QTimer` to manage the lockout countdown and emits a `countdown` signal for the UI.

### `create_cycle_logic.py`
Backend logic for creating custom MRI cycles. Manages cycle configuration including duration, light level, sound groups, and sound mapping. Validates user input and generates corresponding `CycleAction` for playback. Supports previewing light levels and playing sample sounds via hardware controllers. Saves completed cycles through `CycleRepository`.

### `cycle_action.py`
Dataclass representing a single timestamped action within a cycle (e.g. "turn on lights at 0ms", "play sound at 1000ms"). Also defines the `ActionType` enum (`SOUND_START`, `SOUND_STOP`, `LIGHT_ON`, `LIGHT_OFF`, etc.). Includes validation on initialization and helper logic to determine when an action should execute during cycle playback.

### `cycle_config.py`
Dataclass representing a single MRI simulation cycle. Stores cycle ID, name, duration (ms), light configuration, volume and an ordered list of `CycleAction` objects. Provides validation, helper accessors, sound group mapping derived from actions, and to_dict()/from_dict() for serialization.

### `cycle_factory.py`
Provides MRI simulation cycle configurations loaded from `CycleRepository`. Supports retrieving and listing cycles, refreshing from storage, and managing custom cycles. Enforces preset cycle IDs and validates custom cycle ID ranges when creating or adding new cycles.

### `cycle_repository.py`
Handles persistence of MRI simulation cycles to a JSON file. Provides methods to load, save, add, update, and delete `CycleConfig` objects, as well as generate the next available cycle ID.

### `cycle_running_page_logic.py`
Backend controller for the cycle-running page. Manages cycle execution using a timer, emits countdown updates for the UI, and dispatches `CycleActions` to hardware controllers during playback. Supports start, pause, resume, and stop, and handles cycle completion and error signaling.

### `home_page_logic.py`
Backend controller for the home page. Provides access to available cycles via `CycleFactory` and supports deletion of cycles through `CycleRepository`.

### `manual_light_controller.py`
Backend logic for manual light control outside of a running cycle. Allows toggling lights on/off and adjusting brightness levels, while delegating changes to the `LightController`.

### `manual_sound_controller.py`
Backend logic for manual sound control outside of a running cycle. Allows playing up to three sounds simultaneously at a specified volume, using the `SoundPlayer`.

### `sound_config.py`
Dataclass representing a single sound configuration. Stores file name, sound ID, duration, volume, and optional file path, with validation on initialization.

### `sound_group_config.py`
Dataclass representing a group of sounds played together in a cycle. Stores group ID, group volume, and a list of `SoundConfig` objects, with validation for volume and group size.

### `cycles.json`
Cycle configurations are stored in backend/cycles.json as a list of serialized CycleConfig objects. Each cycle includes: id, name, duration_ms, light settings (on, brightness), volume, and a list of timestamped actions (SOUND_START, SOUND_STOP, etc.)

## Architecture

```
Frontend (Layer 1)          Backend (Layer 2)              Hardware (Layer 3)
─────────────────          ──────────────────              ──────────────────
TimerWidget         ←──    CycleRunningPageLogic    ──→    CycleController
                                                            ├── LightController
CycleRunningPage    ←──    CycleLogic               ──→    └── SoundPlayer
                                ↑
SignInPage           ←──   Auth
HomePage             ←──   HomePageLogic
```

Signals flow left (to UI), method calls flow right (to hardware).
