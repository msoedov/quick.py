from .arbitrary import A


def maybe_bool(a: A):
    return a.one_of(True, None, False)


def maybe(*something):
    """
    """

    def gn(a: A):
        return a.one_of(None, *something)

    return gn


def nasty_string(a: A):
    return 'unknown'


def number(a: A):
    kind = a.one_of(int, float)
    num = a.default(kind)
    return num
