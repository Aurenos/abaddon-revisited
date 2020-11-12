import math
import sys, inspect
from abc import ABC, abstractmethod
from typing import Optional, Union
from random import randint


import combatant as comb


class Action(ABC):  # Lawsuit
    name: str
    mp_cost: int = 0

    def __call__(self, user: comb.Combatant, *args, **kwargs):
        self.invoke(user, *args, **kwargs)
        self.deduct_mp_from_user(user)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    def __str__(self):
        return self.name + f"\t({self.mp_cost} MP)" if self.mp_cost > 0 else ""

    @abstractmethod
    def invoke(self, user: comb.Combatant):
        raise NotImplemented

    def deduct_mp_from_user(self, user: comb.Combatant):
        user.mp.delta(self.mp_cost)


class OffensiveAction(Action, ABC):
    @abstractmethod
    def invoke(self, user: comb.Combatant, target: comb.Combatant):
        raise NotImplemented


class SelfAction(Action, ABC):
    @abstractmethod
    def invoke(self, user: comb.Combatant):
        raise NotImplemented


def clamp_damage(value: Union[int, float]):
    return int(math.floor(max(1, min(value, 9999))))


###############################################


class AttackAction(OffensiveAction):
    name = "attack"

    def invoke(
        self,
        user: comb.Combatant,
        target: comb.Combatant,
        damage_range: tuple[int, int],
        damage_multipliers: Optional[list[float]] = None,
    ):
        if damage_multipliers is None:
            damage_multipliers = []

        print(user.name, f"attacks {target.name}")
        input()

        target_evades = randint(1, 100) < target.evasion
        if target_evades:
            print(target.name, f"evades {user.name}'s attack!")
            return

        critical_hit = randint(1, 100) <= 10
        if critical_hit:
            damage_multipliers.append(1.5)

        damage = clamp_damage(math.prod((randint(*damage_range), *damage_multipliers)))

        print(target.name, "takes", damage, "damage!")
        target.hp.delta(-damage)


#######################################################

ACTIONS = {
    cls.name: cls()
    for _, cls in inspect.getmembers(
        sys.modules[__name__],
        lambda c: inspect.isclass(c)
        and not inspect.isabstract(c)
        and inspect.getmodule(c).__name__ == __name__,
    )
}

if __name__ == "__main__":
    print(ACTIONS)
