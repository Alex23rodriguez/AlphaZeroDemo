# flake8: noqa

# Monte Carlo tree search implementation

from abc import ABCMeta, abstractmethod
from math import log


class Node(ABCMeta):
    def __init__(self, state, w: int, n: int, parent: "Node" = None) -> None:
        self.state = state
        self.w = w
        self.n = n
        self.children = []
        self.parent = parent

    @abstractmethod
    def _try_expand(self):
        """
        Try to expand into a new node.
        Retuns the new node if successful, or None if unsuccessful.
        """
        pass

    def expand(self) -> "Node" | None:
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
        if c := self.expand():
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


###
def simulate(root: "Node", rounds=1000):
    # 1. Selection
    root.expand()


### 1. Selection
