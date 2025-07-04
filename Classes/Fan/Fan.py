import typing
from Classes.State import State
from Classes.Fan.GPIO import GPIO
import RPi.GPIO
from Classes.StateCommand import StateCommand


class Fan(StateCommand):
    def __init__(self, pin: int, *_, **__):
        self._pin: int = pin
        GPIO.set_state(self._pin, RPi.GPIO.LOW)
        self._state = State.OFF
        self._block: bool = False

    def set(self, state: State, block: typing.Optional[bool] = None):
        if block is not None:
            self._block = block
            return
        if self._block:
            return
        if state == self._state:
            return
        if state not in (State.ON, State.OFF):
            return

        if state == State.ON:
            new_state = RPi.GPIO.HIGH
        elif state == State.OFF:
            new_state = RPi.GPIO.LOW
        else:
            raise Exception(f"Unknown state {state.name}")
        print(f"Set fan {new_state}")
        self._state = state
        GPIO.set_state(self._pin, new_state)

    def get_text(self) -> str:
        return f"\tState: {self._state.name}\n\tBlock: {'True' if self._block else 'False'}"
