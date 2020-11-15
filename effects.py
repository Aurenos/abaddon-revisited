from enum import Enum


class EffectType(Enum):
    Physical = "physical"
    Magical = "magical"


class Element(Enum):
    Unaspected = "unaspected"
    Fire = "fire"
    Ice = "ice"
    Lightning = "lightning"
    Water = "water"
