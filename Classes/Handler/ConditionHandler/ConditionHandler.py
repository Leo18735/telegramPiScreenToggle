import time

from Classes.Config.HandlerConfigs.ConditionHandlerConfig import ConditionHandlerConfig
from Classes.Handler.BaseHandler import BaseHandler


class ConditionHandler(BaseHandler[ConditionHandlerConfig]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        while True:
            for task in self._config.tasks:
                task.execute(self._request)
            time.sleep(self._config.interval)
