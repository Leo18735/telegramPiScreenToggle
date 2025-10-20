import abc

import RPi.GPIO
from Classes.Controller.BaseController import BaseController, C


class BaseGpioController(BaseController[C], abc.ABC):
    @staticmethod
    def _set_state(state: bool, pin: int):
        RPi.GPIO.setwarnings(False)
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(pin, RPi.GPIO.OUT)
        RPi.GPIO.output(pin, RPi.GPIO.HIGH if state else RPi.GPIO.LOW)
