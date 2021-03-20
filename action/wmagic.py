from random import randint

from combatant import Combatant
from combatant_events import CombatantEvent
from combatant_events import CombatantEventType as cet
from effects import EffectType

from .db import actions
from .types import SelfAction, Spell
from .util import Multiplier, clamp_output


@actions.register
class CureSpell(SelfAction, Spell):
    name = "cure"
    mp_cost = 25
    effect_type = EffectType.MAGICAL

    def produce_results(
        self, user: Combatant, multipliers: list[Multiplier]
    ) -> list[CombatantEvent]:
        hp_restored = clamp_output(randint(20, 25), multipliers)

        return [CombatantEvent(cet.HP_DELTA, hp_restored, user)]
