import abc
import subprocess
from Classes.Controller.BaseController import BaseController


class BaseExecutionController(BaseController, abc.ABC):
    @staticmethod
    def _decode(std: bytes) -> str:
        return std.decode(encoding="utf-8", errors="ignore")

    @classmethod
    def _execute(cls, command: str) -> tuple[str, str, int]:
        process: subprocess.Popen = subprocess.Popen(
            command.split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        return cls._decode(stdout), cls._decode(stderr), process.returncode
