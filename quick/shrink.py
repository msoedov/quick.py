import itertools

strategies_per_type = {}

max_attempts = 1000


class ReducerState(object):
    """docstring for ReducerState"""

    def __init__(self):
        super(ReducerState, self).__init__()
        self.last = None
        self.history = []

    def change(self, val):
        self.last = val
        self.history.append(val)


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
        simplified_vals = strategy(value)
        last_fail = None
        seen_ok = False
        for val in itertools.islice(simplified_vals, 0, max_attempts):
            simplified_input[var] = val
            ok = validator(**simplified_input)
            if not ok:
                if last_fail is not None and seen_ok:
                    break
                last_fail = val
            else:
                seen_ok = True
        simplified_input[var] = last_fail

        return True, simplified_input
    return False, simplified_input


def strategy_for(t_var):

    def wrap(fn):
        strategies_per_type[t_var] = fn
        return fn

    return wrap


@strategy_for(list)
def reduce_to_singleton(val):
    """
    >>> reduce_to_singleton([1, 2])
    [1]
    """

    length = len(val)
    for size in range(1, length + 1):
        for start in range(0, (length - size) + 1):
            yield val[start:start + size]


@strategy_for(dict)
def all_dicts_form(val):
    """
    todo:
    """
    length = len(val)
    for size in range(1, length + 1):
        for start in range(0, (length - size) + 1):
            yield val[start:start + size]


@strategy_for(int)
def reduce_int(val):
    """
    >>> reduce_by_one(2)
    1
    >>> reduce_by_one(-2)
    -1
    """
    for num in range(0, abs(val)):
        yield num


@strategy_for(bool)
def reduce_bool(val):
    yield not val
