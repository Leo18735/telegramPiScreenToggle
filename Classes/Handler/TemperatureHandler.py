import time
import typing
from Classes.Handler.Handler import Handler
from Classes.Fan.Temperature import Temperature
from Classes.Fan.Fan import Fan
from Classes.State import State


class TemperatureHandler(Handler):
    def __init__(self, temperature: Temperature, fan: Fan, sleep_time: int, *_, **__):
        self._temperature: Temperature = temperature
        self._fan: Fan = fan
        self._sleep_time: int = sleep_time

    def run(self):
        while True:
            time.sleep(self._sleep_time)
            desired_state: typing.Optional[State] = self._temperature.get_change()
            if desired_state is None:
                continue
            self._fan.set(desired_state)
