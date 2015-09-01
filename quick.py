"""
Quick check testing library for python
"""
import pprint
from quick.core import check, quick_check
from quick.features import forall, QuickCheck
from quick.generators import number
from quick.arbitrary import A


qc = QuickCheck()


def y_generator(x: bytes):
    return x


# @forall('Compostion of annotation')
# def prop(x: int, y: y_generator):
#     return True


# @forall('Compostion of annotation')
# def prop(x: int, y: float):
#     return True


# @forall('Default values', max_count=100)
# def prop(x: int, y: float, z=1):
#     return max(x, y, z) > 1


@qc('Numbers', max_count=100)
def prop(x: number, y: number):
    return x + y == y + x


@qc.forall('Sorted array', max_count=100)
def prop(x: [number]):
    s = sorted(x)
    x.sort()
    return s == x

qc.run()
