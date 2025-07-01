import sys
from unittest.mock import MagicMock
if sys.platform == "win32":
    sys.modules['RPi'] = MagicMock()
    sys.modules['RPi.GPIO'] = MagicMock()
import RPi.GPIO
from Classes.State import State


class GPIO:
    @staticmethod
    def set_state(pin: int, state: State):
        RPi.GPIO.setwarnings(False)
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(pin, RPi.GPIO.OUT)
        RPi.GPIO.output(pin, RPi.GPIO.HIGH if state == State.ON else RPi.GPIO.LOW)
