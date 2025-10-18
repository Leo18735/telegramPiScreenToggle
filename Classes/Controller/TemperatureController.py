import re
from Classes.Controller.BaseExecutionController import BaseExecutionController


class TemperatureController(BaseExecutionController):
    _base_command: str = "vcgencmd measure_temp"

    def get_state(self) -> float:
        stdout, stderr, code = self._execute(self._base_command)
        if code != 0:
            raise Exception(f"Could not get temperature. {stderr}")
        return float(re.findall(r"temp=(\d+\.\d+)'C", stdout)[0])

    def set_state(self):
        raise NotImplementedError
