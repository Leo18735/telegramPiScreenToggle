import json
import socket
import typing
from Classes.Fan.Fan import Fan
from Classes.Fan.Temperature import Temperature
from Classes.Handler.Handler import Handler
from Classes.Screen.PiScreen import PiScreen
from Classes.State import State


class SocketHandler(Handler):
    """
    Handles incoming socket connections to control a fan or screen.
    """

    def __init__(self, fan: Fan, pi_screen: PiScreen, temperature: Temperature, ip: str, port: int):
        self._fan: Fan = fan
        self._pi_screen: PiScreen = pi_screen
        self._temperature: Temperature = temperature
        self._ip: str = ip
        self._port: int = port

        self._socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._ip, self._port))
        self._socket.listen()

        self._handlers: dict[str, typing.Callable[[State], None]] = {
            "fan": self._fan.set,
            "scr": self._pi_screen.set,
            "sta": self._status_handler,
            "err": self._handle_error
        }

    def _status_handler(self, *_, **__) -> str:
        return json.dumps({"fan": self._fan.get_state(), "screen": self._pi_screen.get_state(), "temp": self._temperature.get_state})

    @staticmethod
    def _handle_error(state: State, *_, **__):
        raise Exception(f"[ERROR] Unrecognized or invalid input: {state.name}")

    def _handle(self, data: str) -> typing.Optional[str]:
        if len(data) != 4:
            return None
        args: list[State | bool] = []
        match data[:3], data[3]:
            case (s, "0") if s in ["fan", "scr"]:
                args.append(State.OFF)
            case (s, "1") if s in ["fan", "scr"]:
                args.append(State.ON)
            case ("fan", "2"):
                args += [State.OFF, True]
            case ("fan", "3"):
                args += [State.OFF, False]
            case ("sta", _):
                pass
            case s:
                raise Exception(f"Unknown state {s.name}")
        return self._handlers.get(data[:3], self._handle_error)(*args)

    def run(self):
        try:
            while True:
                client_sock, address = self._socket.accept()
                with client_sock:
                    try:
                        data = client_sock.recv(4)
                        if not data:
                            continue
                        result: typing.Optional[str] = self._handle(data.decode("utf-8"))
                        if result:
                            client_sock.send(result.encode(encoding="utf-8"))
                    except Exception as e:
                        print(f"Exception: {e}")
        finally:
            self._socket.close()
