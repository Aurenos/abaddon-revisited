import math
from typing import Optional
from random import randint

from .db import register_action
from .types import DamageType, DamagingAction
from .util import clamp_damage
from combatant import Combatant

@register_action
class AttackAction(DamagingAction):
    name = "attack"
    mp_cost = 10
    damage_type = DamageType.Physical

    def invoke(
        self,
        user: Combatant,
        target: Combatant,
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
