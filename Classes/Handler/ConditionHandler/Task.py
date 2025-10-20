import dataclasses
import typing

import requests


@dataclasses.dataclass
class Value:
    value: typing.Union[str, float, int]
    type: typing.Literal["value", "endpoint"]

    def get(self, request_callback: typing.Callable[[str], requests.Response]):
        assert self.type in ["value", "endpoint"]

        print(f"{self.value} {self.type}")

        match self.type:
            case "value":
                return self.value
            case "endpoint":
                response = request_callback(self.value).json()
                print(response)
                return response.get("data").get("state")


@dataclasses.dataclass
class Condition:
    value1: Value
    value2: Value
    comparator: typing.Literal["<", ">", "="]

    def met(self, request_callback: typing.Callable[[str], requests.Response]) -> bool:
        assert self.comparator in ["<", ">", "="]

        value1: typing.Union[float, int, str] = self.value1.get(request_callback)
        value2: typing.Union[float, int, str] = self.value2.get(request_callback)

        print(f"Values: {value1} {self.comparator} {value2}")

        match self.comparator:
            case ">":
                return value1 > value2
            case "<":
                return value1 < value2
            case "=":
                return value1 == value2

    @classmethod
    def from_dict(cls, data: dict) -> typing.Self:
        data["value1"] = Value(**data.get("value1"))
        data["value2"] = Value(**data.get("value2"))
        return cls(**data)


@dataclasses.dataclass
class Task:
    endpoint: str
    conditions: list[Condition]

    @classmethod
    def from_dict(cls, data: dict) -> typing.Self:
        data["conditions"] = [Condition.from_dict(x) for x in data.get("conditions", [])]
        return cls(**data)

    def execute(self, request_callback: typing.Callable[[str], requests.Response]):
        for condition in self.conditions:
            if not condition.met(request_callback):
                return
        request_callback(self.endpoint)
