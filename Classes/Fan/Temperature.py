import re
import time
import typing
from collections import deque
from Classes.Handler.Handler import Handler
from Classes.State import State
from Utils.utils import execute
from Classes.StateCommand import StateCommand


class Temperature(StateCommand, Handler):
    _command: str = "vcgencmd measure_temp"

    def __init__(self, min_temp: float, max_temp: float, update_interval: int, max_past_values: int, *_, **__):
        self._min_temp: float = min_temp
        self._max_temp: float = max_temp
        self._update_interval: int = update_interval
        self._past_temperatures: deque = deque(maxlen=max_past_values)

    @classmethod
    def get(cls, retries: int = 10) -> float:
        if retries == 0:
            raise Exception("Could not get temperature in 10 retries")
        stdout, _, code = execute(cls._command)
        try:
            return float(re.findall(r"temp=(\d+\.\d+)'C", stdout)[0])
        except (Exception, ):
            pass
        time.sleep(5)
        return cls.get(retries - 1)

    def get_change(self) -> typing.Optional[State]:
        temp: float = self.get()
        if temp > self._max_temp:
            return State.ON
        if temp < self._min_temp:
            return State.OFF
        return None

    def get_state(self) -> dict:
        return {"Temp": self.get(), "Max": self._get_max(), "Min": self._get_min()}

    def _get_max(self) -> float:
        return max(self._past_temperatures)

    def _get_min(self) -> float:
        return min(self._past_temperatures)

    def run(self):
        while True:
            self._past_temperatures.append(self.get())
            time.sleep(self._update_interval)
