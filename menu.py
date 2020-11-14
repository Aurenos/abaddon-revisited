from action import Action


class Menu:
    def __init__(self, title: str = ""):
        self.title = title
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
    def options(self):
        return self.actions + self.submenus

    @property
    def opt_dict(self):
        return {f"{i+1}": opt for i, opt in enumerate(self.options)}

    def show(self) -> str:
        print(f"{self.title}")

        if self.title != "":
            print()

        for i, opt in enumerate(self.options):
            if isinstance(opt, self.__class__):
                text = opt.title
            else:
                text = str(opt)
            print(f"{i+1}) {text}")

        if self.is_child:
            print("0) Cancel")

        print()

        while True:
            selection = input("What will you do? ")
            if self.is_child and selection == "0":
                return
            elif selection not in self.opt_dict.keys():
                continue
            elif isinstance(self.opt_dict[selection], self.__class__):
                action_name = self.opt_dict[selection].show()
                if action_name:
                    return action_name
                else:
                    continue
            else:
                return self.opt_dict[selection].name
