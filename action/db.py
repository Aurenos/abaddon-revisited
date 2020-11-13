ACTIONS = {}


def register_action(cls):
    ACTIONS[cls.name] = cls()
    return cls
