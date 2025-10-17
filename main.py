import json
import threading
import time
import typing

from Classes.Controller.BrightnessController import BrightnessController
from Classes.Controller.FanController import FanController
from Classes.Controller.ScreenController import ScreenController
from Classes.Controller.TemperatureController import TemperatureController
from Classes.Handler.BaseHandler import BaseHandler
from Classes.Handler.FlaskHandler import FlaskHandler
from Classes.Handler.TemperatureHandler import TemperatureHandler
from Classes.Handler.TimeHandler import TimeHandler


def delayed(method: typing.Callable, *args, **kwargs):
    time.sleep(10)
    method(*args, **kwargs)


def main():
    with open("config.json") as f:
        config: dict = json.load(f)

    config_controller: dict = config.get("controller")
    fan_controller: FanController = FanController(**config_controller.get("fan_controller"))
    screen_controller: ScreenController = ScreenController()
    temperature_controller: TemperatureController = TemperatureController()
    brightness_controller: BrightnessController = BrightnessController()

    config_handler: dict = config.get("handler")
    BaseHandler.port = config_handler.get("flask_handler").get("port")
    threading.Thread(target=lambda: delayed(TimeHandler(**config_handler.get("time_handler")).run)).start()
    threading.Thread(target=lambda: delayed(TemperatureHandler(**config_handler.get("temperature_handler")).run)).start()
    FlaskHandler(
        fan_controller,
        screen_controller,
        temperature_controller,
        brightness_controller,
        "app",
        **config_handler.get("flask_handler")
    ).run()


if __name__ == '__main__':
    main()
