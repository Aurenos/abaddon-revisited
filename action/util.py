import math
from typing import Optional, Union, TypeVar

Multiplier = TypeVar("Multiplier", int, float)

pause_for_user = input  # alias input to make purpose clear


def clamp_output(
    value: Union[int, float],
    multipliers: Optional[list[Multiplier]] = None,
    negate: bool = False,
):
    if multipliers is None:
        multipliers = []
    mult_value = math.prod([value, *multipliers])
    out = int(math.floor(max(1, min(mult_value, 9999))))
    return -out if negate else out
