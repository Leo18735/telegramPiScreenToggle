import abc
import subprocess

from Classes.Controller.BaseController import BaseController, C


class BaseExecutionController(BaseController[C], abc.ABC):
    @staticmethod
    def _execute(cmd: str, cwd: str = None) -> tuple[str, str, int]:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd
        )
        stdout, stderr = process.communicate()
        code = process.returncode
        return stdout, stderr, code
