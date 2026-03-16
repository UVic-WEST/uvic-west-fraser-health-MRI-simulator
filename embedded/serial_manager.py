# embedded/serial_manager.py

try:
    import serial
except ImportError:
    serial = None

from embedded.pi_config import SERIAL_PORT, BAUD_RATE, SERIAL_TIMEOUT


class SerialManager:
    """
    Handles Raspberry Pi to STM32 serial communication.

    This is a baseline implementation for future integration testing.
    """

    def __init__(self, port: str = SERIAL_PORT, baud_rate: int = BAUD_RATE):
        self.port = port
        self.baud_rate = baud_rate
        self.connection = None

    def connect(self) -> bool:
        """
        Establish serial connection to STM32 if pyserial is available.
        """
        if serial is None:
            print("pyserial is not installed. SerialManager running in mock mode.")
            return False

        try:
            self.connection = serial.Serial(
                self.port,
                self.baud_rate,
                timeout=SERIAL_TIMEOUT
            )
            return True
        except Exception as e:
            print(f"Failed to open serial connection: {e}")
            self.connection = None
            return False

    def send_command(self, command: str) -> str:
        """
        Send a string command to the STM32.
        """
        if self.connection is None:
            return f"[MOCK SEND] {command}"

        try:
            self.connection.write((command + "\n").encode("utf-8"))
            return f"Sent command: {command}"
        except Exception as e:
            return f"Failed to send command: {e}"

    def read_response(self):
        """
        Read a response line from STM32 if available.
        """
        if self.connection is None:
            return None

        try:
            return self.connection.readline().decode("utf-8").strip()
        except Exception:
            return None

    def disconnect(self) -> None:
        """
        Close serial connection cleanly.
        """
        if self.connection is not None:
            self.connection.close()
            self.connection = None