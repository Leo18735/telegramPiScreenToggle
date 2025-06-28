from Utils.utils import execute
import re
from Classes.State import State


class PiScreen:
    _command: str = "XDG_RUNTIME_DIR=/run/user/1000 wlr-randr --output DSI-1"

    def __init__(self):
        self._state: State = self._get()

    def set(self, state: State) -> State:
        if state == self._state:
            return State.NO_CHANGE
        if state not in (State.ON, State.OFF):
            raise Exception(f"State '{state.name}' not allowed")
        if execute(f"{self._command} {'--on' if state == State.ON else '--off'}")[2] != 0:
            return State.ERROR
        self._state = state
        return state

    @classmethod
    def _get(cls) -> State:
        stdout, _, code = execute(cls._command)
        if code != 0:
            return State.ERROR
        matches: list[str] = re.findall("enabled: (yes|no)", stdout[stdout.lower().find("dsi"):].lower())
        if len(matches) == 0:
            return State.ERROR
        return State.ON if matches[0] == "yes" else State.OFF
