import threading
from dotenv import load_dotenv
import os
import sys
import json
import typing
if sys.platform == "win32":
    from Utils import utils

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

    utils.execute = mock_execute


from Classes.Handler.TelegramHandler import TelegramHandler
from Classes.Handler.TemperatureHandler import TemperatureHandler
from Classes.Handler.SocketHandler import SocketHandler
from Classes.Fan.Temperature import Temperature
from Classes.Screen.PiScreen import PiScreen
from Classes.Fan.Fan import Fan


def main():
    with open("configs/temperature.json", "r") as f:
        config_temperature: dict = json.load(f)
    with open("configs/fan.json", "r") as f:
        config_fan: dict = json.load(f)
    with open("configs/temperature_handler.json", "r") as f:
        config_temperature_handler: dict = json.load(f)
    with open("configs/socket_handler.json", "r") as f:
        config_socket_handler: dict = json.load(f)
    load_dotenv(".env")
    token: str = os.getenv("TOKEN")

    temperature: Temperature = Temperature(**config_temperature)
    fan: Fan = Fan(**config_fan)
    pi_screen: PiScreen = PiScreen()

    temperature_handler: TemperatureHandler = TemperatureHandler(temperature, fan, **config_temperature_handler)
    telegram_handler: TelegramHandler = TelegramHandler(temperature, fan, pi_screen, token)
    socket_handler: SocketHandler = SocketHandler(fan, pi_screen, *config_socket_handler)

    threading.Thread(target=temperature_handler.run).start()
    threading.Thread(target=socket_handler.run).start()
    telegram_handler.run()


if __name__ == '__main__':
    main()
