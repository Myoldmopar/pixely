response = None


class GPIO(object):
    """
    Provides a way to mock the GPIO class, useful for testing or just development on non-RPi machines
    """

    @staticmethod
    def set_next_response(x):
        global response
        response = x

    @staticmethod
    def reset_next_response():
        global response
        response = None

    # Mocked stuff below

    # pin numbering schemes, we'll always use GPIO (BCM), but we can include here as we're mocking it
    BCM = 1
    BOARD = 2

    # pin status
    IN = 1
    OUT = 2

    # pull up/down status
    PUD_DOWN = 1

    # event type
    RISING = 1
    FALLING = 2
    BOTH = 3

    @staticmethod
    def input(x):
        pass

    @staticmethod
    def cleanup():
        pass

    @staticmethod
    def setmode(x):
        pass

    @staticmethod
    def setup(pin: int, status: int, pull_up_down: int = 0):
        pass

    @staticmethod
    def setwarnings(flag: bool):
        pass

    @staticmethod
    def add_event_detect(channel: int, event_type: int):
        pass

    @staticmethod
    def event_detected(channel: int):
        pass
