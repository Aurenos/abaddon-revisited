from enum import Enum, auto
from dataclasses import dataclass
from typing import Any
from combatant import Combatant


class CombatantEventType(Enum):
    """The different types of ActionResults possible"""

    HP_DELTA = auto()
    MP_DELTA = auto()
    EVADE = auto()
    FORCE_ACTION = auto()


@dataclass
class CombatantEvent:
    """My substitute for Python's lack of true algebraic data types"""

    type_: CombatantEventType
    value: Any
    combatant: Combatant
