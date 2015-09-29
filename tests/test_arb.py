import unittest
from quick.features import forall, QuickCheck
from quick.generators import number
from quick.arbitrary import A

qc = QuickCheck(max_count=100)


def non_emty_list(el: number, ls: [number]):
    """
    Generator which always returns non empty list
    """
    ls.append(el)
    return ls


@qc.forall('Arbitrary some_of')
def prop(a: A, x: [number]):
    sub_set = a.some_of(x)
    for el in sub_set:
        if el not in x:
            return False
    return True


@qc.forall('Arbitrary some_of should return non empty list')
def prop(a: A, x: non_emty_list):
    sub_set = a.some_of(x, empty=False)
    return len(sub_set) >= 1


@qc.forall('Arbitrary one of')
def prop(a: A, x: [number]):
    element = a.one_of(x)
    return element in x


TestSpec = qc.as_testcase()
