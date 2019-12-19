from pixely.configs.base import ConfigBase


class DoctorStrangeCostume(ConfigBase):

    def __init__(self):
        super().__init__()

    def switch_signals(self) -> dict:
        return {}
