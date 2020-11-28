from abc import ABC, abstractmethod
from typing import Dict, Optional, Hashable, TypeVar, Generic


class Context:

    def __init__(self, initial_state: "State"):
        self.state = initial_state

    def show(self):
        while self.state is not None:
            self.state.context = self
            input_ = self.state.run()
            self.state = self.state.next(input_)


CTX_T = TypeVar("CTX_T", bound=Context)
Transitions = Dict[Optional[Hashable], Optional["State"]]


class State(ABC, Generic[CTX_T]):

    _context: Optional[CTX_T] = None

    @property
    def context(self) -> CTX_T:
        if self._context is None:
            raise RuntimeError("'menu' is not initialized")

        return self._context

    @context.setter
    def context(self, value: CTX_T) -> None:
        if self._context is not None:
            raise ValueError("'menu' can be configured only once")

        self._context = value

    def next(self, input_: Optional[Hashable]) -> Optional["State"]:
        return self.transitions[input_]

    @property
    @abstractmethod
    def transitions(self) -> Transitions:
        pass

    @abstractmethod
    def run(self) -> Optional[Hashable]:
        pass


