import abc


class StateCommand(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_state(self) -> dict:
        pass
