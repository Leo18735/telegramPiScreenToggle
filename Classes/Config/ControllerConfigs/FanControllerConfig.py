import dataclasses

from Classes.Config.BaseConfig import BaseConfig


@dataclasses.dataclass
class FanControllerConfig(BaseConfig):
    pin: int = None
