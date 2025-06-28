import re

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
        if code == 0:
            try:
                return float(re.findall(r"temp=(\d+\.\d+)'C", stdout)[0])
            except:
                pass
        return -1

    def get_change(self) -> State:
        temp: float = self.get()
        if temp < 0:
            return State.ERROR
        if temp > self._max_temp:
            return State.ON
        if temp < self._min_temp:
            return State.OFF
        return State.NO_CHANGE
