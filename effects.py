from enum import Enum
from typing import Union


class EffectType(Enum):
    PHYSICAL = "physical"
    MAGICAL = "magical"


class Element(Enum):
    UNASPECTED = "unaspected"
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    WATER = "water"

    def __str__(self):
        return self.value

    def __invert__(self):
        if self is Element.FIRE:
            return Element.ICE

        if self is Element.ICE:
            return Element.FIRE

        if self is Element.LIGHTNING:
            return Element.WATER

        if self is Element.WATER:
            return Element.LIGHTNING

        if self is Element.UNASPECTED:
            return

    @classmethod
    def all(cls) -> list["Element"]:
        return list(cls.__members__.values())


class Ailment(Enum):
    POISON = "poison"
    CONFUSION = "confusion"
    BERSERK = "berserk"


class Buff(Enum):
    PROTECT = "protect"


class PersistentEffect:
    def __init__(self, type_: Union[Ailment, Buff], duration: int):
        self.type_ = type_
        self.duration = duration
