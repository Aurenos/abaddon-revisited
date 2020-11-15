import math
from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Optional

from combatant import Combatant
from effects import EffectType, Element

Multiplier = TypeVar("Multiplier", int, float)


class Action(ABC):  # Lawsuit
    name: str
    mp_cost: int = 0
    action_type: EffectType
    element: Element = Element.Unaspected

    def __call__(self, user: Combatant, *args, **kwargs):
        if self.announce:
            self.announce(user, *args, **kwargs)
        else:
            self.__announce(user)
        self.invoke(user, *args, **kwargs)
        self.deduct_mp_from_user(user)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    def __str__(self):
        return self.display_name + (
            f"\t({self.mp_cost} MP)" if self.mp_cost > 0 else ""
        )

    @property
    def display_name(self):
        return self.name.title()

    @abstractmethod
    def invoke(self, user: Combatant, *args, **kwargs):
        raise NotImplementedError
    
    def __announce(self, user: Combatant):
        print(user.name, "uses", f"{self.display_name}!")
        input()

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


class Spell:
    def announce(self, user: Combatant, target: Optional[Combatant] = None, *_, **__):
        s = f"{user.name} casts {self.display_name}"
        if target:
            s += f" on {target.name}"
        s += "!"
        print(s)
        input()
