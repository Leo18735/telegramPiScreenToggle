from Classes.State import State
from Utils.utils import execute
import re
from Classes.StateCommand import StateCommand


class PiScreen(StateCommand):
    _command: str = "XDG_RUNTIME_DIR=/run/user/1000 wlr-randr --output DSI-1"

    def __init__(self):
        self._state: State = self.get_current()

    def set(self, state: State):
        if state == self._state:
            return
        if state == State.ON:
            new_state = "on"
        elif state == State.OFF:
            new_state = "off"
        else:
            raise Exception(f"Unknown state {state.name}")
        print(f"Set screen {new_state}")
        self._state = state
        if execute(f"{self._command} --{new_state}")[2] != 0:
            raise Exception("Could not set screen state")

    @classmethod
    def get_current(cls) -> State:
        stdout, _, code = execute(cls._command)
        if code != 0:
            raise Exception("Could not get screen state")
        matches: list[str] = re.findall("enabled: (yes|no)", stdout[stdout.lower().find("dsi"):].lower())
        if len(matches) == 0:
            raise Exception("Could not get screen state")
        return State.ON if matches[0] == "yes" else State.OFF

    def get_state(self) -> dict:
        return {"State": self._state.name}
