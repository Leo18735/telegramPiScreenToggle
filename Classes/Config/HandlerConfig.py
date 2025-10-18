import dataclasses

from Classes.Config.BaseConfig import BaseConfig
from Classes.Config.HandlerConfigs.FlaskHandlerConfig import FlaskHandlerConfig
from Classes.Config.HandlerConfigs.TemperatureHandlerConfig import TemperatureHandlerConfig
from Classes.Config.HandlerConfigs.TimeHandlerConfig import TimeHandlerConfig


@dataclasses.dataclass
class HandlerConfig(BaseConfig):
    time_handler: TimeHandlerConfig = dataclasses.field(default_factory=TimeHandlerConfig)
    temperature_handler: TemperatureHandlerConfig = dataclasses.field(default_factory=TemperatureHandlerConfig)
    flask_handler: FlaskHandlerConfig = dataclasses.field(default_factory=FlaskHandlerConfig)
