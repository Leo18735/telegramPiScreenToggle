import dataclasses
import typing
from dataclasses import field

import requests

from Classes.Config.BaseConfig import BaseConfig
from Classes.Config.HandlerConfigs.ConditionHandler.Value import Value


@dataclasses.dataclass
class Condition(BaseConfig):
    value1: Value = field(default_factory=Value)
    value2: Value = field(default_factory=Value)
    comparator: typing.Literal["<", ">", "="] = None

    def met(self, request_callback: typing.Callable[[str], requests.Response]) -> bool:
        assert self.comparator in ["<", ">", "="]

        value1: typing.Union[float, int, str] = self.value1.get(request_callback)
        value2: typing.Union[float, int, str] = self.value2.get(request_callback)

        match self.comparator:
            case ">":
                return value1 > value2
            case "<":
                return value1 < value2
            case "=":
                return value1 == value2

    @staticmethod
    def _custom_value1(data: dict) -> Value:
        return Value().load_config(data)

    @staticmethod
    def _custom_value2(data: dict) -> Value:
        return Value().load_config(data)
