import time
from gpiozero import LED


# Initialize the LED on Broadcom pin GPIO17
led = LED(17)

class LEDStrip:
    """
        Controls an individual LED light for testing software to hardware integration. 

        Args:
            spi_device: path to the SPI device (default: '/dev/spidev0.0')
            led_count:  number of LEDs in the strip (default: 120)
            led_freq:   SPI clock speed in kHz (default: 800)
    """

    # def __init__(self, spi_device='/dev/spidev0.0', led_count=120, led_freq=800):
    #     self.strip = Pi5Neo(spi_device, led_count, led_freq)


    def set_white(self, brightness):
        """
            Set the brightness (float between 0.0 and 1.0) of the LED strip

            Example:
                strip.set_white(0.5)  # 50% brightness
        """
        if brightness > 0.5:
            led.on()
        else:
            led.off()

    def power_off(self):
        """
        Turn off all LEDs on the strip 
        """
        led.off()


if __name__ == '__main__': # Running `python led_strip.py` to test

    led = LEDStrip()

    print('Press Ctrl-C to quit.')

    try:
        while True:
            val = input("Enter brightness (0-255): ")
            try:
                brightness = val
                if 0 <= brightness <= 1:
                    led.set_white(brightness)
                else:
                    print("Please enter a number between 0 and 1.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    except KeyboardInterrupt:
        led.power_off()