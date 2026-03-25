"""Manual light controller (Layer 2).

Lets the user control light brightness outside of a running cycle.
Reserves the Layer 3 LightController while active and restores
default light levels when closed.
"""

from PySide6.QtCore import QObject

DEFAULT_BRIGHTNESS = 50


class ManualLightController(QObject):
    """Backend logic for manual light control on the home page.

    While active, the user can toggle lights on/off and adjust brightness
    in increments of 10 (0–100). When deactivated, lights return to
    default levels and the Layer 3 controller is released.

    Attributes:
        light_controller: Layer 3 LightController instance.
        is_active (bool): Whether the manual controller is currently in use.
        lights_on (bool): Whether the lights are currently turned on.
        brightness (int): Current brightness level (0–100).
    """

    def __init__(self, light_controller, parent=None):
        """Initialise with a reference to the Layer 3 light controller.

        Args:
            light_controller (LightController): Layer 3 hardware controller.
            parent (QObject, optional): Qt parent for ownership.
        """
        super().__init__(parent)
        self.light_controller = light_controller
        self.is_active = False
        self.lights_on = True
        self.brightness = DEFAULT_BRIGHTNESS

    def set_manual_light_controller_status(self, on: bool) -> bool:
        """Activate or deactivate the manual light controller.

        When activated, the light controller is reserved and lights turn on
        at the current brightness. When deactivated, lights return to default
        and the controller is released.

        Args:
            on (bool): True to activate, False to deactivate.

        Returns:
            bool: True if the operation succeeded.
        """
        if on:
            self.is_active = True
            self.lights_on = True
            self.brightness = DEFAULT_BRIGHTNESS
            self.light_controller.change_lights(self.brightness / 100.0)
        else:
            self.is_active = False
            self.lights_on = True
            self.brightness = DEFAULT_BRIGHTNESS
            self.light_controller.system_idle()

        return True

    def toggle_lights(self, on: bool) -> bool:
        """Turn the lights fully on or fully off.

        Brightness level is preserved while off so it can be adjusted
        and will apply when lights are turned back on.

        Args:
            on (bool): True to turn lights on, False to turn off.

        Returns:
            bool: True if the operation succeeded.
        """
        print("light is on:" + str(on))
        if not self.is_active:
            return False

        self.lights_on = on

        if on:
            self.light_controller.change_lights(self.brightness / 100.0)
        else:
            self.light_controller.system_off()

        return True

    def update_brightness(self, light_level: int) -> bool:
        """Update the brightness level.

        The brightness is stored even if lights are off, and will be
        applied when lights are turned back on.

        Args:
            light_level (int): Brightness from 0 to 100 in increments of 10.

        Returns:
            bool: True if the operation succeeded, False if inactive or
                light_level is out of range.
        """
        print("brightness has been updated to" + str(light_level))

        if not self.is_active:
            return False

        if light_level < 0 or light_level > 100 or light_level % 10 != 0:
            return False

        self.brightness = light_level

        if self.lights_on:
            self.light_controller.change_lights(self.brightness / 100.0)

        return True
