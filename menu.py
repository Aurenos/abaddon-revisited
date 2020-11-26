from action import Action
from typing import TypeVar


MenuOption = TypeVar("MenuOption", "Menu", Action)


class Menu:
    """Class for constructing the text menus. Uses builder pattern to allow
    for method chaining style of construction."""

    def __init__(self, title: str = "", prompt: str = "What will you do? "):
        self.title = title
        self.prompt = prompt
        self.actions: list[Action] = []
        self.submenus: list["Menu"] = []
        self.is_child = False

    def add_submenu(self, submenu: "Menu"):
        submenu.is_child = True
        self.submenus.append(submenu)
        return self

    def add_action(self, action: Action):
        self.actions.append(action)
        return self

    @property
    def options(self) -> dict[str, MenuOption]:
        opts = self.actions + self.submenus
        return {f"{i+1}": opt for i, opt in enumerate(opts)}

    def valid_selection(self, selection: str) -> bool:
        return selection in self.options.keys()

    def get_selection(self, selection: str) -> MenuOption:
        return self.options[selection]

    def is_menu(self, selection: MenuOption) -> bool:
        return isinstance(selection, self.__class__)

    def print_separator(self):
        print("-" * 25)

    def show(self):
        """Does the work of printing out the menu text"""

        if self.is_child:
            print()

        self.print_separator()

        print(f"{self.title}")

        if self.title != "":
            print()

        for key, opt in self.options.items():
            if self.is_menu(opt):
                text = opt.title.title()
            else:
                text = str(opt)
            print(f"{key}) {text}")

        if self.is_child:
            print("0) Cancel")

        print()

    def get_action(self) -> str:
        """Shows the menu text and prompts the user for input.
        Will return the name of an Action to be performed in the battle loop"""

        self.show()

        while True:
            select_in = input(self.prompt)
            if self.is_child and select_in == "0":
                return
            elif not self.valid_selection(select_in):
                continue
            elif self.is_menu(
                # Using 3.8's fancy new walrus operator
                selection := self.get_selection(select_in)
            ):
                # For when the selection is a submenu
                action_name = selection.get_action()
                if action_name:
                    return action_name
                else:
                    self.show()
                    continue
            else:
                return selection.name
