import abc
import subprocess

from Classes.Controller.BaseController import BaseController


class BaseExecutionController(BaseController, abc.ABC):
    @staticmethod
    def _execute(cmd: str) -> tuple[str, str, int]:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        code = process.returncode
        return stdout, stderr, code
