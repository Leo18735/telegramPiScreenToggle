import re
import typing

from Classes.State import State
from Utils.utils import execute


class Temperature:
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
        finally:
            raise Exception("Could not get temp")

    def get_change(self) -> typing.Optional[State]:
        temp: float = self.get()
        if temp > self._max_temp:
            return State.ON
        if temp < self._min_temp:
            return State.OFF
        return None
