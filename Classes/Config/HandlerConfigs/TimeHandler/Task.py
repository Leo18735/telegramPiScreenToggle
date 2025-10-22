import dataclasses
from datetime import datetime

from Classes.Config.BaseConfig import BaseConfig


@dataclasses.dataclass
class Task(BaseConfig):
    time: datetime = None
    endpoint: str = None

    @staticmethod
    def _custom_time(data: str) -> datetime:
        hour, minute = data.split(":")
        return datetime(year=1970, month=1, day=1, hour=int(hour), minute=int(minute), second=0)
