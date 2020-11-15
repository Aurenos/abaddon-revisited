from action import Action


class Menu:
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
    def options(self):
        return self.actions + self.submenus

    @property
    def opt_dict(self):
        return {f"{i+1}": opt for i, opt in enumerate(self.options)}

    def print_separator(self):
        print("-" * 25)

    def show(self):
        if self.is_child: 
            print()
        
        self.print_separator()

        print(f"{self.title}")

        if self.title != "":
            print()

        for i, opt in enumerate(self.options):
            if isinstance(opt, self.__class__):
                text = opt.title.title()
            else:
                text = str(opt)
            print(f"{i+1}) {text}")

        if self.is_child:
            print("0) Cancel")

        print()


    def get_action(self) -> str:
        self.show()

        while True:
            selection = input(self.prompt)
            if self.is_child and selection == "0":
                return
            elif selection not in self.opt_dict.keys():
                continue
            elif isinstance(self.opt_dict[selection], self.__class__):
                action_name = self.opt_dict[selection].get_action()
                if action_name:
                    return action_name
                else:
                    self.show()
                    continue
            else:
                return self.opt_dict[selection].name
