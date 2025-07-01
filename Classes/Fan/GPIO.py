import sys
from unittest.mock import MagicMock

from Classes.State.StateOut import StateOut

if sys.platform == "win32":
    sys.modules['RPi'] = MagicMock()
    sys.modules['RPi.GPIO'] = MagicMock()
import RPi.GPIO
from Classes.State.StateIn import StateIn


class GPIO:
    @staticmethod
    def set_state(pin: int, state: StateIn) -> StateOut:
        RPi.GPIO.setwarnings(False)
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(pin, RPi.GPIO.OUT)
        if state == StateIn.ON:
            new_state = RPi.GPIO.HIGH
            return_state = StateOut.ON
        elif state == StateIn.OFF:
            new_state = RPi.GPIO.LOW
            return_state = StateOut.OFF
        else:
            raise Exception(f"Unknown state {state.name}")
        RPi.GPIO.output(pin, new_state)
        return return_state
