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
        pass

    @abstractmethod
    def get_next_state(self, state: State, action: int, player: int) -> State:
        pass

    @abstractmethod
    def _check_win(self, state: State, action: int) -> bool:
        pass

    @abstractmethod
    def get_value_and_terminated(self, state: State, action: int) -> tuple[int, bool]:
        pass

    @abstractmethod
    def get_opponent(self, player: int) -> int:
        pass
