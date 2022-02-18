import logging
import traceback

from pixely.configuration import ConfigBase
from pixely.exceptions import NormalResetAndTurnOff

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('debug.log', 'w', 'utf-8')
handler.setFormatter(logging.Formatter('%(name)s %(message)s'))
root_logger.addHandler(handler)

try:
    import RPi.GPIO as GPIO
    logging.debug("Importing actual RPi.GPIO library")
except (ImportError, RuntimeError):
    from pixely.gpio_mock.GPIO import GPIO
    logging.debug("Importing mock GPIO library (presumably for testing purposes)")


class Operator(object):
    """
    This class is a main operator for the Raspberry Pi light show.
    """
    def __init__(self, configuration: ConfigBase):
        self.configuration = configuration

    def run(self):
        """
        This is the main driver function, which initializes the basic GPIO mode, executes the configuration's run()
        method, and handles different exit conditions.  All specific pin configurations, actions, and triggers are
        handled in the run() method.
        """
        logging.debug("Operator started")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        try:
            logging.debug(f"Running configuration: {self.configuration.name()}")

            self.configuration.run()
        except (NormalResetAndTurnOff, KeyboardInterrupt):
            pass  # don't need to do anything, the finally: block will clean things up
        except Exception as e:
            print("Encountered an unexpected exception, reporting and aborting: ")
            print(str(e))
            traceback.print_exc()
        finally:
            GPIO.cleanup()
