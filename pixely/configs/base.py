from pixely.configs.trigger import Trigger
from pixely.actions.base import ActionBase
from typing import Dict


class ConfigBase(object):
    """
    An abstract base class for all possible configurations
    """

    def __init__(self):
        pass

    def switch_signals(self) -> Dict[ActionBase, Trigger]:
        """
        This returns a map with keys that are GPIO pins used to signal actions, and values that are those actions
        :return:
        """
        raise NotImplementedError('Must override switch_signals in derived classes')
