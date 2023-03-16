import numpy as np
from game import Game, State
from random import choice


class Node:
    def __init__(
        self,
        game: Game,
        args,
        state: State,
        parent: "Node" | None = None,
        action_taken: int | None = None,
    ):
        self.game = game
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.value_sum = 0  # w
        self.visit_count = 0  # n
        self.children = []
        self.expandable_moves = game.get_valid_moves(state)

    def is_fully_expanded(self):
        return np.sum(self.expandable_moves) == 0 and len(self.children) > 0

    def select(self) -> "Node":
        return max((self._get_ucb(child), child) for child in self.children)[1]

    def _get_ucb(self, child: "Node"):
        # ucb formula
        # we want it to be from the perspective of the parent (opponent)
        # so we pick the child with the lowest q value
        # therefore, 1 - child's q value
        q_value = 1 - child.value_sum / child.visit_count
        return q_value + self.args["C"] * np.sqrt(
            np.log(self.value_sum) / child.value_sum
        )

    def expand(self) -> "Node":
        action = choice(self.expandable_moves.nonzero()[0])
        # action = choice([i for i, v in enumerate(self.expandable_moves) if v])
        # equivalent to the following code
        # action = np.random.choice(np.where(self.expandable_moves == 1)[0])
        self.expandable_moves[action] = 0

        # we use 1 as player for all nodes!
        # all nodes will play from "first person perspective"
        # instead, opponents are handled by the MCTS by changing the state of our child
        # also makes code valid for 1 player games
        # see video at 1:19:00
        child_state = self.state.copy()
        child_state = self.game.get_next_state(child_state, action, 1)
        child_state = self.game.change_perspective(child_state, player=-1)

        child = Node(self.game, self.args, child_state, self, action)
        self.children.append(child)
        return child

    def simulate(self):
        if self.action_taken:
            v, t = self.game.get_value_and_terminated(self.state, self.action_taken)


class MCTS:
    def __init__(self, game: Game, args):
        self.game = game
        self.args = args

    def search(self, state):
        root = Node(self.game, self.args, state)

        for round in range(self.args["num_searches"]):
            node = root
            # 1. Selection
            while node.is_fully_expanded():
                node = node.select()

            value, is_terminal = self.game.get_value_and_terminated(
                node.state, node.action_taken
            )
            value = self.game.get_opponent_value(value)

            if not is_terminal:
                # 2. Expansion
                node = node.expand()

                # 3. Simulation
                node.simulate()

            # 4. Backprop
        # return visit counts
