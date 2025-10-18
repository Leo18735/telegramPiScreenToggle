import dataclasses
import typing
import time
from Classes.Handler.BaseHandler import BaseHandler


@dataclasses.dataclass
class Task:
    temperature: float
    condition: str
    endpoint: str

    @classmethod
    def from_dict(cls, data: dict) -> typing.Self:
        data["temperature"] = float(data.get("temperature"))
        return cls(**data)


class TemperatureHandler(BaseHandler):
    def __init__(self, tasks: list[dict]):
        self._old_temperature: typing.Optional[float] = None
        self._tasks: list[Task] = [Task(**task) for task in tasks]

    def _get_temperature(self) -> float:
        return self._request("temperature/get").json().get("data").get("state")

    def run(self, run_condition: typing.Callable[[], bool] = lambda: True):
        self._old_temperature = self._get_temperature()
        while True:
            temperature: float = self._get_temperature()
            for task in self._tasks:
                if task.condition == ">":
                    if self._old_temperature < temperature:
                        if temperature > task.temperature:
                            self._request(task.endpoint)
                elif task.condition == "<":
                    if self._old_temperature > temperature:
                        if temperature < task.temperature:
                            self._request(task.endpoint)
            self._old_temperature = temperature
            time.sleep(60)
