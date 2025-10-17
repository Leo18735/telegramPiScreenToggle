import abc
import RPi.GPIO

from Classes.Controller.BaseController import BaseController


class BaseGpioController(BaseController, abc.ABC):
    def __init__(self, pin: int):
        self._pin: int = pin
        self._state: bool = False
        self._set_state(False)

    def _set_state(self, state: bool):
        self._state = state
        RPi.GPIO.setwarnings(False)
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(self._pin, RPi.GPIO.OUT)
        RPi.GPIO.output(self._pin, RPi.GPIO.HIGH if state else RPi.GPIO.LOW)
