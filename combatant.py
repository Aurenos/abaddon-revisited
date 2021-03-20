import functools
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from random import randint
from typing import Any, Optional, Union

from effects import Ailment, Buff, EffectType, Element, PersistentEffect


@functools.total_ordering
class ClampedStat:
    def __init__(self, maximum: int, minimum: int = 0):
        self.maximum = maximum
        self.minimum = minimum
        self.current = maximum

    def delta(self, other: int):
        value = self.current + other
        self.current = self.__clamp(value)

    def __lt__(self, other: Union[int, "ClampedStat"]):
        if isinstance(other, ClampedStat):
            return self.current < other.current
        return self.current < other

    def __eq__(self, other: Union[int, "ClampedStat"]):
        if isinstance(other, ClampedStat):
            return self.current == other.current
        return self.current == other

    def __str__(self):
        return f"{str(self.current)} / {str(self.maximum)}"

    def __clamp(self, value: int):
        return max(self.minimum, min(value, self.maximum))


class CombatantEventType(Enum):
    """The different types of ActionResults possible"""

    HP_DELTA = auto()
    MP_DELTA = auto()
    EVADE = auto()
    FORCE_ACTION = auto()
    ANNOUNCEMENT = auto()


@dataclass
class CombatantEvent:
    """My substitute for Python's lack of true algebraic data types"""

    type_: CombatantEventType
    value: Any
    combatant: "Combatant"
    special_text: Optional[str] = None


class Combatant(ABC):
    def __init__(
        self,
        name: str,
        hp: int,
        mp: int,
        evasion: int,
        affinity: Optional[Element] = None,
    ):
        self.name = name
        self.hp = ClampedStat(hp)
        self.mp = ClampedStat(mp)
        self.evasion = evasion
        self.affinity = affinity
        self.persistent_effects: list[PersistentEffect] = []

    @property
    @abstractmethod
    def base_damage(self) -> tuple[int, int]:
        raise NotImplementedError

    @property
    @abstractmethod
    def stat_block(self) -> str:
        raise NotImplementedError

    @property
    def defeated(self) -> bool:
        return self.hp.current <= 0

    @abstractmethod
    def get_stat_by_effect_type(self, effect_type: EffectType):
        raise NotImplementedError

    def is_weak_to(self, element: Element):
        return self.affinity and ~self.affinity == element

    def absorbs(self, element: Element):
        return self.affinity and self.affinity == element

    def handle_persistent_effects(self) -> list[CombatantEvent]:
        events = []
        for effect in self.persistent_effects:
            if effect.type_ == Ailment.POISON:
                poison_dmg = int(self.hp.maximum / randint(15, 25))
                stxt = f"{self.name} is poisoned!"
                events.append(
                    CombatantEvent(CombatantEventType.HP_DELTA, -poison_dmg, self, stxt)
                )

                effect.duration -= 1
                if effect.duration <= 0:
                    events.append(
                        CombatantEvent(
                            CombatantEventType.ANNOUNCEMENT,
                            None,
                            self,
                            f"{self.name} is no longer poisoned!",
                        )
                    )

        self.clean_persistent_effects()
        return events

    def clean_persistent_effects(self):
        self.persistent_effects = [
            effect for effect in self.persistent_effects if effect.duration > 0
        ]


class Player(Combatant):
    def __init__(self):
        super().__init__(
            name="Spero",
            hp=randint(8000, 9999),
            mp=randint(380, 550),
            evasion=randint(10, 20),
        )
        self.strength = randint(100, 255)
        self.magic = randint(100, 255)

    @property
    def base_damage(self) -> tuple[int, int]:
        return (30, 40)

    @property
    def stat_block(self) -> str:
        base = f"{self.name}\n\nHP: {self.hp}\nMP: {self.mp}"
        buffs = ", ".join(
            effect.type_.value
            for effect in self.persistent_effects
            if isinstance(effect.type_, Buff)
        )

        if buffs:
            base += f"\nBuffs: {buffs}"

        ailments = ", ".join(
            effect.type_.value
            for effect in self.persistent_effects
            if isinstance(effect.type_, Ailment)
        )

        if ailments:
            base += f"\nAilments: {ailments}"

        return base

    def get_stat_by_effect_type(self, effect_type: EffectType):
        if effect_type == EffectType.PHYSICAL:
            return self.strength

        if effect_type == EffectType.MAGICAL:
            return self.magic


class Abaddon(Combatant):
    def __init__(self):
        super().__init__(
            name="Abaddon",
            hp=randint(480000, 520000),
            mp=randint(2500, 3000),
            evasion=randint(5, 10),
        )

    @property
    def base_damage(self):
        return (960, 1160)

    @property
    def hp_percent(self):
        return math.floor((self.hp.current / self.hp.maximum) * 100)

    @property
    def stat_block(self) -> str:
        return f"{self.name}\n\nHP: {self.hp} ( {self.hp_percent}% )"

    def get_stat_by_effect_type(self, effect_type: EffectType):
        return 1

    def take_turn(self) -> str:
        return "attack"
