from quick.features import QuickCheck

qc = QuickCheck()


@qc.forall('Test simplification list', max_count=10)
def prop(x: [int]):
    return len(x) == 3


@qc.forall('Test simplification int', max_count=10)
def prop(x: int, y: int):
    return x + y == 5
