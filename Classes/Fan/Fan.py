from Classes.State import State
from Classes.Fan.GPIO import GPIO


class Fan:
    def __init__(self, pin: int, *_, **__):
        self._pin: int = pin
        self._state: State = self.set(State.OFF)

    def set(self, state: State) -> State:
        if (hasattr(self, "_state") and state == self._state) or state == state.NO_CHANGE:
            return State.NO_CHANGE
        if state == State.BLOCK:
            GPIO.set_state(self._pin, State.OFF)
        else:
            if hasattr(self, "_state") and self._state == State.BLOCK and state != State.OFF:
                return self._state
            GPIO.set_state(self._pin, state)
        self._state = state
        return self._state
