from random import randint

from combatant import Combatant
from effects import EffectType

from .db import actions
from .types import ActionResult
from .types import ActionResultType as artype
from .types import SelfAction, Spell
from .util import Multiplier, clamp_output


@actions.register
class CureSpell(SelfAction, Spell):
    name = "cure"
    mp_cost = 25
    effect_type = EffectType.Magical

    def produce_results(
        self, user: Combatant, multipliers: list[Multiplier]
    ) -> list[ActionResult]:
        hp_restored = clamp_output(randint(20, 25), multipliers)

        return [ActionResult(artype.HP_DELTA, hp_restored, user)]
