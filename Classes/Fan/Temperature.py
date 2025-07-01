import re
import typing

from Classes.State import State
from Utils.utils import execute
from Classes.StateCommand import StateCommand


class Temperature(StateCommand):
    _command: str = "vcgencmd measure_temp"

    def __init__(self, min_temp: float, max_temp: float, *_, **__):
        self._min_temp: float = min_temp
        self._max_temp: float = max_temp

    @classmethod
    def get(cls) -> float:
        stdout, _, code = execute(cls._command)
        if code != 0:
            return -1
        try:
            return float(re.findall(r"temp=(\d+\.\d+)'C", stdout)[0])
        except:
            pass
        return -1

    def get_change(self) -> typing.Optional[State]:
        temp: float = self.get()
        if temp == -1:
            return None
        if temp > self._max_temp:
            return State.ON
        if temp < self._min_temp:
            return State.OFF
        return None

    def get_text(self) -> str:
        return f"\n\tTemp: {self.get()}"
