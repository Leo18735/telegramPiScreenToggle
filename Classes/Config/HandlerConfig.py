import dataclasses

from Classes.Config.BaseConfig import BaseConfig
from Classes.Config.HandlerConfigs.ConditionHandlerConfig import ConditionHandlerConfig
from Classes.Config.HandlerConfigs.FlaskHandlerConfig import FlaskHandlerConfig
from Classes.Config.HandlerConfigs.TimeHandlerConfig import TimeHandlerConfig


@dataclasses.dataclass
class HandlerConfig(BaseConfig):
    time_handler: TimeHandlerConfig = dataclasses.field(default_factory=TimeHandlerConfig)
    condition_handler: ConditionHandlerConfig = dataclasses.field(default_factory=ConditionHandlerConfig)
    flask_handler: FlaskHandlerConfig = dataclasses.field(default_factory=FlaskHandlerConfig)
