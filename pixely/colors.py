from rpi_ws281x import Color as Color


class PixelyColor:
    """
    A class representing a single RGB pixel, or a combination of r, g, and b
    """
    Off = Color(0, 0, 0)
    Red = Color(255, 0, 0)
    Green = Color(0, 255, 0)
    Blue = Color(0, 0, 255)
    White = Color(255, 255, 255)
    Orange = Color(219, 87, 0)

    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0
