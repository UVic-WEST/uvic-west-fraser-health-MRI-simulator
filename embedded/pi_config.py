# embedded/pi_config.py

"""
Central configuration for Raspberry Pi deployment.

This file stores Raspberry Pi-specific runtime settings so they can
be updated in one place during hardware integration.
"""

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200
SERIAL_TIMEOUT = 1.0

AUDIO_MIXER = "PCM,0"
AUDIO_PLAYER_CMD = "aplay"
AUDIO_STOP_CMD = "killall"

RUNNING_ON_PI = False  # Set True during Raspberry Pi deployment testing