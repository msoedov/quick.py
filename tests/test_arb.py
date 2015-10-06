from quick.features import QuickCheck
from quick.generators import number
from quick.arbitrary import A

qc = QuickCheck(max_count=100)


def non_empty_list(el: number, ls: [number]):
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


@qc.forall('For any given list N len(A.some_of(N)) <= len(N)')
def prop(a: A, x: [number]):
    sub_set = a.some_of(x)
    return len(sub_set) <= len(x)


@qc.forall('Arbitrary some_of should return non empty list')
def prop(a: A, x: non_empty_list):
    sub_set = a.some_of(x, empty=False)
    return len(sub_set) >= 1


@qc.forall('Arbitrary one of')
def prop(a: A, x: [number]):
    element = a.one_of(*x)
    return element in x


@qc.forall('A.shuffle of any given list should result list of the same size')
def prop(a: A, x: [number]):
    shuffled = a.shuffle(x)
    return len(shuffled) == len(x)


@qc.forall('Shuffled singleton list should be the same')
def prop(a: A, x: number):
    shuffled = a.shuffle([x])
    return shuffled == [x]


TestSpec = qc.as_testcase()
