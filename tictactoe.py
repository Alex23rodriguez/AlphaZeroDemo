# flake8: noqa
import numpy as np
from game import Game, Moves, State


class TicTacToe(Game):
    def __init__(self, size=3):
        self.size = size
        self.action_size = self.size * self.size

    def get_initial_state(self) -> State:
        return np.zeros((self.size, self.size), np.int8)

    def get_valid_moves(self, state: State) -> Moves:
        return (state.reshape(-1) == 0).astype(np.uint8)

    def get_next_state(self, state: State, action: int, player: int) -> State:
        state.reshape(-1)[action] = player
        return state

    def _check_win(self, state: State, action: int) -> bool:
        row = action // self.size
        col = action % self.size
        goal = self.size * state.reshape(-1)[action]
        return (
            state[row, :].sum() == goal
            or state[:, col].sum() == goal
            or state.trace() == goal
            or np.flip(state, axis=0).trace() == goal
        )

    def get_value_and_terminated(
        self, state: State, action: int | None
    ) -> tuple[int, bool]:
        if action is not None and self._check_win(state, action):
            return 1, True
        if state.all():  # check if all elements are non-zero
            return 0, True
        return 0, False

    def get_opponent(self, player: int) -> int:
        return -player

    def get_opponent_value(self, value: int) -> int:
        return -value

    def change_perspective(self, state: State, player: int) -> State:
        return state * player
