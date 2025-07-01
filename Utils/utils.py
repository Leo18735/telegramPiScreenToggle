import subprocess


def execute(cmd: str) -> tuple[str, str, int]:
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    code = process.returncode
    return stdout, stderr, code


import sys
import typing
if sys.platform == "win32":
    def mock_execute(cmd: str) -> tuple[str, str, int]:
        result: typing.Optional[str] = None
        if cmd == "vcgencmd measure_temp":
            result = "temp=50.0'C"
        if cmd == "XDG_RUNTIME_DIR=/run/user/1000 wlr-randr --output DSI-1":
            result = "DSI enabled=yes"
        if cmd == "XDG_RUNTIME_DIR=/run/user/1000 wlr-randr --output DSI-1 --on":
            result = ""
        if cmd == "XDG_RUNTIME_DIR=/run/user/1000 wlr-randr --output DSI-1 --off":
            result = ""

        if result is None:
            raise Exception(cmd)
        return result, "", 0

    execute = mock_execute
