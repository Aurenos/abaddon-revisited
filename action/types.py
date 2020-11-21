from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional

from combatant import Combatant
from effects import EffectType, Element

from .util import pause_for_user, Multiplier


__all__ = [
    "ActionResultType",
    "ActionResult",
    "Action",
    "OffensiveAction",
    "SelfAction",
    "Spell",
]


class ActionResultType(Enum):
    HP_DELTA = auto()
    MP_DELTA = auto()


@dataclass
class ActionResult:
    type_: ActionResultType
    value: Any
    combatant: Combatant


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
        pause_for_user()
        results = self.produce_results(user, *args, **kwargs)
        self.apply_results(results)
        self.deduct_mp_from_user(user)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    def __str__(self):
        return self.display_name + (
            f"\t({self.mp_cost} MP)" if self.mp_cost > 0 else ""
        )

    def apply_results(self, results: list[ActionResult]):
        for result in results:
            if result.type_ == ActionResultType.HP_DELTA:
                result.combatant.hp.delta(result.value)
                if result.value <= 0:
                    print(result.combatant.name, "takes", abs(result.value), "damage!")
                else:
                    print(
                        result.combatant.name,
                        "restores",
                        result.value,
                        "HP!",
                        f"(Current: {result.combatant.hp})",
                    )

            elif result.type_ == ActionResultType.MP_DELTA:
                result.combatant.mp.delta(result.value)
                if result.value <= 0:
                    print(
                        result.combatant.name, "takes", abs(result.value), "MP damage!"
                    )
                else:
                    print(result.combatant.name, "restores", result.value, "MP!")

            pause_for_user()

    @property
    def display_name(self):
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
    ) -> list[ActionResult]:
        raise NotImplementedError

    def check_affinity(self, target: Combatant) -> tuple[list[Multiplier], bool]:
        multipliers = []
        negate = False
        if target.is_weak_to(self.element):
            print(target.name, "is weak to", f"{self.element}!")
            multipliers.append(1.5)
        elif target.absorbs(self.element):
            print(target.name, "absorbs", f"{self.element}!")
            negate = True

        return multipliers, negate


class SelfAction(Action, ABC):
    @abstractmethod
    def produce_results(
        self, user: Combatant, multipliers: list[Multiplier]
    ) -> list[ActionResult]:
        raise NotImplementedError


class Spell:
    def announce(self, user: Combatant, target: Optional[Combatant] = None, *_, **__):
        s = f"{user.name} casts {self.display_name}"
        if target:
            s += f" on {target.name}"
        s += "!"
        print(s)
