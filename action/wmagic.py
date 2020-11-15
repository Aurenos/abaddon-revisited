from random import randint
from combatant import Combatant

from .db import actions
from .types import SelfAction, Spell, Multiplier
from .util import clamp_output
from effects import EffectType


@actions.register
class CureSpell(SelfAction, Spell):
    name = "cure"
    mp_cost = 25
    effect_type = EffectType.Magical

    def invoke(self, user: Combatant, multipliers: list[Multiplier]):     
        hp_restored = clamp_output(randint(20, 25), multipliers)
        
        print(user.name, "restores", hp_restored, "HP!")

        user.hp.delta(hp_restored)
