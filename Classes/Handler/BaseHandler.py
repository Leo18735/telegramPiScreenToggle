import abc

import requests

from Classes.BaseConfigHolder import BaseConfigHolder
from Classes.Config.Config import C, Config


class BaseHandler(BaseConfigHolder[C], abc.ABC):
    def __init__(self, config: Config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self._port: int = config.handler.flask_handler.port

    @abc.abstractmethod
    def run(self):
        pass

    def _request(self, endpoint: str) -> requests.Response:
        return requests.get(f"http://127.0.0.1:{self._port}/api/v1/{endpoint}")
