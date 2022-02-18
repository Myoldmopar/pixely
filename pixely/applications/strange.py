import time
import math

from rpi_ws281x import Color  # always import the innocent Color structure
try:
    # then try to import GPIO first, if we fail, use both the mock GPIO and mock PixelStrip classes
    import RPi.GPIO as GPIO
    from rpi_ws281x import PixelStrip
except (ImportError, RuntimeError):
    from pixely.mock.GPIO import GPIO
    from pixely.mock.pixelstrip import MockStrip as PixelStrip

from pixely.configuration import ConfigBase
from pixely.pixel import StripRGBPixel


class CostumeState:
    # there are different states for what the costume is 'doing'
    Idle = 0  # no lights on, waiting on input
    Charging = 1  # arms charging up in the correct color scheme, accents glowing
    Armed = 2  # accents bright, charging paths on but dim, wrists and hands glowing bright
    Calming = 3  # all lights calmly turn off

    Good = 0  # in this case the target color is green, 0, 255, 0
    Evil = 1  # in this case the target color is red, 255, 0, 0


class ArmLedStrip:
    def __init__(self, gpio_pin_number: int):
        self.num_leds = 144
        led_frequency_hz = 800000  # LED signal frequency in hertz (usually 800khz)
        led_dma_channel = 10  # DMA channel to use for generating signal (try 10)
        max_brightness = 255  # This sets the absolute max, so just use 255 and adjust brightness by individual colors
        led_invert = False  # True to invert the signal (when using NPN transistor level shift)
        led_channel = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
        self.strip = PixelStrip(
            self.num_leds, gpio_pin_number, led_frequency_hz, led_dma_channel, led_invert, max_brightness,
            led_channel
        )
        self.strip.begin()
        self.num_charging_waves = 3  # number of oscillations during charging
        initial_offset = -math.pi / 2.0  # setting this as a quarter period makes it charge up nicely
        self.lights_per_period = self.num_leds / self.num_charging_waves
        self.pixels = []
        for i in range(0, self.num_leds):
            x = i * (2 * math.pi / self.lights_per_period) + initial_offset
            p = StripRGBPixel(i, x)
            self.pixels.append(p)

    def calm(self):
        pass

    def charge(self):
        num_times_to_charge = 2  # number of times to charge before fading and resonating
        target_value = 15  # final target value for arm while resonating wrist
        num_steps = 20  # number of steps to fade to target value
        max_val = 255  # maximum brightness during charge-up
        amplitude = max_val / 2.0

        # charge up the arm
        for iteration in range(0, self.num_leds * num_times_to_charge):
            # each iteration, we just want to walk from the end to the beginning, and
            # move the value from upstream down one, then calculate a new value for the zeroth element by
            # adding a small shift to the calculated value
            for i in range(self.num_leds - 1, 0, -1):
                self.pixels[i].green = self.pixels[i - 1].green
            this_shift = iteration * 2 * math.pi * self.num_charging_waves / self.num_leds
            self.pixels[0].green = amplitude + amplitude * math.sin(self.pixels[0].x - this_shift)
            self.update()

        # fade down to the target value
        # store the values before we start altering them
        step_sizes = []
        for i in range(0, self.num_leds):
            actual_distance = target_value - self.pixels[i].green  # positive if we are too low
            step_sizes.append(actual_distance / num_steps)

        # now actually go in and gradually get them close to the target value (round-off error will occur)
        for step in range(0, num_steps):
            for i in range(0, self.num_leds):
                self.pixels[i].green += step_sizes[i]
            self.update()

        # now one final pass to get them all to the target value
        for i in range(0, self.num_leds):
            self.pixels[i].green = target_value
        self.update()

        # then resonate the last half period
        periods_ignored = self.num_charging_waves - 1
        starting_led_of_last_period = self.lights_per_period * periods_ignored + 1
        starting_point_for_resonating = int(starting_led_of_last_period)
        resonating_value_modifiers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                      19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        # list(range(21)) + list(reversed(range(1, 20)))
        resonating_values = [target_value + x for x in resonating_value_modifiers]
        for _ in range(5):
            for val in resonating_values:
                for i in range(starting_point_for_resonating, self.num_leds):
                    self.pixels[i].green = val
                self.update()
                time.sleep(0.02)
        # this should be in a try...except block with a KeyboardInterrupt handler that cleans up and returns
    
    def update(self):
        for i, p in enumerate(self.pixels):
            r = int(p.red)
            g = int(p.green)
            b = int(p.blue)
            self.strip.setPixelColor(i, Color(g, 0, g))
        self.strip.show()
        time.sleep(0.015)


class DoctorStrangeCostume(ConfigBase):

    def __init__(self):
        arm_led_pin = 18  # GPIO pin connected to the pixels (18 uses PWM!)
        self.arms = ArmLedStrip(arm_led_pin)  # for now both arms are parallel, ideally we do them individually L/R

    @staticmethod
    def setup_gpio():
        GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(15, GPIO.OUT)
        GPIO.setup(7, GPIO.OUT)
        # GPIO.add_event_detect(channel, GPIO.RISING)
        # time.sleep(20)
        # if GPIO.event_detected(channel):
        #     print('Button pressed')

    def name(self) -> str:
        return "Doctor Strange Full Costume"

    def run(self):
        GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print("Waiting for button press on board pin 36...")
        pressed = False
        while True:
            # button is pressed when pin is LOW
            if not GPIO.input(36):
                if not pressed:
                    self.arms.charge()
                    pressed = True
            # button not pressed (or released)
            else:
                pressed = False
            time.sleep(0.05)


if __name__ == "__main__":
    d = DoctorStrangeCostume()
    d.arms.charge()
