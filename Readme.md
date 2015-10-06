# quick.py

quick.py is property testing liblary for python inspired by the Haskell library QuickCheck


What is property testing and what is QuickCheck?
--------------------------------------------------

```quote
QuickCheck is a tool for testing Haskell programs automatically.
The programmer provides a specification of the program, in the
form of properties which functions should satisfy,
and QuickCheck then tests that the properties hold in a large number
of randomly generated cases. Specifications are expressed in Haskell,
using combinators defined in the QuickCheck library.
QuickCheck provides combinators to define properties,
observe the distribution of test data, and define test data generators.
```

Examples
-------

Basic example:

```python
# example.py
from quick.features import QuickCheck

qc = QuickCheck(max_count=100)


@qc.forall('Associative of addition for integers')
def prop(x: int, y: int):
    return (x + y) == (y + x)


TestAddtion = qc.as_testcase()

```

```shell
>>> nosetests example.py
....................................................................................................
----------------------------------------------------------------------
Ran 100 tests in 0.061s

OK

```


Custom generators:

```python
# example.py
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


@qc.forall('Sorted lists first element should be always lesser or eq than last')
def prop(x: non_empty_list):
    sorted_x = sorted(x)
    first = sorted_x[0]
    last = sorted_x[-1]
    return first <= last


TestSort = qc.as_testcase()

```

```shell
>>> nosetests example.py
....................................................................................................
----------------------------------------------------------------------
Ran 100 tests in 0.070s

OK

```


Features
--------
- Integration with unittests liblary
- Custom generators
- Simpification of failure input (in progres)



Python 2 support?
-----------------
Oups, sorry


Getting Help
------------

For **feature requests** and **bug reports** [submit an issue
](https://github.com/msoedov/quick/issues) to the GitHub issue tracker for
quick.py.