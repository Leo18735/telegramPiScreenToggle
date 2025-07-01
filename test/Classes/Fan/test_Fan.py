import pytest
from Classes.State import State
from Classes.Fan.Fan import Fan


class TestFan:
    def setup_method(self):
        self._fan = Fan(0)

    @pytest.mark.parametrize("current_state,new_state,expected_return_state,expected_new_state", [
        (State.OFF, State.OFF, State.NO_CHANGE, State.OFF),
        (State.OFF, State.ON, State.ON, State.ON),
        (State.OFF, State.ERROR, State.NO_CHANGE, State.OFF),
        (State.OFF, State.NO_CHANGE, State.NO_CHANGE, State.OFF),
        (State.OFF, State.BLOCK, State.BLOCK, State.BLOCK),

        (State.ON, State.OFF, State.OFF, State.OFF),
        (State.ON, State.ON, State.NO_CHANGE, State.ON),
        (State.ON, State.ERROR, State.NO_CHANGE, State.ON),
        (State.ON, State.NO_CHANGE, State.NO_CHANGE, State.ON),
        (State.ON, State.BLOCK, State.BLOCK, State.BLOCK),

        (State.BLOCK, State.OFF, State.OFF, State.OFF),
        (State.BLOCK, State.ON, State.BLOCK, State.BLOCK),
        (State.BLOCK, State.ERROR, State.NO_CHANGE, State.BLOCK),
        (State.BLOCK, State.NO_CHANGE, State.NO_CHANGE, State.BLOCK),
        (State.BLOCK, State.BLOCK, State.NO_CHANGE, State.BLOCK),
    ])
    def test_set(self, current_state: State, new_state: State, expected_return_state, expected_new_state: State):
        self._fan._state = current_state
        return_state: State = self._fan.set(new_state)

        assert expected_return_state == return_state
        assert expected_new_state == self._fan._state
