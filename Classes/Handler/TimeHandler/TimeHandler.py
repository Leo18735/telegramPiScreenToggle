import time
from datetime import datetime

from Classes.Config.HandlerConfigs.TimeHandlerConfig import TimeHandlerConfig
from Classes.Handler.BaseHandler import BaseHandler


class TimeHandler(BaseHandler[TimeHandlerConfig]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_time: datetime = datetime.now()

    def run(self):
        while True:
            c_time: datetime = datetime.now()
            for task in self._config.tasks:
                if self._old_time < task.time.replace(year=c_time.year, month=c_time.month, day=c_time.day) <= c_time:
                    self._request(task.endpoint)
            self._old_time = c_time
            time.sleep(60)
