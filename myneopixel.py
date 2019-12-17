from rpi_ws281x import PixelStrip, Color
import time
import math

LED_COUNT = 144        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255    # initially   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


class Colors:
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    RED = Color(255, 0, 0)


def fade_in_time_and_values(num_steps, total_time, start_bright, end_bright):
    total_distance = end_bright - start_bright
    increment = total_distance / num_steps
    step_time = total_time / 50
    bright_values = [start_bright]
    this_bright = start_bright
    while this_bright <= end_bright:
        this_bright = this_bright + increment
        bright_values.append(this_bright)
    return step_time, bright_values


strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# reset back to zero
for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(0, 0, 0))

# delta_t, greens = fade_in_time_and_values(100, 2, 0, 255)
# for green_intensity in greens:
#     for pixel in range(0, LED_COUNT):
#         # print("Setting green intensity to: " + str(green_intensity))
#         strip.setPixelColor(pixel, Color(0, int(green_intensity), 0))
#     strip.show()
#     time.sleep(delta_t)

MAX_VAL = 20  # 255
MIN_VAL = 0
AMPLITUDE = (MAX_VAL - MIN_VAL) / 2
DIVISIONS = 12
c = 2 * math.pi / DIVISIONS
offsets = [
    -0 * c, -1 * c, -2 * c, -3 * c, -4 * c, -5 * c,
    -6 * c, -7 * c, -8 * c, -9 * c, -10 * c, -11 * c,
] * 8

time_step = 0.3
for offset in offsets:
    for pixel in range(LED_COUNT):
        x = pixel / LED_COUNT
        radians = 2 * 3.141 * x + offset
        green_value = AMPLITUDE + AMPLITUDE * math.sin(radians)
        strip.setPixelColor(pixel, Color(0, int(green_value), 0))
    strip.show()
    time_step *= 0.9
    time_step = max(time_step, 0.02)
    time.sleep(time_step)

for pixel in range(100):
    strip.setPixelColor(pixel, Color(0, int(pixel * 1), 0))
    strip.show()
    time.sleep(0.02)
#
# brightnesses = [0, 25, 50, 100, 125, 150, 175, 200, 225, 255, 225, 200, 175, 150, 125, 100, 75, 50, 25]
#
# while True:
#     for brightness in brightnesses:
#         for pixel in range(101, LED_COUNT):
#             strip.setPixelColor(pixel, Color(0, brightness, 0))
#         strip.show()
#         time.sleep(0.02)
