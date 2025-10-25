import glob
import os
import threading
import queue
import psutil
import subprocess
from Classes.Config.ControllerConfigs.SlideshowControllerConfig import SlideshowControllerConfig
from Classes.Controller.BaseExecutionController import BaseExecutionController


class SlideshowController(BaseExecutionController[SlideshowControllerConfig]):
    def get_state(self):
        return [
            os.path.splitext(os.path.basename(x))[0]
            for x in
            glob.glob(f"{os.path.join(self._config.slideshow_path, self._config.configs_path)}/*.json")
        ]

    def kill_slideshow(self):
        args: list[str] = ([self._config.python_path, self._config.main_path] +
                           [x for x in self._config.args if not (x.startswith("#") and x.endswith("#"))])
        for process in psutil.process_iter():
            try:
                if process.cwd() == self._config.slideshow_path and all(x in process.cmdline() for x in args):
                    process.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def __start_slideshow(self, config_name: str, duration: int, communication_queue: queue.Queue[str]):
        communication_queue.put(self._execute_handle_result(
            f"{self._config.python_path} {self._config.main_path} {' '.join(self._config.args)}"
            .replace("#CONFIG_NAME#", config_name)
            .replace("#DURATION#", str(duration)),
            self._config.slideshow_path
        ))

    @staticmethod
    def _execute_handle_result(cmd: str, cwd: str) -> str:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=cwd
        )

        all_lines: list[str] = []
        for line in process.stdout.readlines():
            if "started" in line.lower():
                return ""
            all_lines.append(line)
        return "".join(all_lines)


    def set_state(self, state: str, duration: int):
        self.kill_slideshow()
        communication_queue: queue.Queue[str] = queue.Queue()
        threading.Thread(
            target=self.__start_slideshow,
            args=(state, duration, communication_queue),
            daemon=True
        ).start()
        result = communication_queue.get()
        if not result:
            return
        raise Exception(result)
