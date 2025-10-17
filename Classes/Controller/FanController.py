from Classes.Controller.BaseGpioController import BaseGpioController


class FanController(BaseGpioController):
    def get_state(self) -> bool:
        return self._state

    def set_state(self, state: str):
        self._set_state(state)
