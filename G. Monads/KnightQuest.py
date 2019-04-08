from typing import NewType, List as L
from pymonad import List

class Infix:
    def __init__(self, function):
        self.fn = function

    def __ror__(self, left_arg):
        """
        For | on left:
        Store the left argument as self.left_arg
        and return this object.
        """
        self.left_arg = left_arg
        return self

    def __or__(self, right_arg):
        """For | on right: Execute the function. """
        return self.fn(self.left_arg, right_arg)


KnightPos = NewType('KnightPos', (int, int))

def moveKnight(pos: KnightPos) -> L[KnightPos]:
    c = pos[0]
    r = pos[1]

    possPos = List((c+2,r-1),(c+2,r+1),(c-2,r-1),(c-2,r+1),(c+1,r-2),(c+1,r+2),(c-1,r-2),(c-1,r+2))

    return filter(lambda cr: cr[0] in range(1, 9) and cr[1] in range(1,9), possPos)

def in3(pos: KnightPos) -> L[KnightPos]:
    return List(pos) >> moveKnight >> moveKnight >> moveKnight

def canReachIn3(start: KnightPos, end: KnightPos) -> bool:
    return end in in3(start)

rI3 = Infix(canReachIn3)

print((0,0) |rI3| (6,3))
