from abc import ABC, abstractmethod
from typing import Optional

from combatant import Combatant, CombatantEvent
from effects import EffectType, Element

from .util import Multiplier
from util import pause_for_user

__all__ = [
    "Action",
    "OffensiveAction",
    "SelfAction",
    "Spell",
]


class Action(ABC):  # Lawsuit
    """The base class of all actions.

    __call__ uses a template method pattern to take care of resolving
    actions and applying the results of those actions to the combatants;
    sub-classes need only override the produce_results() method to be
    functional.
    """

    name: str
    mp_cost: int = 0
    action_type: EffectType
    element: Element = Element.UNASPECTED

    def __call__(self, user: Combatant, *args, **kwargs) -> list[CombatantEvent]:
        if self.announce:
            self.announce(user, *args, **kwargs)
        else:
            self.__announce(user)
        pause_for_user()
        events = self.produce_results(user, *args, **kwargs)
        self.deduct_mp_from_user(user)
        return events

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    def __str__(self):
        return self.display_name + (
            f"\t({self.mp_cost} MP)" if self.mp_cost > 0 else ""
        )

    @property
    def display_name(self) -> str:
        return self.name.title()

    def __announce(self, user: Combatant):
        print(user.name, "uses", f"{self.display_name}!")

    def deduct_mp_from_user(self, user: Combatant):
        user.mp.delta(-self.mp_cost)


class OffensiveAction(Action, ABC):
    @abstractmethod
    def produce_results(
        self,
        user: Combatant,
        target: Combatant,
        damage_range: tuple[int, int],
        multipliers: list[Multiplier],
    ) -> list[CombatantEvent]:
        raise NotImplementedError

    def check_affinity(self, target: Combatant) -> tuple[Multiplier, Multiplier]:
        """Check to see if the element of this action interacts with the element of the
        target in some way. Prints out appropriate contextual text and returns a pair of multipliers"""

        weakness_multiplier = 1
        absorption_multiplier = 1
        if target.is_weak_to(self.element):
            print(target.name, "is weak to", f"{self.element}!")
            weakness_multiplier = 1.5
        elif target.absorbs(self.element):
            print(target.name, "absorbs", f"{self.element}!")
            absorption_multiplier = -1

        return weakness_multiplier, absorption_multiplier


class SelfAction(Action, ABC):
    @abstractmethod
    def produce_results(
        self, user: Combatant, multipliers: list[Multiplier]
    ) -> list[CombatantEvent]:
        raise NotImplementedError


class Spell:
    """Mixin class to define special announce() method for spell actions"""

    def announce(self, user: Combatant, target: Optional[Combatant] = None, *_, **__):
        s = f"{user.name} casts {self.display_name}"
        if target:
            s += f" on {target.name}"
        s += "!"
        print(s)
