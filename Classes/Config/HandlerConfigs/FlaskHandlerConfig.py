import dataclasses

from Classes.Config.BaseConfig import BaseConfig


@dataclasses.dataclass
class FlaskHandlerConfig(BaseConfig):
    ip: str = None
    port: int = None
