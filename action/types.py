import math
from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar

from combatant import Combatant


Multiplier = TypeVar("Multiplier", int, float)


class ActionType(Enum):
    Physical = "physical"
    Magical = "magical"


class Action(ABC):  # Lawsuit
    name: str
    mp_cost: int = 0
    action_type: ActionType

    def __call__(self, user: Combatant, *args, **kwargs):
        self.invoke(user, *args, **kwargs)
        self.deduct_mp_from_user(user)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    def __str__(self):
        return self.name.title() + (
            f"\t({self.mp_cost} MP)" if self.mp_cost > 0 else ""
        )

    @abstractmethod
    def invoke(self, user: Combatant, *args, **kwargs):
        raise NotImplementedError

    def deduct_mp_from_user(self, user: Combatant):
        user.mp.delta(-self.mp_cost)


class DamagingAction(Action, ABC):
    @abstractmethod
    def invoke(
        self,
        user: Combatant,
        target: Combatant,
        damage_range: tuple[int, int],
        multipliers: list[Multiplier],
    ):
        raise NotImplementedError


class SelfAction(Action, ABC):
    @abstractmethod
    def invoke(self, user: Combatant, multipliers: list[Multiplier]):
        raise NotImplementedError
