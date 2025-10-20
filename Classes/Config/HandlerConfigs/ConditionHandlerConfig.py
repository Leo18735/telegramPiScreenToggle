import dataclasses

from Classes.Config.BaseConfig import BaseConfig
from Classes.Handler.ConditionHandler.Task import Task


@dataclasses.dataclass
class ConditionHandlerConfig(BaseConfig):
    tasks: list[Task] = None

    @staticmethod
    def _custom_tasks(data: list[dict]) -> list[Task]:
        return [Task.from_dict(x) for x in data]
