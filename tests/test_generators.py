import unittest

from quick.arbitrary import A
from quick.features import QuickCheck, forall
from quick.generators import *

qc = QuickCheck()


@qc.forall('Maybe generator')
def prop(x: maybe(None)):
    return x is None


TestSpec = qc.as_testcase()
