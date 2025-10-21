import dataclasses

from Classes.Config.BaseConfig import BaseConfig
from Classes.Config.ControllerConfigs.BrightnessControllerConfig import BrightnessControllerConfig
from Classes.Config.ControllerConfigs.FanControllerConfig import FanControllerConfig
from Classes.Config.ControllerConfigs.ScreenControllerConfig import ScreenControllerConfig
from Classes.Config.ControllerConfigs.SlideshowControllerConfig import SlideshowControllerConfig
from Classes.Config.ControllerConfigs.TemperatureControllerConfig import TemperatureControllerConfig


@dataclasses.dataclass
class ControllerConfig(BaseConfig):
    brightness_controller: BrightnessControllerConfig = dataclasses.field(default_factory=BrightnessControllerConfig)
    fan_controller: FanControllerConfig = dataclasses.field(default_factory=FanControllerConfig)
    temperature_controller: TemperatureControllerConfig = dataclasses.field(default_factory=TemperatureControllerConfig)
    screen_controller: ScreenControllerConfig = dataclasses.field(default_factory=ScreenControllerConfig)
    slideshow_controller: SlideshowControllerConfig = dataclasses.field(default_factory=SlideshowControllerConfig)
