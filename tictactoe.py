# flake8: noqa

# TicTacToe implementation for abstract Node

from random import choice
from .mcts import Node


class TicTacToe(Node):
    @staticmethod
    def get_initial_state():
        return [0] * 9

    def _try_expand(self):
        moves = self.get_next_moves(self.state)
        if not moves:
            return
        return TicTacToe(choice(moves), self)

    def get_next_moves(self, state):
        ans = []
        for i, v in enumerate(state):
            if v == 0:
                state[i] = -1
                for j, v2 in enumerate(state):
                    if v2 == 0:
                        state[j] = 1
                        ans.append(state.copy())
                        state[j] = 0
                state[i] = 0
        return ans
