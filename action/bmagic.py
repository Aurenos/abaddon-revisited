from random import randint

from combatant import Combatant
from effects import EffectType, Element

from .db import actions
from .types import ActionResult
from .types import ActionResultType as art
from .types import OffensiveAction, Spell
from .util import Multiplier, clamp_output, pause_for_user


class ElementalSpell(OffensiveAction, Spell):
    mp_cost = 30
    effect_type = EffectType.Magical

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


@actions.register
class FlareSpell(ElementalSpell):
    name = "flare"
    element = Element.Fire


@actions.register
class BlizzardSpell(ElementalSpell):
    name = "blizzard"
    element = Element.Ice


@actions.register
class BoltSpell(ElementalSpell):
    name = "bolt"
    element = Element.Lightning

    # Just because "Bolt" is a really short name
    # TODO: Maybe add some way to calculate how many \t's we need in the base __str__
    def __str__(self):
        return f"{self.display_name}\t\t({self.mp_cost} MP)"


@actions.register
class WaterSpell(ElementalSpell):
    name = "water"
    element = Element.Water


@actions.register
class MPAbsorbSpell(OffensiveAction, Spell):
    name = "mp_absorb"
    effect_type = EffectType.Magical
    
    @property
    def display_name(self):
        return "MP Absorb"

    def produce_results(
        self,
        user: Combatant,
        target: Combatant,
        damage_range: tuple[int, int],
        multipliers: list[Multiplier],
    ):
        if target.mp <= 0:
            print(target.name, "has no MP left")
            pause_for_user()
            return []

        multipliers.append(1/36)    # hurray for magic numbers :P

        damage = clamp_output(randint(*damage_range), multipliers)
        if damage > target.mp:  # the original didn't actually have this check
            damage = target.mp.current

        return [
            ActionResult(art.MP_DELTA, -damage, target),
            ActionResult(art.MP_DELTA, damage, user)
        ]
