import abc

import requests

from Classes.BaseConfigHolder import BaseConfigHolder
from Classes.Config.Config import C, Config


class BaseHandler(BaseConfigHolder[C], abc.ABC):
    def __init__(self, config: Config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self._ip: str = self.__get_ip(config.handler.flask_handler.ip)
        self._port: int = config.handler.flask_handler.port

    @staticmethod
    def __get_ip(ip: str) -> str:
        return {
            "0.0.0.0": "127.0.0.1"
        }.get(ip, ip)

    @abc.abstractmethod
    def run(self):
        pass

    def _request(self, endpoint: str) -> requests.Response:
        return requests.get(f"http://{self._ip}:{self._port}/api/v1/{endpoint}")
