import time
from gpiozero import LED

class LEDStrip: # Change embedded/led_controller.py to use this LEDStrip class to test frontend -> SPI connection
    """
    Controls a single LED on GPIO 10
    Replaces the LED strip with a basic GPIO LED
    """
    def __init__(self, gpio_pin=10):
        self.led = LED(gpio_pin)
    
    def set_white(self, brightness):
        """
        Turn LED on/off based on brightness (0.0-1.0)
        brightness >= 0.5 = LED on, otherwise off

        For PWM dimming, use:
            self.led.value = brightness
        """
        if brightness >= 0.5:
            self.led.on()
        else:
            self.led.off()
    
    def power_off(self):
        """
        Turn off the LED
        """
        self.led.off()

if __name__ == '__main__':  # Running `python led_strip.py` to test
    led = LEDStrip()
    print('Press Ctrl-C to quit.')
    try:
        while True:
            val = input("Enter brightness (0.0-1.0): ")
            try:
                brightness = float(val)
                if 0 <= brightness <= 1:
                    led.set_white(brightness)
                    print(f"LED {'on' if brightness >= 0.5 else 'off'}")
                else:
                    print("Please enter a number between 0 and 1.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        led.power_off()
        print("\nLED turned off.")
