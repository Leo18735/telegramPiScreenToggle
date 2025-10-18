import dataclasses
import typing


@dataclasses.dataclass
class Task:
    temperature: float
    condition: str
    endpoint: str

    @classmethod
    def from_dict(cls, data: dict) -> typing.Self:
        data["temperature"] = float(data.get("temperature"))
        return cls(**data)
