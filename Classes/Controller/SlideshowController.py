import glob
import threading
import os
import psutil

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
                           [x for x in self._config.args if not (x.startswith("#")  and x.endswith("#"))])
        for process in psutil.process_iter():
            try:
                if process.cwd() == self._config.slideshow_path and all(x in process.cmdline() for x in args):
                    process.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def __start_slideshow(self, config_name: str):
        self._execute(f"{self._config.python_path} {self._config.main_path} {' '.join(self._config.args)}"
                      .replace("#CONFIG_NAME#", config_name),
                      cwd=self._config.slideshow_path)

    def set_state(self, state: str):
        self.kill_slideshow()
        threading.Thread(
            target=self.__start_slideshow,
            args=(state, ),
            daemon=True
        ).start()
