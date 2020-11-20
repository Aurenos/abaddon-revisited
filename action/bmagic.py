from random import randint

from combatant import Combatant
from effects import EffectType, Element

from .db import actions
from .types import ActionResult
from .types import ActionResultType as artype
from .types import DamagingAction, Spell
from .util import Multiplier, clamp_output


@actions.register
class FlareSpell(DamagingAction, Spell):
    name = "flare"
    mp_cost = 30
    effect_type = EffectType.Magical
    element = Element.Fire

    def produce_results(
        self,
        user: Combatant,
        target: Combatant,
        damage_range: tuple[int, int],
        multipliers: list[Multiplier],
    ) -> list[ActionResult]:
        if target.affinity and ~target.affinity == self.element:
            print(target.name, "is weak to", f"{self.element}!")
            multipliers.append(1.5)

        damage = clamp_output(randint(*damage_range), multipliers)

        return [ActionResult(artype.HP_DELTA, -damage, target)]
