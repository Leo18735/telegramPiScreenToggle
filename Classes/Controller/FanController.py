import threading

from Classes.Config.ControllerConfigs.FanControllerConfig import FanControllerConfig
from Classes.Controller.BaseGpioController import BaseGpioController


class FanController(BaseGpioController[FanControllerConfig]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state: bool = False
        self._blocked: bool = False
        self._set_state(False, self._config.pin)

        self._lock: threading.Lock = threading.Lock()

    def get_state(self) -> bool:
        return self._state

    def set_state(self, state: str):
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
        self._set_state(self._state, self._config.pin)
        self._lock.release()
