import dataclasses
import typing

import requests

from Classes.Config.BaseConfig import BaseConfig
from Classes.Config.HandlerConfigs.ConditionHandler.Condition import Condition


@dataclasses.dataclass
class Task(BaseConfig):
    endpoint: str = None
    conditions: list[Condition] = None

    @staticmethod
    def _custom_conditions(data: list[dict]) -> list[Condition]:
        return [Condition().load_config(x) for x in data]

    def execute(self, request_callback: typing.Callable[[str], requests.Response]):
        for condition in self.conditions:
            if not condition.met(request_callback):
                return
        request_callback(self.endpoint)
