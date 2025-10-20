from __future__ import annotations

import dataclasses
import json
import re
import threading
import time
import typing

from Classes.Config.BaseConfig import BaseConfig
from Classes.Config.ControllerConfig import ControllerConfig
from Classes.Config.HandlerConfig import HandlerConfig

C = typing.TypeVar("C", bound=BaseConfig)


@dataclasses.dataclass
class Config(BaseConfig):
    controller: ControllerConfig = dataclasses.field(default_factory=ControllerConfig)
    handler: HandlerConfig = dataclasses.field(default_factory=HandlerConfig)
    _file: str = None
    reload_interval: int = None
    _load_complete: bool = False

    @classmethod
    def load_config_file(cls, file: str) -> typing.Self:
        return cls(_file=file)

    def __post_init__(self):
        self._reload(True)
        while not self._load_complete:
            time.sleep(1)
        threading.Thread(target=self._reload_thread, daemon=True).start()

    def _reload_thread(self):
        while True:
            time.sleep(self.reload_interval)
            self._reload()

    def _reload(self, init: bool = False):
        with open(self._file, "r") as f:
            config: dict = json.load(f)
        self.load_config(config)
        if init:
            self._load_complete = True

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
