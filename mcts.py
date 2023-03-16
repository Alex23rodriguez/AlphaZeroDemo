from numpy import log
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
        return sum(self.expandable_moves) == 0 and len(self.children) > 0

    def select(self):
        return max((child._get_ucb(), child) for child in self.children)[1]

    def _get_ucb(self):
        # ucb formula
        return self.value_sum / self.visit_count + 2 * (log(self.value_sum))

    def expand(self):
        action = choice([i for i, v in enumerate(self.expandable_moves) if v])
        self.expandable_moves[action] = 0
        self.children.append(Node(self.game, self.args, self.state, self, action))
        return self.children[-1]

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
            # 2. Expansion
            if node.children:
                node = node.expand()
            else:
                pass  # TODO backprop
            # 3. Simulation
            node.simulate()
            # 4. Backprop
        # return visit counts
