import time
import typing

from Classes.Config.Config import TemperatureHandlerConfig
from Classes.Handler.BaseHandler import BaseHandler


class TemperatureHandler(BaseHandler[TemperatureHandlerConfig]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_temperature: typing.Optional[float] = None

    def _get_temperature(self) -> float:
        return self._request("temperature/get").json().get("data").get("state")

    def run(self):
        self._old_temperature = self._get_temperature()
        while True:
            temperature: float = self._get_temperature()
            for task in self._config.tasks:
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
