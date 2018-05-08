from typing import Callable, List

from .core import flatten, generate


def Value(gen_function: Callable) -> List[str]:
    """
    Helper function to generate value from annotted generator without
    using QC.
    """
    function, schema = generate(gen_function)
    kwargs = flatten(schema)
    return function(**kwargs)


def Values(gen_function, number: int):
    return [Value(gen_function) for _ in range(number)]
