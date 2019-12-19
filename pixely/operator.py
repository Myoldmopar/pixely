from time import sleep

try:
    from RPi.GPIO import input
    import RPi.GPIO as GPIO
except ImportError:
    from pixely.gpio_mock.GPIO import GPIO


class Operator(object):
    """
    This class is a main operator for the Raspberry Pi light show.
    """
    def __init__(self, configuration):
        self.configuration = configuration

    def run(self) -> None:
        """
        This is the main driver function, which includes an infinite loop and performs operations according to the
        specified configuration.
        :return:
        """
        GPIO.setmode(GPIO.BCM)
        try:
            while True:  # this will carry on until you hit CTRL+C
                if GPIO.input(25):  # if port 25 == 1
                    print("Port 25 is 1/GPIO.HIGH/True - button pressed")
                else:
                    print("Port 25 is 0/GPIO.LOW/False - button not pressed")
                sleep(0.1)  # wait 0.1 seconds

        except KeyboardInterrupt:
            GPIO.cleanup()  # clean up after yourself
