# flake8: noqa

# Monte Carlo tree search implementation

from abc import ABC, abstractmethod
from math import log
from random import choice


class Node(ABC):
    @abstractmethod
    @staticmethod
    def get_initial_state():
        pass

    def __init__(self, state, parent: "Node" = None) -> None:
        self.state = state
        self.w = 0
        self.n = 0
        self.children = []
        self.parent = parent

    @abstractmethod
    def _try_expand(self):
        """
        Try to expand into a new node.
        Retuns the new node if successful, or None if unsuccessful.
        """
        pass

    def _expand(self) -> "Node" | None:
        if n := self.try_expand():
            self.children.append(n)
        return n

    def update(self, won: bool) -> None:
        self.n += 1
        self.w += won
        if self.parent:
            self.parent.update()
        else:
            global N
            N += 1

    def select_and_expand(self) -> "Node":
        # check if node creates a child
        if c := self._expand():
            return c

        # TODO: what happens when all nodes are explored?
        if len(self.children) == 0:
            return self

        if len(self.children) == 1:
            return self.children[0]

        return max((c._ucb(), c) for c in self.children)[1]

    def _ucb(self) -> float:
        global C, N
        return self.w / self.n + C * (log(N) / self.n) ** 0.5

    def play(self) -> int:
        """Play until the end."""
        state = self.state
        while state:
            moves = self.get_next_moves(state)
            if not moves:
                return self.did_win(state)
            state = choice(moves)
            curr_p = not curr_p

    @abstractmethod
    def get_next_moves(self, state) -> list:
        """
        Generate the next possible moves from the given state.
        Note that because of the way the 'update' method is defined, next_moves should be from the same player!
        Therefore, this has to generate every possible move for the opponent, and the move after that.
        """
        pass

    @abstractmethod
    def _did_win(self, state):
        """Given a state, returns 1 if starting player won, -1 if lost, 0 if draw."""
        pass


###
def simulate(root: "Node", rounds=1000):
    global N
    for _ in range(rounds):
        N += 1
        # 1. Selection and 2. Expansion
        n = root.select_and_expand()

        # 3. Random play
        w = n.play()

        # backpropagation
        n.update(w == 1)


### 1. Selection
