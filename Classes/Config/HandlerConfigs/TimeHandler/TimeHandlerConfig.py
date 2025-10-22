import dataclasses

from Classes.Config.BaseConfig import BaseConfig
from Classes.Config.HandlerConfigs.TimeHandler.Task import Task


@dataclasses.dataclass
class TimeHandlerConfig(BaseConfig):
    tasks: list[Task] = None
    interval: int = None

    @staticmethod
    def _custom_tasks(data: list[dict]) -> list[Task]:
        return [Task().load_config(x) for x in data]
