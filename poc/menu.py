from abc import ABC, abstractmethod
from typing import Dict, Optional, Hashable, TypeVar, Generic


class Menu:

    def __init__(self, initial_state: "State"):
        self.state = initial_state

    def show(self):
        while self.state is not None:
            self.state.menu = self
            input_ = self.state.run()
            self.state = self.state.next(input_)


MENU_T = TypeVar("MENU_T", bound=Menu)
Transitions = Dict[Optional[Hashable], Optional["State"]]


class State(ABC, Generic[MENU_T]):

    _menu: Optional[MENU_T] = None

    @property
    def menu(self) -> MENU_T:
        if self._menu is None:
            raise RuntimeError("'menu' is not initialized")

        return self._menu

    @menu.setter
    def menu(self, value: MENU_T) -> None:
        if self._menu is not None:
            raise ValueError("'menu' can be configured only once")

        self._menu = value

    def next(self, input_: Optional[Hashable]) -> Optional["State"]:
        return self.transitions[input_]

    @property
    @abstractmethod
    def transitions(self) -> Transitions:
        pass

    @abstractmethod
    def run(self) -> Optional[Hashable]:
        pass


