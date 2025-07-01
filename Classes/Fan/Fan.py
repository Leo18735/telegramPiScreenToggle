import typing

from Classes.State.StateIn import StateIn
from Classes.State.StateOut import StateOut
from Classes.Fan.GPIO import GPIO


class Fan:
    def __init__(self, pin: int, *_, **__):
        self._pin: int = pin
        self._state: typing.Optional[StateOut] = None
        self._state = self.set(StateIn.OFF)

    def set(self, state: StateIn) -> StateOut:
        new_state: typing.Optional[StateIn] = None
        match (self._state, state):
            case (StateOut.BLOCK, StateIn.UNBLOCK):
                new_state = StateIn.OFF
            case (StateOut.BLOCK, _):
                return StateOut.BLOCK
            case (s1, s2) if s1 == s2:
                return self._state
            case (_, s) if s in (StateIn.ON, StateIn.OFF):
                new_state = s
            case (s1, s2):
                raise Exception(f"Unhandled {s1.name} {s2.name}")
        self._state = GPIO.set_state(self._pin, new_state)
        return self.get()

    def get(self) -> StateOut:
        return self._state
