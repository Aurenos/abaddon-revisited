from random import randint

from combatant import Combatant
from effects import EffectType, Element

from .db import actions
from .types import ActionResult
from .types import ActionResultType as art
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
        weakness_multipliers, negation = self.check_affinity(target)
        multipliers += weakness_multipliers                  

        damage = clamp_output(randint(*damage_range), multipliers, negate=negation)

        return [ActionResult(art.HP_DELTA, -damage, target)]
