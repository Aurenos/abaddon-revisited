from random import randint

from .db import actions
from .types import ActionType, DamagingAction, Multiplier
from .util import clamp_output
from combatant import Combatant


@actions.register
class AttackAction(DamagingAction):
    name = "attack"
    action_type = ActionType.Physical

    def invoke(
        self,
        user: Combatant,
        target: Combatant,
        damage_range: tuple[int, int],
        multipliers: list[Multiplier],
    ):
        print(user.name, f"attacks {target.name}")
        input()

        target_evades = randint(1, 100) < target.evasion
        if target_evades:
            print(target.name, f"evades {user.name}'s attack!")
            return

        critical_hit = randint(1, 100) <= 10
        if critical_hit:
            multipliers.append(1.5)

        damage = clamp_output(randint(*damage_range), multipliers)

        print(target.name, "takes", damage, "damage!")
        target.hp.delta(-damage)
