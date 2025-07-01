import typing
from Classes.State.StateIn import StateIn
from Utils.utils import execute
import re
from Classes.State.StateOut import StateOut


class PiScreen:
    _command: str = "XDG_RUNTIME_DIR=/run/user/1000 wlr-randr --output DSI-1"

    def __init__(self):
        self._state: StateOut = self.get_current()

    @classmethod
    def _set(cls, state: StateIn) -> StateOut:
        if state == StateIn.ON:
            new_state = "on"
            return_state = StateOut.ON
        elif state == StateIn.OFF:
            new_state = "off"
            return_state = StateOut.OFF
        else:
            raise Exception(f"Unknown state {state.name}")
        if execute(f"{cls._command} --{new_state}")[2] != 0:
            raise Exception("Could not set screen state")
        return return_state

    def set(self, state: StateIn) -> StateOut:
        new_state: typing.Optional[StateIn] = None
        match (self.get(), state):
            case (s1, s2) if s1 == s2:
                return self.get()
            case (_, s) if s in (StateIn.ON, StateIn.OFF):
                new_state = s
            case (s1, s2):
                raise Exception(f"Unhandled {s1.name} {s2.name}")

        self._state = self._set(new_state)
        return self.get()

    @classmethod
    def get_current(cls) -> StateOut:
        stdout, _, code = execute(cls._command)
        if code != 0:
            raise Exception("Could not get screen state")
        matches: list[str] = re.findall("enabled: (yes|no)", stdout[stdout.lower().find("dsi"):].lower())
        if len(matches) == 0:
            raise Exception("Could not get screen state")
        return StateOut.ON if matches[0] == "yes" else StateOut.OFF

    def get(self) -> StateOut:
        return self._state
