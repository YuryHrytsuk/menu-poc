from typing import Optional, Hashable

import inquirer

from poc.menu import State, Menu, Transitions


class ListActionsState(State[Menu]):

    @property
    def transitions(self) -> Transitions:
        return {
            "Sub Menu": SubMenuState(ListSubActionsState()),
            "Noop action": NoopActionState(),
            "Exit": None
        }

    def run(self) -> Optional[Hashable]:
        choose_action_q = inquirer.List(
            "action",
            message="Choose action:",
            choices=list(self.transitions.keys()),
        )
        answers = inquirer.prompt([choose_action_q])
        return answers[choose_action_q.name]


class NoopActionState(State[Menu]):

    @property
    def transitions(self) -> Transitions:
        return {
            None: ListActionsState()
        }

    def run(self) -> Optional[Hashable]:
        print("Do nothing")
        return None


class SubMenuState(Menu, State[Menu]):

    value: Optional[str] = None

    @property
    def transitions(self) -> Transitions:
        return {
            None: ListActionsState()
        }

    def run(self) -> Optional[Hashable]:
        self.show()
        return None


class ListSubActionsState(State[SubMenuState]):

    @property
    def transitions(self) -> Transitions:
        return {
            "Set value": SetValueState(),
            "Get value": GetValueState(),
            "Exit": None
        }

    def run(self) -> Optional[Hashable]:
        choose_action_q = inquirer.List(
            "action",
            message="Choose action:",
            choices=list(self.transitions.keys()),
        )
        answers = inquirer.prompt([choose_action_q])
        return answers[choose_action_q.name]


class SetValueState(State[SubMenuState]):

    @property
    def transitions(self) -> Transitions:
        return {
            None: ListSubActionsState()
        }

    def run(self) -> Optional[Hashable]:
        input_value_q = inquirer.Text(
            "input_value",
            "Input value: "
        )
        answers = inquirer.prompt([input_value_q])
        self.menu.value = answers[input_value_q.name]
        return None


class GetValueState(State[SubMenuState]):

    @property
    def transitions(self) -> Transitions:
        return {
            None: ListSubActionsState()
        }

    def run(self) -> Optional[Hashable]:
        print(f"Value: {self.menu.value}")
        return None


if __name__ == "__main__":
    menu = Menu(initial_state=ListActionsState())
    menu.show()
