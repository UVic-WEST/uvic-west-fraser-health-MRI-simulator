import time
from gpiozero import LED

class LEDStrip:
    """
    Controls a single LED on GPIO 17
    Replaces the LED strip with a basic GPIO LED
    """
    def __init__(self, gpio_pin=17):
        self.led = LED(gpio_pin)
    
    def set_white(self, brightness):
        """
        Turn LED on/off based on brightness (0-255)
        brightness > 127 = LED on, otherwise off
        
        For PWM dimming, use:
            self.led.value = brightness / 255.0
        """
        if brightness > 127:
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
            val = input("Enter brightness (0-255): ")
            try:
                brightness = int(val)
                if 0 <= brightness <= 255:
                    led.set_white(brightness)
                    print(f"LED {'on' if brightness > 127 else 'off'}")
                else:
                    print("Please enter a number between 0 and 255.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        led.power_off()
        print("\nLED turned off.")