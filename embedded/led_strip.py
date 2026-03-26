import time

try:
    from pi5neo import Pi5Neo
except ImportError:
    class Pi5Neo:  # Mock library for running app on non-Raspberry pi OS 
        def __init__(self, *args, **kwargs):
            self.num_leds = 120
        def set_led_color(self, *args, **kwargs): pass
        def clear_strip(self): print("LEDs off")
        def update_strip(self): print("LEDs updated")

class LEDStrip:
    """
        Controls the LED light strip directly using SPI and Pi5Neo library

        Adapted from code provided by the electrical team!

        Args:
            spi_device: path to the SPI device (default: '/dev/spidev0.0')
            led_count:  number of LEDs in the strip (default: 120)
            led_freq:   SPI clock speed in kHz (default: 800)
    """

    def __init__(self, spi_device='/dev/spidev0.0', led_count=120, led_freq=800):
        self.strip = Pi5Neo(spi_device, led_count, led_freq)


    def set_white(self, brightness):
        """
            Set the brightness (float between 0.0 and 1.0) of the LED strip

            Example:
                strip.set_white(0.5)  # 50% brightness
        """
        r = int(255 * brightness)
        g = int(204 * brightness)
        b = int(153 * brightness)

        self.strip.clear_strip()
        for i in range(self.strip.num_leds):
            self.strip.set_led_color(i, g, r, b)
        self.strip.update_strip()

    def power_off(self):
        """
        Turn off all LEDs on the strip 
        """
        self.strip.clear_strip()
        self.strip.update_strip()


if __name__ == '__main__': # Running `python led_strip.py` to test

    led = LEDStrip()

    print('Press Ctrl-C to quit.')

    try:
        while True:
            val = input("Enter brightness (0-255): ")
            try:
                brightness = int(val)
                if 0 <= brightness <= 255:
                    led.set_white(brightness)
                else:
                    print("Please enter a number between 0 and 255.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    except KeyboardInterrupt:
        led.power_off()