from typing import Callable


class Action:  # Lawsuit
    def __init__(self, action_fn: Callable, mp_cost: int = 0):
        self.action_fn = action_fn
        self.mp_cost = mp_cost

    def __call__(self,*args, **kwargs):
        return self.action_fn(*args, **kwargs)
