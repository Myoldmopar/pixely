from rpi_ws281x import Color as Color
from pixely.colors import PixelyColor
from subprocess import check_call
import sys


class MockStrip:

    def __init__(self, num_leds: int, *_):
        self.response = None
        self.num_leds = num_leds
        self.leds = [PixelyColor.Off] * num_leds

    def set_next_response(self, x):
        self.response = x

    def clear_response(self):
        self.response = None

    def begin(self):
        return self.response

    # noinspection PyPep8Naming
    def setPixelColor(self, index: int, c: Color):
        self.leds[index] = c
        return self.response

    @staticmethod
    def rgb_from_color(c: Color):
        b = c & 0xff
        g = (c >> 8) & 0xff
        r = (c >> 16) & 0xff
        return r, g, b

    def show(self):
        sys.stdout.write('\r')
        sys.stdout.flush()
        format_string = ""
        for led in self.leds:
            rgb = MockStrip.rgb_from_color(led)
            format_string += f"\\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m█\\x1b[0m"
        check_call(['printf', format_string])
        sys.stdout.flush()
        return self.response


if __name__ == "__main__":
    m = MockStrip(144)
    [m.setPixelColor(x, Color(219, x, 0)) for x in range(80)]
    m.show()
