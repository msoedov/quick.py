import random
import sys
from typing import Any, Optional, Union

from .common import *

max_num = sys.maxsize
max_num = 1000
generation_width = 20


def default(
    type: Any,
    lo: int = -max_num,
    hi: int = max_num,
    complex_size: int = generation_width,
    min_complexity: int = 0,
) -> Optional[Union[bytes, int, float, str]]:
    if type == float:
        return random.uniform(lo, hi)

    elif type == int:
        return random.randint(lo, hi)

    elif type == str:
        size = random.randint(min_complexity, complex_size)
        lo = 0 if lo < 0 else lo
        hi = sys.maxunicode if hi > sys.maxunicode else hi
        return "".join([chr(random.randint(lo, hi)) for _ in range(size)])

    elif type == bytes:
        size = random.randint(min_complexity, complex_size)
        lo = 0 if lo < 0 else lo
        hi = 255 if hi > 255 else hi
        return bytes([random.randint(lo, hi) for _ in range(size)])
