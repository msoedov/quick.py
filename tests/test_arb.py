import unittest
from quick.features import forall, QuickCheck
from quick.generators import number
from quick.arbitrary import A

qc = QuickCheck()


@qc.forall('Arbitrary some of')
def prop(a: A, x: [number]):
    sub_set = a.some_of(x)
    for el in sub_set:
        if el not in x:
            return False
    return True


class TestSpec(unittest.TestCase):

    def test_module(self):
        qc.run()
