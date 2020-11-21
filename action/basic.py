from random import randint

from combatant import Combatant

from .db import actions
from .types import ActionResult
from .types import ActionResultType as art
from .types import OffensiveAction, EffectType
from .util import Multiplier, clamp_output


@actions.register
class AttackAction(OffensiveAction):
    name = "attack"
    effect_type = EffectType.Physical

    def announce(self, user: Combatant, target: Combatant, *_, **__):
        print(user.name, f"attacks {target.name}")

    def produce_results(
        self,
        user: Combatant,
        target: Combatant,
        damage_range: tuple[int, int],
        multipliers: list[Multiplier],
    ) -> list[ActionResult]:
        target_evades = randint(1, 100) < target.evasion
        if target_evades:
            print(target.name, f"evades {user.name}'s attack!")
            return []

        critical_hit = randint(1, 100) <= 10
        if critical_hit:
            multipliers.append(1.5)

        damage = clamp_output(randint(*damage_range), multipliers)

        return [ActionResult(art.HP_DELTA, -damage, target)]
