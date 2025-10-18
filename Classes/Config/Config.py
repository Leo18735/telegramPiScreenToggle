from __future__ import annotations

import abc
import dataclasses
import inspect
import json
import re
import threading
import time
import typing

from Classes.Handler.TemperatureHandler.Task import Task as TemperatureTask
from Classes.Handler.TimeHandler.Task import Task as TimeTask


class BaseConfig(abc.ABC):
    @staticmethod
    def _custom_loader(obj: BaseConfig, key: str, value):
        method_name: str = f"_custom_{key}"
        if not hasattr(obj, method_name):
            return value
        method: typing.Callable = getattr(obj, method_name)
        if not inspect.isfunction(method):
            return value
        return method(value)

    def load_config(self, config: dict):
        for key, obj in self.__dict__.items():
            if key.startswith("_"):
                continue
            value = config.get(key)
            if isinstance(obj, BaseConfig):
                obj.load_config(value)
                continue
            setattr(self, key, self._custom_loader(self, key, value))
        return self


@dataclasses.dataclass
class BrightnessControllerConfig(BaseConfig):
    file: str = None


@dataclasses.dataclass
class FanControllerConfig(BaseConfig):
    pin: int = None


@dataclasses.dataclass
class ScreenControllerConfig(BaseConfig):
    command: str = None


@dataclasses.dataclass
class TemperatureControllerConfig(BaseConfig):
    command: str = None


@dataclasses.dataclass
class ControllerConfig(BaseConfig):
    brightness_controller: BrightnessControllerConfig = dataclasses.field(default_factory=BrightnessControllerConfig)
    fan_controller: FanControllerConfig = dataclasses.field(default_factory=FanControllerConfig)
    temperature_controller: TemperatureControllerConfig = dataclasses.field(default_factory=TemperatureControllerConfig)
    screen_controller: ScreenControllerConfig = dataclasses.field(default_factory=ScreenControllerConfig)


@dataclasses.dataclass
class TimeHandlerConfig(BaseConfig):
    tasks: list[TimeTask] = None

    @staticmethod
    def _custom_tasks(data: list[dict]) -> list[TimeTask]:
        return [TimeTask.from_dict(x) for x in data]


@dataclasses.dataclass
class TemperatureHandlerConfig(BaseConfig):
    tasks: list[TemperatureTask] = None

    @staticmethod
    def _custom_tasks(data: list[dict]) -> list[TemperatureTask]:
        return [TemperatureTask.from_dict(x) for x in data]


@dataclasses.dataclass
class FlaskHandlerConfig(BaseConfig):
    ip: str = None
    port: int = None


@dataclasses.dataclass
class HandlerConfig(BaseConfig):
    time_handler: TimeHandlerConfig = dataclasses.field(default_factory=TimeHandlerConfig)
    temperature_handler: TemperatureHandlerConfig = dataclasses.field(default_factory=TemperatureHandlerConfig)
    flask_handler: FlaskHandlerConfig = dataclasses.field(default_factory=FlaskHandlerConfig)


C = typing.TypeVar("C", bound=BaseConfig)


@dataclasses.dataclass
class Config(BaseConfig):
    controller: ControllerConfig = dataclasses.field(default_factory=ControllerConfig)
    handler: HandlerConfig = dataclasses.field(default_factory=HandlerConfig)
    _file: str = None
    _reload_interval: int = None

    @classmethod
    def load_config_file(cls, file: str, reload_interval: int) -> typing.Self:
        return cls(_file=file, _reload_interval=reload_interval)._reload()

    def __post_init__(self):
        threading.Thread(target=self._reload_thread, daemon=True).start()

    def _reload_thread(self):
        while True:
            time.sleep(self._reload_interval)
            self._reload()
            print(self.controller.fan_controller.pin)

    def _reload(self):
        with open(self._file, "r") as f:
            config: dict = json.load(f)
        return self.load_config(config)

    @classmethod
    def _find_config(cls, obj, name: str):
        if not isinstance(obj, BaseConfig):
            return None
        for config_name, config_object in obj.__dict__.items():
            if config_name == name:
                return config_object
            config: typing.Optional = cls._find_config(config_object, name)
            if config:
                return config
        return None

    @staticmethod
    def _camel_to_snake(name: str) -> str:
        return re.sub(
            r'([a-z0-9])([A-Z])', r'\1_\2',
            re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
        ).lower()

    def get_correct_config(self, name: str) -> C:
        return self._find_config(self, self._camel_to_snake(name))
