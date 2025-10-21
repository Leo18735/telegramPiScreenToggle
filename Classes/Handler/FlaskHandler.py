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
        0: "",
        1: "value not in ['on', 'off']",
        2: "value > 255 | < 0",
        3: "value not in ['on', 'off', 'block', 'unblock']",
        4: ""
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
            if value not in ["on", "off", "block", "unblock"]:
                return self._error(3)
            try:
                self._fan_controller.set_state(value)
            except Exception as e:
                return self._error(-1, str(e))
            return self._error(0)

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
            if value not in ["on", "off"]:
                return self._error(1)
            try:
                self._screen_controller.set_state(value == "on")
            except Exception as e:
                return self._error(-1, str(e))
            return self._error(0)

        @self._app.route("/api/v1/screen/get")
        def _screen_get():
            try:
                return self._error(0, data={"state": "on" if self._screen_controller.get_state() else "off"})
            except Exception as e:
                return self._error(-1, str(e))

        @self._app.route("/api/v1/brightness/set/<int:value>")
        def _brightness_set(value: int):
            if value > 255 or value < 0:
                return self._error(2)
            try:
                self._brightness_controller.set_state(value)
            except Exception as e:
                return self._error(-1, str(e))
            return self._error(0)

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
        def _slideshow_set(value: str):
            available_configs: list[str] = self._slideshow_controller.get_state()
            if value not in available_configs:
                return self._error(4, f"{value} does not exist. "
                                      f"Available: {' ,'.join(available_configs)}")
            try:
                self._slideshow_controller.set_state(value)
            except Exception as e:
                return self._error(-1, str(e))
            return self._error(0)

        @self._app.route("/api/v1/slideshow/get")
        def _slideshow_get():
            try:
                return self._error(0, data={"state": self._slideshow_controller.get_state()})
            except Exception as e:
                return self._error(-1, str(e))
