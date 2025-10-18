import dataclasses

from Classes.Config.BaseConfig import BaseConfig


@dataclasses.dataclass
class BrightnessControllerConfig(BaseConfig):
    file: str = None
