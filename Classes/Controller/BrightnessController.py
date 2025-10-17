import re
from Classes.Controller.BaseController import BaseController


class BrightnessController(BaseController):
    _file: str = "/sys/class/backlight/10-0045/brightness"

    def set_state(self, brightness: int):
        with open(self._file, "w") as f:
            f.write(str(brightness))

    def get_state(self):
        with open(self._file, "r") as f:
            return re.findall(r"\d+", f.read())[0]
