import abc


class StateCommand(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_text(self) -> str:
        pass
