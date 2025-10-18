import abc
import typing

import requests


class BaseHandler(abc.ABC):
    port: typing.Optional[int] = None

    def __init__(self, *_, **__):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    def _request(self, endpoint: str) -> requests.Response:
        return requests.get(f"http://127.0.0.1:{self.port}/api/v1/{endpoint}")
