import json

from Classes.Controller.BrightnessController import BrightnessController
from Classes.Controller.FanController import FanController
from Classes.Controller.ScreenController import ScreenController
from Classes.Controller.TemperatureController import TemperatureController
from Classes.Handler.FlaskHandler import FlaskHandler


def main():
    with open("config.json") as f:
        config: dict = json.load(f)

    fan_controller: FanController = FanController(**config.get("fan_controller"))
    screen_controller: ScreenController = ScreenController()
    temperature_controller: TemperatureController = TemperatureController()
    brightness_controller: BrightnessController = BrightnessController()

    FlaskHandler(
        fan_controller,
        screen_controller,
        temperature_controller,
        brightness_controller,
        "app",
        "0.0.0.0",
        5000
    ).run()


if __name__ == '__main__':
    main()
