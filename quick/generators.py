from .arbitrary import A, Arbitrary


def maybe_bool(a: Arbitrary):
    """
    >>> maybe_bool(A()) in [None, True, False]
    True
    """
    return maybe(bool)(a)


def maybe(kind):

    def gn(a: Arbitrary):
        return a.one_of(None, a.default(kind))

    return gn


def number(a: Arbitrary):
    kind = a.one_of(int, float)
    num = a.default(kind)
    return num


def positive_num(x: int):
    return abs(x)
