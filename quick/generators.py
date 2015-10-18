from .arbitrary import A


def maybe_bool(a: A):
    """
    >>> maybe_bool(A()) in [None, True, False]
    True
    """
    return maybe(bool)(a)


def maybe(t):

    def gn(a: A):
        return a.one_of(None, a.default(t))

    return gn


def number(a: A):
    kind = a.one_of(int, float)
    num = a.default(kind)
    return num


def positive_num(x: int):
    return abs(x)
