# flake8: noqa
import numpy as np


class TicTacToe:
    def __init__(self, size=3):
        self.size = size
        self.action_space = self.size * self.size

    def get_initial_state(self):
        return np.zeros((self.size, self.size), np.int8)

    def get_valid_moves(self, state):
        return (state.reshape(-1) == 0).astype(np.uint8)

    def get_next_state(self, state, action, player):
        state.reshape(-1)[action] = player
        return state

    def _check_win(self, state, action):
        row = action // self.size
        col = action % self.size
        goal = self.size * state.reshape(-1)[action]
        return (
            state[row, :].sum() == goal
            or state[:, col].sum() == goal
            or state.trace() == goal
            or np.flip(state, axis=0).trace() == goal
        )

    def get_value_and_terminated(self, state, action):
        if self._check_win(state, action):
            return 1, True
        if state.all():  # check if all elements are non-zero
            return 0, True
        return 0, False

    def get_opponent(self, player):
        return -player
