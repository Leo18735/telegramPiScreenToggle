import abc


class Handler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self):
        pass
