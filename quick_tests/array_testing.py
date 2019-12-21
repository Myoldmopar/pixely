from rpi_ws281x import PixelStrip, Color
import time
import math

from RPi import GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

LED_COUNT = 144        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # This will be the forever max brightness - use color values to alter brightness later (0, 255)
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


class Pix(object):
    def __init__(self, _index, _x):
        self.green = 0
        self.index = _index
        self.x = _x


def update_strip(values):
    for i in range(len(values)):
        strip.setPixelColor(i, Color(0, int(values[i].green), 0))
    strip.show()
    time.sleep(0.015)


class ArmCharge(object):

    NUM_TIMES_TO_CHARGE = 2  # number of times to charge before fading and resonating
    TARGET_VALUE = 15  # final target value for arm while resonating wrist
    NUM_STEPS = 20  # number of steps to fade to target value
    NUM_WAVES = 3  # number of oscillations during charging
    INITIAL_OFFSET = -math.pi / 2.0  # setting this as a quarter period makes it charge up nicely
    MAX_VAL = 255  # maximum brightness during charge-up

    def __init__(self, num_leds):
        self.num_leds = num_leds
        self.amplitude = self.MAX_VAL / 2.0
        self.lights_per_period = self.num_leds / self.NUM_WAVES

        self.values = []
        for i in range(0, self.num_leds):
            x = i * (2 * math.pi / self.lights_per_period) + self.INITIAL_OFFSET
            p = Pix(i, x)
            self.values.append(p)

    def run(self):

        # charge up the arm
        for iteration in range(0, self.num_leds * self.NUM_TIMES_TO_CHARGE):
            # each iteration, we just want to walk from the end to the beginning, and
            # move the value from upstream down one, then calculate a new value for the zeroth element by
            # adding a small shift to the calculated value
            for i in range(self.num_leds-1, 0, -1):
                self.values[i].green = self.values[i-1].green
            this_shift = iteration * 2 * math.pi * self.NUM_WAVES / self.num_leds
            self.values[0].green = self.amplitude + self.amplitude * math.sin(self.values[0].x - this_shift)
            update_strip(self.values)

        # fade down to the target value
        # store the values before we start altering them
        step_sizes = []
        for i in range(0, self.num_leds):
            actual_distance = self.TARGET_VALUE - self.values[i].green  # positive if we are too low
            step_sizes.append(actual_distance / self.NUM_STEPS)
        # now actually go in and gradually get them close to the target value (round-off error will occur)
        for step in range(0, self.NUM_STEPS):
            for i in range(0, self.num_leds):
                self.values[i].green += step_sizes[i]
            update_strip(self.values)
        # now one final pass to get them all to the target value
        for i in range(0, self.num_leds):
            self.values[i].green = self.TARGET_VALUE
        update_strip(self.values)

        # then resonate the last half period
        periods_ignored = self.NUM_WAVES - 1
        starting_led_of_last_period = self.lights_per_period * periods_ignored + 1
        starting_point_for_resonating = int(starting_led_of_last_period)  # int((self.num_leds + starting_led_of_last_period) / 2)
        resonating_value_modifiers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        resonating_values = [self.TARGET_VALUE + x for x in resonating_value_modifiers]
        for _ in range(5):  # while True:
            for val in resonating_values:
                for i in range(starting_point_for_resonating, self.num_leds):
                    self.values[i].green = val
                update_strip(self.values)
                time.sleep(0.02)
        # this should be in a try...except block with a KeyboardInterrupt handler that cleans up and returns


ac = ArmCharge(144)
ac.run()

