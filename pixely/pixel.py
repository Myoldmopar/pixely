from pixely.colors import PixelyColor


class StripRGBPixel(PixelyColor):
    """
    A class representing a single RGB pixel along an LED strip, with RGB members along with x and index members
    """
    def __init__(self, index: int, x: float):
        """
        Initialize the StripRGBPixel instance

        :param index: Zero-based index of pixel on the LED strip
        :param x: A physical representation of the x-position of this pixel, not necessarily accurate to real-life
        """
        super().__init__()
        self.index = index
        self.x = x
