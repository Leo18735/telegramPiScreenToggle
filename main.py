import threading
import time

from Classes.Config.Config import Config
from Classes.Controller.BrightnessController import BrightnessController
from Classes.Controller.FanController import FanController
from Classes.Controller.ScreenController import ScreenController
from Classes.Controller.TemperatureController import TemperatureController
from Classes.Handler.BaseHandler import BaseHandler
from Classes.Handler.ConditionHandler.ConditionHandler import ConditionHandler
from Classes.Handler.FlaskHandler import FlaskHandler
from Classes.Handler.TimeHandler.TimeHandler import TimeHandler


def delayed(handler_class: type[BaseHandler], *args):
    time.sleep(10)
    handler_class(*args).run()


def main():
    config: Config = Config.load_config_file("config.json")

    fan_controller: FanController = FanController(config)
    screen_controller: ScreenController = ScreenController(config)
    temperature_controller: TemperatureController = TemperatureController(config)
    brightness_controller: BrightnessController = BrightnessController(config)

    threading.Thread(target=delayed, args=(TimeHandler, config)).start()
    threading.Thread(target=delayed, args=(ConditionHandler, config)).start()
    FlaskHandler(
        fan_controller,
        screen_controller,
        temperature_controller,
        brightness_controller,
        config
    ).run()


if __name__ == '__main__':
    main()
