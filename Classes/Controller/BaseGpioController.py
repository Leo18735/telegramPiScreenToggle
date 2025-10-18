import abc

import RPi.GPIO

from Classes.Controller.BaseController import BaseController
import threading


class BaseGpioController(BaseController, abc.ABC):
    def __init__(self, pin: int):
        self._pin: int = pin
        self._state: bool = False
        self._blocked: bool = False
        self._set_state("off")

        self._lock: threading.Lock = threading.Lock()

    def _set_state(self, state: str):
        self._lock.acquire()
        if state not in ["unblock", "block"] and self._blocked:
            self._lock.release()
            raise Exception("Fan is blocked")
        elif state == "block":
            self._blocked = True
            self._lock.release()
            return
        elif state == "unblock":
            self._blocked = False
            self._lock.release()
            return
        new_state = state == "on"
        self._state = new_state
        RPi.GPIO.setwarnings(False)
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(self._pin, RPi.GPIO.OUT)
        RPi.GPIO.output(self._pin, RPi.GPIO.HIGH if self._state else RPi.GPIO.LOW)
        self._lock.release()
