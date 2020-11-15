from random import randint
from combatant import Combatant

from .db import actions
from .types import SelfAction, Multiplier
from .util import clamp_output
from effects import EffectType


@actions.register
class CureSpell(SelfAction):
    name = "cure"
    mp_cost = 25
    effect_type = EffectType.Magical

    def invoke(self, user: Combatant, multipliers: list[Multiplier]):
        print(user.name, f"casts {self.display_name}!")
        input()
        
        hp_restored = clamp_output(randint(20, 25), multipliers)
        
        print(user.name, "restores", hp_restored, "HP!")

        user.hp.delta(hp_restored)
