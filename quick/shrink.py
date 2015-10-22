import itertools
from copy import deepcopy
from .core import flatten, GenValue

strategies_per_type = {}

max_attempts = 1000


def shrink(validator, schema):
    """
    :param: schema Schema{'a': GenValue(lambda x: x+1,
                         {'x':
                                GenValue(lambda c: c,
                                    {'c': 1})}),
                    'd': 1
                    }
    """
    simplified_input = flatten(schema)
    attemps = 0
    for var, value in schema.items():
        simplified_vals = variations(value)
        last_fail = None
        for val in itertools.islice(simplified_vals, 0, max_attempts):
            sc = deepcopy(schema)
            sc[var] = val
            simplified_input = flatten(sc)
            ok = validator(**simplified_input)
            if not ok:
                if last_fail is not None:
                    break
                last_fail = sc
            attemps += 1
        else:
            if last_fail is None:
                return False, flatten(schema)
        return True, flatten(last_fail)
    return False, flatten(schema)


def reduce(t_var):

    def wrap(fn):
        strategies_per_type[t_var] = fn
        return fn

    return wrap


def variations(value):
    strategy = strategies_per_type.get(type(value))
    if strategy is None:
        return [value]
    return strategy(value)


class llist(object):

    def __init__(self, seq):
        self.lst = list(seq)

    def __getitem__(self, index):
        try:
            return self.lst[index]
        except LookupError:
            return self.lst[-1]

    def __len__(self):
        return len(self.lst)


@reduce(GenValue)
def gen_simpl(val):
    """
    GenValue(gen=lambda x, y: x, kwargs={'y': [None], 'x': [None, None, None]})
    """
    fn, kw = val
    kw_variations = {}
    longest = 0
    for k, v in kw.items():
        vars = llist(variations(v))
        kw_variations[k] = vars
        lv = len(vars)
        if longest < lv:
            longest = lv
    for ii in range(longest):
        for key, vars in kw_variations.items():
            ikw = {k: v[ii] for k, v in kw_variations.items()}
            yield GenValue(fn, ikw)


@reduce(list)
def all_list_for(val):

    length = len(val)
    yield []
    for size in range(1, length + 1):
        for start in range(0, (length - size) + 1):
            yield val[start:start + size]


@reduce(dict)
def all_dicts_for(val):
    """
    """
    key_lists = all_list_for(list(val.keys()))
    for key_set in key_lists:
        yield {k: val[k] for k in key_set}


@reduce(int)
def all_ints_for(val):
    for num in range(0, abs(val)):
        yield num


@reduce(str)
def all_str_for(val):
    chars = val.split()
    sub_strs = all_list_for(chars)
    for sub_str in sub_strs:
        return ''.join(sub_str)


@reduce(bool)
def all_bools_for(val):
    yield not val
