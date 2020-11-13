import math
from typing import Union

def clamp_damage(value: Union[int, float]):
    return int(math.floor(max(1, min(value, 9999))))
