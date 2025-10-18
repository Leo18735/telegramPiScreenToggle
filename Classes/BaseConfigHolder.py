import abc
from typing import Generic

from Classes.Config.Config import C
from Classes.Config.Config import Config


class BaseConfigHolder(Generic[C], abc.ABC):
    def __init__(self, config: Config, *args, **kwargs):
        self._config: C = config.get_correct_config(self.__class__.__name__)
        super().__init__(*args, **kwargs)
