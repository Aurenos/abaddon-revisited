import math
from typing import Union, Optional

from .types import Multiplier


def clamp_output(value: Union[int, float], multipliers: Optional[list[Multiplier]] = None):
    if multipliers is None:
        multipliers = []
    mult_value = math.prod([value, *multipliers])
    return int(math.floor(max(1, min(mult_value, 9999))))
