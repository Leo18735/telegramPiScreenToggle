from flask_wrapper.FlaskWrapper import FlaskWrapper

from Classes.BaseConfigHolder import BaseConfigHolder
from Classes.Config.HandlerConfigs.FlaskHandlerConfig import FlaskHandlerConfig
from Classes.Controller.BrightnessController import BrightnessController
from Classes.Controller.FanController import FanController
from Classes.Controller.ScreenController import ScreenController
from Classes.Controller.SlideshowController import SlideshowController
from Classes.Controller.TemperatureController import TemperatureController


class FlaskHandler(FlaskWrapper, BaseConfigHolder[FlaskHandlerConfig]):
    _errors = {
        0: ""
    }

    def __init__(self,
                 fan_controller: FanController,
                 screen_controller: ScreenController,
                 temperature_controller: TemperatureController,
                 brightness_controller: BrightnessController,
                 slideshow_controller: SlideshowController,
                 *args, **kwargs):
        BaseConfigHolder.__init__(self, *args, **kwargs)
        FlaskWrapper.__init__(self, "telegramPiScreenToggle", self._config.ip, self._config.port)

        self._fan_controller: FanController = fan_controller
        self._screen_controller: ScreenController = screen_controller
        self._temperature_controller: TemperatureController = temperature_controller
        self._brightness_controller: BrightnessController = brightness_controller
        self._slideshow_controller: SlideshowController = slideshow_controller

    def run(self):
        if self._config.ip not in ["0.0.0.0", "127.0.0.1"]:
            return
        super().run()

    def _add_routes(self):
        @self._app.route("/api/v1/ping")
        def _api_v1_ping():
            return ""

        @self._app.route("/api/v1/fan/set/<value>")
        def _fan_set(value: str):
            try:
                possible_values: list[str] = ["on", "off", "block", "unblock"]
                assert value in possible_values, f"{value} not in {possible_values}"
                self._fan_controller.set_state(value)
                return self._error(0)
            except Exception as e:
                return self._error(-1, str(e))

        @self._app.route("/api/v1/fan/get")
        def _fan_get():
            try:
                state, blocked = self._fan_controller.get_state()
                return self._error(0, data={
                    "state": "on" if state else "off",
                    "mode": "blocked" if blocked else "unblocked"
                })
            except Exception as e:
                return self._error(-1, str(e))

        @self._app.route("/api/v1/screen/set/<value>")
        def _screen_set(value: str):
            try:
                possible_values: list[str] = ["on", "off"]
                assert value in possible_values, f"{value} not in {possible_values}"
                self._screen_controller.set_state(value == "on")
                return self._error(0)
            except Exception as e:
                return self._error(-1, str(e))

        @self._app.route("/api/v1/screen/get")
        def _screen_get():
            try:
                return self._error(0, data={"state": "on" if self._screen_controller.get_state() else "off"})
            except Exception as e:
                return self._error(-1, str(e))

        @self._app.route("/api/v1/brightness/set/<int:value>")
        def _brightness_set(value: int):
            try:
                assert 0 <= value <= 255, f"0 > {value} > 255"
                self._brightness_controller.set_state(value)
                return self._error(0)
            except Exception as e:
                return self._error(-1, str(e))

        @self._app.route("/api/v1/brightness/get")
        def _brightness_get():
            try:
                return self._error(0, data={"state": self._brightness_controller.get_state()})
            except Exception as e:
                return self._error(-1, str(e))

        @self._app.route("/api/v1/temperature/get")
        def _temperature_get():
            try:
                return self._error(0, data={"state": self._temperature_controller.get_state()})
            except Exception as e:
                return self._error(-1, str(e))

        @self._app.route("/api/v1/slideshow/set/<value>")
        def _slideshow_set(value: str, duration: int = 3):
            try:
                if value == "off":
                    self._slideshow_controller.kill_slideshow()
                    return self._error(0)
                possible_configs: list[str] = self._slideshow_controller.get_state()
                assert value in possible_configs, f"{value} not in {possible_configs}"
                self._slideshow_controller.set_state(value, duration)
                return self._error(0)
            except Exception as e:
                return self._error(-1, str(e))

        @self._app.route("/api/v1/slideshow/set/<value>/<int:duration>")
        def _slideshow_set_duration(value: str, duration: int):
            return _slideshow_set(value, duration)

        @self._app.route("/api/v1/slideshow/get")
        def _slideshow_get():
            try:
                return self._error(0, data={"state": self._slideshow_controller.get_state()})
            except Exception as e:
                return self._error(-1, str(e))
