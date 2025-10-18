import dataclasses

from Classes.Config.BaseConfig import BaseConfig


@dataclasses.dataclass
class ScreenControllerConfig(BaseConfig):
    command: str = None
