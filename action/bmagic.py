from effects import EffectType
from random import randint
from combatant import Combatant

from .db import actions
from .types import DamagingAction, Multiplier
from .util import clamp_output
from effects import EffectType, Element


@actions.register
class FlareSpell(DamagingAction):
    name = "flare"
    mp_cost = 30
    effect_type = EffectType.Magical
    element = Element.Fire

    def invoke(
        self,
        user: Combatant,
        target: Combatant,
        damage_range: tuple[int, int],
        multipliers: list[Multiplier],
    ):
        print(user.name, "casts", self.display_name, "on", f"{target.name}!")
        input()

        if target.affinity and ~target.affinity == self.element:
            print(target.name, "is weak to", f"{self.element}!")
            multipliers.append(1.5)
        
        damage = clamp_output(randint(*damage_range), multipliers)

        print(target.name, "takes", damage, "damage!")
        target.hp.delta(-damage)
