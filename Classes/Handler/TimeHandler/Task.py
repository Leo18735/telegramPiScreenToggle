import dataclasses
from datetime import datetime


@dataclasses.dataclass
class Task:
    time: datetime
    endpoint: str

    @classmethod
    def from_dict(cls, data: dict):
        hour, minute = data.get("time").split(":")
        data["time"] = datetime(year=1970, month=1, day=1, hour=int(hour), minute=int(minute), second=0)
        return cls(**data)
