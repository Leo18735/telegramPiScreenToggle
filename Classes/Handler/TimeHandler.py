import dataclasses
import time
from datetime import datetime
from Classes.Handler.BaseHandler import BaseHandler

@dataclasses.dataclass
class Task:
    time: datetime
    endpoint: str

    @classmethod
    def from_dict(cls, data: dict):
        hour, minute = data.get("time").split(":")
        data["time"] = datetime(year=1970, month=1, day=1, hour=int(hour), minute=int(minute))
        return cls(**data)


class TimeHandler(BaseHandler):
    def __init__(self, tasks: dict):
        self._old_time: datetime = datetime.now()
        self._tasks: list[Task] = [Task.from_dict(task) for task in tasks]

    def run(self):
        time.sleep(10)
        while True:
            c_time: datetime = datetime.now()
            for task in self._tasks:
                if self._old_time < task.time.replace(year=c_time.year, month=c_time.month, day=c_time.day) <= c_time:
                    self._request(task.endpoint)
            self._old_time = c_time
            time.sleep(60)
