import math

NUM_LEDS = 10
MAX_VAL = 255
MIN_VAL = 0
AMPLITUDE = (MAX_VAL - MIN_VAL) / 2


class FakeLED:

    def __init__(self):
        self.green_value = 0
        self.x = 0
        self.radians = 0

    def __str__(self):
        return ("%s" % int(self.green_value)).zfill(3)


def print_strip(_led_strip):
    string = ', '.join([str(_led) for _led in _led_strip])
    print(string)


led_strip = []
for i in range(0, NUM_LEDS):
    led_strip.append(FakeLED())

for i, led in enumerate(led_strip):
    x = i / NUM_LEDS
    led.x = x

for offset in [0, -math.pi / 3, -2 * math.pi / 3, -math.pi, -4 * math.pi / 3, -5 * math.pi / 3]:
    for i, led in enumerate(led_strip):
        led.radians = 2 * 3.141 * led.x + offset
        led.green_value = AMPLITUDE + AMPLITUDE * math.sin(led.radians)
    print_strip(led_strip)
