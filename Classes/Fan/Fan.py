from Classes.State import State
from Classes.Fan.GPIO import GPIO


class Fan:
    def __init__(self, pin: int, *_, **__):
        self._pin: int = pin
        self._state: State = State.ERROR
        self._state = self.set(State.OFF)

    def set(self, state: State) -> State:
        new_state: State = State.ERROR
        match (self._state, state):
            case (s1, s2) if s1 == s2:
                return State.NO_CHANGE
            case (_, s) if s == State.NO_CHANGE:
                return State.NO_CHANGE
            case (_, s) if s == State.ERROR:
                return State.NO_CHANGE
            case (State.BLOCK, s) if s != State.OFF:
                return State.BLOCK
            case (_, s) if s == State.BLOCK:
                new_state = State.OFF
            case (_, s):
                new_state = s
        GPIO.set_state(self._pin, new_state)
        self._state = state
        return self._state

    def get(self) -> State:
        return self._state
