import time
from gpiozero import LED

# Initialize the LED on Broadcom pin GPIO17
led = LED(17)

try:
    print("Blinking LED... Press Ctrl+C to stop.")
    while True:
        led.on()       # Turn LED on (3.3V)
        time.sleep(1)  # Wait 1 second
        led.off()      # Turn LED off (0V)
        time.sleep(1)  # Wait 1 second

except KeyboardInterrupt:
    print("\nProgram stopped safely.")
