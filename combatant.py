import functools
from abc import ABC, abstractmethod
from random import randint


@functools.total_ordering
class ClampedStat:
    def __init__(self, maximum: int, minimum: int = 0):
        self.maximum = maximum
        self.minimum = minimum
        self.current = maximum

    def delta(self, other: int):
        value = self.current + other
        self.current = self.__clamp(value)

    def __lt__(self, other: int):
        return self.current < other

    def __eq__(self, other: int):
        return self.current == other

    def __str__(self):
        return f"{str(self.current)} / {str(self.maximum)}"

    def __clamp(self, value: int):
        return max(self.minimum, min(value, self.maximum))


class Combatant(ABC):
    def __init__(self, name: str, hp: int, mp: int, evasion: int):
        self.name = name
        self.hp = ClampedStat(hp)
        self.mp = ClampedStat(mp)
        self.evasion = evasion

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
    def stat_block(self) -> str:
        return f"{self.name}\n\nHP: {self.hp}"

    def take_turn(self) -> str:
        return "attack"
