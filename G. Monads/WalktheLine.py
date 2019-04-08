from typing import NewType
from pymonad.Reader import curry
from pymonad.Maybe import *

Birds = NewType('Birds', int)
Pole = NewType('Pole', (Birds, Birds))

@curry
def landLeft(n: Birds, pole: Pole) -> Maybe:
    left: Birds = pole[0]
    right: Birds = pole[1]

    if (abs((left + n) - right) < 4):
        return Just((left + n, right))
    else:
        return Nothing

@curry
def landRight(n: Birds, pole: Pole) -> Maybe:
    left: Birds = pole[0]
    right: Birds = pole[1]

    if (abs(left - (right + n)) < 4):
        return Just((left, right + n))
    else:
        return Nothing

print(Just((0, 0)) >> landLeft(1) >> Nothing >> landRight(1))
