strategies_per_type = {}

max_attempts = 1000


class ReducerState(object):
    """docstring for ReducerState"""

    def __init__(self):
        super(ReducerState, self).__init__()
        self.last = None
        self.left = None
        self.right = None

    def change(self, val):
        self.last = val


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
        successes = 0
        ok = False
        last_fail = None
        for _ in range(max_attempts):
            simplified_input[var] = simplified
            ok = validator(**simplified_input)
            if ok:
                successes += 1
                if successes > 3:
                    break
            else:
                last_fail = simplified
            try:
                simplified = strategy(simplified, ok)
            except GiveUp:
                break
            except Exception:
                # todo?
                break
        simplified_input[var] = last_fail

        return True, simplified_input
    return False, simplified_input


def strategy_for(t_var):

    def wrap(fn):
        ctx = ReducerState()

        def wrap(*args, **kw):
            val = fn(ctx, *args, **kw)
            ctx.change(val)
            return val

        strategies_per_type[t_var] = wrap
        return wrap

    return wrap


@strategy_for(list)
def reduce_to_singleton(ctx: ReducerState, x, backtrack=False):
    """
    >>> reduce_to_singleton([1, 2])
    [1]
    """
    if not x:
        raise GiveUp('Singleton list')
    return x[:-1]


@strategy_for(int)
def reduce_int(ctx: ReducerState, val, backtrack=False):
    """
    >>> reduce_by_one(2)
    1
    >>> reduce_by_one(-2)
    -1
    """
    if val == 0 or val == 1:
        raise GiveUp('')
    if backtrack:
        return (ctx.last - val) // 2
    return val // 2
