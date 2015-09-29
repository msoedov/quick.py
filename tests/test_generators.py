import unittest
from quick.features import forall, QuickCheck
from quick.generators import *
from quick.arbitrary import A

qc = QuickCheck()


@qc.forall('Maybe generator')
def prop(x: maybe(None)):
    return x is None


TestSpec = qc.as_testcase()
