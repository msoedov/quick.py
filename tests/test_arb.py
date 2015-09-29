import unittest
from quick.features import forall, QuickCheck
from quick.generators import number
from quick.arbitrary import A

qc = QuickCheck()


def non_emty_list(el: number, ls: [number]):
    """
    Generator which always returns non empty list
    """
    ls.append(el)
    return ls


@qc.forall('Arbitrary some of')
def prop(a: A, x: [number]):
    sub_set = a.some_of(x)
    for el in sub_set:
        if el not in x:
            return False
    return True


@qc.forall('Arbitrary some of should return no empty list')
def prop(a: A, x: non_emty_list):
    sub_set = a.some_of(x, empty=False)
    return sub_set != []


@qc.forall('Arbitrary one of')
def prop(a: A, x: [number]):
    element = a.one_of(x)
    return element in x


class TestSpec(unittest.TestCase):

    def test_module(self):
        qc.run()
