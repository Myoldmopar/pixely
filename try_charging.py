
class FakeLED:
    def __init__(self, nominal_color=(0, 255, 0)):
        self.nominal_color = nominal_color
        self.current_color = (0, 0, 0)


def print_strip(_led_strip):
    colors = [str(x.current_color) for x in _led_strip]
    string = ' -- '.join(colors)
    print(string)


led_strip = [FakeLED()] * 10


print_strip(led_strip)