import socket
import typing
from Classes.Fan.Fan import Fan
from Classes.Handler.Handler import Handler
from Classes.Screen.PiScreen import PiScreen
from Classes.State import State


class SocketHandler(Handler):
    """
    Handles incoming socket connections to control a fan or screen.
    """

    def __init__(self, fan: Fan, pi_screen: PiScreen, ip: str, port: int):
        self._fan = fan
        self._pi_screen = pi_screen
        self._ip = ip
        self._port = port

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._ip, self._port))
        self._socket.listen()

        self._handlers: dict[str, typing.Callable[[State], None]] = {
            "fan": self._fan.set,
            "scr": self._pi_screen.set,
            "err": self._handle_error
        }

    @staticmethod
    def _handle_error(state: State):
        print(f"[ERROR] Unrecognized or invalid input: {state.name}")

    def _handle(self, data: str):
        if len(data) != 4:
            return
        state: State = State.ERROR
        match data[3]:
            case "0":
                state = State.OFF
            case "1":
                state = State.ON
        if state == State.ERROR:
            return
        self._handlers.get(data[:3], self._handle_error)(state)

    def run(self):
        try:
            while True:
                client_sock, address = self._socket.accept()
                with client_sock:
                    data = client_sock.recv(4)
                    if not data:
                        continue
                    self._handle(data.decode("utf-8"))
        finally:
            self._socket.close()
