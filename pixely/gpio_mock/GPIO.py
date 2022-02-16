class GPIO(object):
    """
    Provides a way to mock the GPIO class, useful for testing or just development on non-RPi machines
    """

    def __init__(self):
        self._response = None

    def set_next_response(self, x):
        self._response = x

    def reset_next_response(self):
        self._response = None

    # Mocked stuff below

    # pin numbering schemes, we'll always use GPIO (BCM), but we can include here as we're mocking it
    BCM = 1
    BOARD = 2

    # pin status
    IN = 1
    OUT = 2

    def input(self, x):
        return self._response

    def cleanup(self):
        return self._response

    def setmode(self, x):
        return self._response

    def setup(self, pin, status):
        return self._response
