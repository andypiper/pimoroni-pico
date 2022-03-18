import time
import math
from pimoroni import Button
from plasma import WS2812
from servo import ServoCluster, servo2040

# Press "Boot" to exit the program.

# NOTE: ServoCluster lets you control up to 30 servos at once. This is
# done using the RP2040's PIO system. As such it is experimental and may
# have edge-cases that will need to be fixed. This is particularly true
# when attempting to run a program multiple times.
# If you do encounter issues, try resetting your board.

SPEED = 5             # The speed that the LEDs will cycle at
BRIGHTNESS = 0.4      # The brightness of the LEDs
UPDATES = 50          # How many times the LEDs and Servos will be updated per second
SERVO_EXTENT = 80.0   # How far from zero to move the servos

# Create a servo cluster for pins 0 to 7, using PIO 0 and State Machine 0
START_PIN = servo2040.SERVO_1
END_PIN = servo2040.SERVO_8
servos = ServoCluster(pio=0, sm=0, pins=list(range(START_PIN, END_PIN + 1)))

# Create the LED bar, using PIO 1 and State Machine 0
led_bar = WS2812(servo2040.NUM_LEDS, 1, 0, servo2040.LED_DAT)

# Create the user button
user_sw = Button(servo2040.USER_SW)

# Start updating the LED bar
led_bar.start()


offset = 0.0

# Make waves until the user button is pressed
while user_sw.raw() is not True:

    offset += SPEED / 1000.0

    # Update all the LEDs
    for i in range(servo2040.NUM_LEDS):
        hue = i / (servo2040.NUM_LEDS * 4)
        led_bar.set_hsv(i, hue + offset, 1.0, BRIGHTNESS)

    # Update all the Servos
    for i in range(servos.count()):
        angle = ((i / servos.count()) + offset) * math.pi * 2
        servos.value(i, math.sin(angle) * SERVO_EXTENT, load=False)
    servos.load()  # We have now set all the servo values, so load them

    time.sleep(1.0 / UPDATES)

# Stop all the servos
servos.disable_all()

# Turn off the LED bar
led_bar.clear()
