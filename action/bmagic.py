from random import randint

from combatant import Combatant, CombatantEvent
from combatant import CombatantEventType as cet
from effects import EffectType, Element

from .db import actions
from .types import OffensiveAction, Spell
from .util import Multiplier, clamp_output
from util import pause_for_user


class ElementalSpell(OffensiveAction, Spell):
    mp_cost = 30
    effect_type = EffectType.MAGICAL

    def produce_results(
        self,
        user: Combatant,
        target: Combatant,
        damage_range: tuple[int, int],
        multipliers: list[Multiplier],
    ) -> list[CombatantEvent]:
        weakness_multiplier, absorption_multiplier = self.check_affinity(target)
        multipliers.append(weakness_multiplier)

        damage = (
            clamp_output(randint(*damage_range), multipliers) * absorption_multiplier
        )

        return [CombatantEvent(cet.HP_DELTA, -damage, target)]


@actions.register
class FlareSpell(ElementalSpell):
    name = "flare"
    element = Element.FIRE


@actions.register
class BlizzardSpell(ElementalSpell):
    name = "blizzard"
    element = Element.ICE


@actions.register
class BoltSpell(ElementalSpell):
    name = "bolt"
    element = Element.LIGHTNING

    # Just because "Bolt" is a really short name
    # TODO: Maybe add some way to calculate how many \t's we need in the base __str__
    def __str__(self):
        return f"{self.display_name}\t\t({self.mp_cost} MP)"


@actions.register
class WaterSpell(ElementalSpell):
    name = "water"
    element = Element.WATER


@actions.register
class MPAbsorbSpell(OffensiveAction, Spell):
    name = "mp_absorb"
    effect_type = EffectType.MAGICAL

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

        multipliers.append(1 / 36)  # hurray for magic numbers :P

        damage = clamp_output(randint(*damage_range), multipliers)
        if damage > target.mp:  # the original didn't actually have this check
            damage = target.mp.current

        return [
            CombatantEvent(cet.MP_DELTA, -damage, target),
            CombatantEvent(cet.MP_DELTA, damage, user),
        ]
