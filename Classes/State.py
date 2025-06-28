import enum


class State(enum.Enum):
    OFF = 0
    ON = 1
    ERROR = 2
    NO_CHANGE = 3
    BLOCK = 4
