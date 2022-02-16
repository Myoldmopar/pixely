from inspect import currentframe


class ConfigBase(object):
    """
    An abstract base class for all possible configurations
    """
    def name(self) -> str:
        raise NotImplementedError(
            f"Must override {self.__class__.__name__}::{currentframe().f_back.f_code.co_name} in derived classes"
        )

    def run(self):
        raise NotImplementedError(
            f"Must override {self.__class__.__name__}::{currentframe().f_back.f_code.co_name} in derived classes"
        )
