from Classes.State import State
from Classes.Fan.GPIO import GPIO


class Fan:
    def __init__(self, pin: int, *_, **__):
        self._pin: int = pin
        self._state: State = State.ERROR
        self._state = self.set(State.OFF)

    def set(self, state: State) -> State:
        if self._state == State.BLOCK and state != State.OFF:
            return self._state
        if state == self._state or state == state.NO_CHANGE:
            return State.NO_CHANGE
        if state == State.BLOCK:
            GPIO.set_state(self._pin, State.OFF)
        else:
            GPIO.set_state(self._pin, state)
        self._state = state
        return self._state

    def get(self) -> State:
        return self._state
