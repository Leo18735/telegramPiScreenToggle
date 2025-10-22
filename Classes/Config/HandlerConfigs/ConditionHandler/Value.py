import dataclasses
import typing

import requests

from Classes.Config.BaseConfig import BaseConfig


@dataclasses.dataclass
class Value(BaseConfig):
    value: typing.Union[str, float, int] = None
    type: typing.Literal["value", "endpoint"] = None

    def get(self, request_callback: typing.Callable[[str], requests.Response]):
        assert self.type in ["value", "endpoint"]

        match self.type:
            case "value":
                return self.value
            case "endpoint":
                return request_callback(self.value).json().get("data").get("state")
