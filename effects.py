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

