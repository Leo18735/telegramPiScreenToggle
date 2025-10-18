import json
import threading
import time

from Classes.Controller.BrightnessController import BrightnessController
from Classes.Controller.FanController import FanController
from Classes.Controller.ScreenController import ScreenController
from Classes.Controller.TemperatureController import TemperatureController
from Classes.Handler.BaseHandler import BaseHandler
from Classes.Handler.FlaskHandler import FlaskHandler
from Classes.Handler.TemperatureHandler import TemperatureHandler
from Classes.Handler.TimeHandler import TimeHandler


def delayed(handler_class: type[BaseHandler], *args, **kwargs):
    time.sleep(10)
    handler_class(*args, **kwargs).run()


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
    threading.Thread(target=delayed, args=(TimeHandler,), kwargs=config_handler.get("time_handler")).start()
    threading.Thread(target=delayed, args=(TemperatureHandler,),
                     kwargs=config_handler.get("temperature_handler")).start()
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
