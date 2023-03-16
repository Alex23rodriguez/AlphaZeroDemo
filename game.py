from abc import ABC, abstractmethod
from typing import Any, Tuple
from nptyping import Int8, NDArray, Shape, UInt8


State = NDArray[Any, Int8]
Moves = NDArray[Shape["Size"], Int8]


class Game(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_initial_state(self) -> State:
        pass

    @abstractmethod
    def get_valid_moves(self, state: State) -> Moves:
        # an array of size action_space with
        # zeros for impossible moves and 1 for possible moves
        pass

    @abstractmethod
    def get_next_state(self, state: State, action: int, player: int) -> State:
        pass

    @abstractmethod
    def _check_win(self, state: State, action: int) -> bool:
        pass

    @abstractmethod
    def get_value_and_terminated(
        self, state: State, action: int | None
    ) -> tuple[int, bool]:
        # action should only be None for root node (at beginning of search)
        pass

    @abstractmethod
    def get_opponent(self, player: int) -> int:
        pass

    @abstractmethod
    def get_opponent_value(self, value: int) -> int:
        pass

    @abstractmethod
    def change_perspective(self, state: State, player: int) -> State:
        pass
