import functools
import math
from abc import ABC, abstractmethod
from random import randint
from typing import Optional, Union

from effects import EffectType, Element, Ailment


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
        self.ailments: list[Ailment] = []

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

    def handle_ailments(self):
        pass


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
        return f"{self.name}\n\nHP: {self.hp}\nMP: {self.mp}"

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
