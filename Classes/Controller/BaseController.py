import abc

from Classes.BaseConfigHolder import BaseConfigHolder, C


class BaseController(BaseConfigHolder[C], abc.ABC):
    @abc.abstractmethod
    def get_state(self):
        pass

    @abc.abstractmethod
    def set_state(self, *_, **__):
        pass
