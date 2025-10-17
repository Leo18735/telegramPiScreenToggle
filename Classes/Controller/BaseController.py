import abc


class BaseController(abc.ABC):
    @abc.abstractmethod
    def get_state(self):
        pass

    @abc.abstractmethod
    def set_state(self, *_, **__):
        pass
