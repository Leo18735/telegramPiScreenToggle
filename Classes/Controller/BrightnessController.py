import re

from Classes.Config.Config import BrightnessControllerConfig
from Classes.Controller.BaseController import BaseController


class BrightnessController(BaseController[BrightnessControllerConfig]):
    def set_state(self, brightness: int):
        with open(self._config.file, "w") as f:
            f.write(str(brightness))

    def get_state(self):
        with open(self._config.file, "r") as f:
            return re.findall(r"\d+", f.read())[0]
