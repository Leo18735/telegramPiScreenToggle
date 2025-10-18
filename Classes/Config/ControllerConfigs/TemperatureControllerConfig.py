import dataclasses

from Classes.Config.BaseConfig import BaseConfig


@dataclasses.dataclass
class TemperatureControllerConfig(BaseConfig):
    command: str = None
