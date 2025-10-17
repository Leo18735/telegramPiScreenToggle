import abc
import RPi.GPIO

from Classes.Controller.BaseController import BaseController


class BaseGpioController(BaseController, abc.ABC):
    def __init__(self, pin: int):
        self._pin: int = pin
        self._state: bool = False
        self._blocked: bool = False
        self._set_state("off")

    def _set_state(self, state: str):
        if state != "unblock" and self._blocked:
            raise Exception("Fan is blocked")
        elif state == "block":
            self._blocked = True
            return
        elif state == "unblock":
            self._blocked = False
            return
        new_state = state == "on"
        self._state = new_state
        RPi.GPIO.setwarnings(False)
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(self._pin, RPi.GPIO.OUT)
        RPi.GPIO.output(self._pin, RPi.GPIO.HIGH if self._state else RPi.GPIO.LOW)
