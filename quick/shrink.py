strategies_per_type = {}

max_attempts = 1000


class GiveUp(Exception):
    pass


def shrink(validator, input):
    """
    # basic example
    >>> validator = lambda x: 1 == x[-1]
    >>> shrink(validator, {'x': [1, 2, 3]})
    (True, {'x': [1, 2]})

    # It should return input as is for unknown structures
    >>> validator = lambda x: 1 == x[-1]
    >>> shrink(validator, {'x': None})
    (False, {'x': None})
    """
    simplified_input = input.copy()
    for var, value in input.items():
        strategy = strategies_per_type.get(type(value))
        if not strategy:
            continue
        simplified = strategy(value)
        prev = simplified_input
        for _ in range(max_attempts):
            prev = simplified_input.copy()
            simplified_input[var] = simplified
            ok = validator(**simplified_input)
            if ok:
                break
            try:
                simplified = strategy(simplified)
            except GiveUp:
                break
            except Exception:
                # todo?
                break
        simplified_input = prev
        return True, simplified_input
    return False, simplified_input


def strategy_for(t_var):

    def wrap(fn):
        strategies_per_type[t_var] = fn
        return fn

    return wrap


@strategy_for(list)
def reduce_to_singleton(x):
    """
    >>> reduce_to_singleton([1, 2])
    [1]
    """
    if not x:
        raise GiveUp('Singleton list')
    return x[:-1]


@strategy_for(int)
def reduce_by_one(x):
    """
    >>> reduce_by_one(2)
    1
    >>> reduce_by_one(-2)
    -1
    """
    if x == 0:
        raise GiveUp('Singleton list')
    return x + 1 if x < 0 else x - 1
