from action.types import Action


class ActionDB:
    __instance = None

    def __init__(self):
        raise RuntimeError("Call init() instead")

    @classmethod
    def init(cls):
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            cls.__actions = {}
        return cls.__instance

    def register(self, cls):
        self.__actions[cls.name] = cls()
        return cls

    def __getattr__(self, name: str) -> Action:
        return self.__actions[name]

    def __getitem__(self, key: str) -> Action:
        return getattr(self, key)


actions = ActionDB.init()
