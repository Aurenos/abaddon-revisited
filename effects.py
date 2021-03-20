from enum import Enum
from typing import Union


class EffectType(Enum):
    Physical = "physical"
    Magical = "magical"


class Element(Enum):
    Unaspected = "unaspected"
    Fire = "fire"
    Ice = "ice"
    Lightning = "lightning"
    Water = "water"

    def __str__(self):
        return self.value

    def __invert__(self):
        if self is Element.Fire:
            return Element.Ice

        if self is Element.Ice:
            return Element.Fire

        if self is Element.Lightning:
            return Element.Water

        if self is Element.Water:
            return Element.Lightning

        if self is Element.Unaspected:
            return

    @classmethod
    def all(cls) -> list["Element"]:
        return list(cls.__members__.values())


class Ailment(Enum):
    Poison = "poison"
    Confusion = "confusion"
    Berserk = "berserk"


class Buff(Enum):
    Protect = "protect"


class PersistentEffect:
    def __init__(self, type_: Union[Ailment, Buff], duration: int):
        self.type_ = type_
        self.duration = duration
