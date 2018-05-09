from quick.features import QuickCheck
from quick.generators import number

qc = QuickCheck()


def y_generator(x: bytes):
    return x


@qc.forall("Compostion of annotation")
def prop(x: int, y: y_generator):
    return True


@qc.forall("Int and float")
def prop(x: int, y: float):
    return True


@qc.forall("Radom unicode str")
def prop(x: str):
    return True


@qc.forall("Default values", max_count=100)
def prop(x: int, z=1):
    return abs(x) + 1 > z


@qc("Numbers", max_count=100)
def prop(x: number, y: number):
    return x + y == y + x


@qc.forall("Sorted array", max_count=100)
def prop(x: [number]):
    s = sorted(x)
    x.sort()
    return s == x


TestSpec = qc.as_testcase()
