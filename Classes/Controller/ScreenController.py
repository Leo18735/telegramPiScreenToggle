import re

from Classes.Controller.BaseExecutionController import BaseExecutionController


class ScreenController(BaseExecutionController):
    _base_command: str = "XDG_RUNTIME_DIR=/run/user/1000 wlr-randr --output DSI-1"

    def get_state(self) -> bool:
        stdout, stderr, code = self._execute(self._base_command)
        if code != 0:
            raise Exception(f"Could not get screen state. {stderr}")
        return re.findall("enabled: (yes|no)", stdout[stdout.lower().find("dsi"):].lower())[0] == "yes"

    def set_state(self, state: bool):
        _, stderr, code = self._execute(f"{self._base_command} --{'on' if state else 'off'}")
        if code != 0:
            raise Exception(f"Could not set screen state. {stderr}")
