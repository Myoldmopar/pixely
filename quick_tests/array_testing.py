import math


class Pix(object):
    def __init__(self, _index, _x):
        self.green = 0
        self.index = _index
        self.x = _x


class ArmCharge(object):

    NUM_TIMES_TO_CHARGE = 3  # number of times to charge before fading and resonating
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
        for iteration in range(0, self.NUM_TIMES_TO_CHARGE):
            # each iteration, we just want to walk from the end to the beginning, and
            # move the value from upstream down one, then calculate a new value for the zeroth element by
            # adding a small shift to the calculated value
            for i in range(self.num_leds-1, 0, -1):
                self.values[i].green = self.values[i-1].green
            this_shift = iteration * 2 * math.pi * self.NUM_WAVES / self.num_leds
            self.values[0].green = self.amplitude + self.amplitude * math.sin(self.values[0].x - this_shift)
            print(','.join([str(int(x.green)) for x in self.values]))
            # strip.show()

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
            print(','.join([str(int(x.green)) for x in self.values]))
            # strip.show()
        # now one final pass to get them all to the target value
        for i in range(0, self.num_leds):
            self.values[i].green = self.TARGET_VALUE
        print(','.join([str(int(x.green)) for x in self.values]))
        # strip.show()

        # then resonate the last half period
        periods_ignored = self.NUM_WAVES - 1
        starting_led_of_last_period = self.lights_per_period * periods_ignored + 1
        starting_point_for_resonating = int((self.num_leds + starting_led_of_last_period) / 2)
        resonating_value_modifiers = [0, -2, -5, -10, -5, -2, 0, 5, 10, 20, 10, 5]
        resonating_values = [self.TARGET_VALUE + x for x in resonating_value_modifiers]
        for _ in range(3):  # while True:
            for val in resonating_values:
                for i in range(starting_point_for_resonating, self.num_leds):
                    self.values[i].green = val
                print(','.join([str(int(x.green)) for x in self.values]))
                # strip.show()
                # time.sleep(0.025)
        # this should be in a try...except block with a KeyboardInterrupt handler that cleans up and returns


ac = ArmCharge(144)
ac.run()
