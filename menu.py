from action import Action


class MenuOption:
    def __init__(self, text: str, action: Action):
        self.text = text
        self.action = action

    def invoke(self, *args, **kwargs):
        return self.action(*args, **kwargs)


class Menu:
    def __init__(self, options: list[MenuOption], title: str = ""):
        self.options = options
        self.title = title

    @property
    def opt_dict(self):
        return { f"{i+1}": opt for i, opt in enumerate(self.options)}

    def show(self):
        print("-" * 50, "\n")
        print(f"{self.title}")

        if self.title != "":
            print()

        for i, opt in enumerate(self.options):
            print(f"{i+1}) {opt.text}")

        while True:
            selection = input("What will you do? ")
            if selection in self.opt_dict.keys():
                self.opt_dict[selection].invoke()
                break

