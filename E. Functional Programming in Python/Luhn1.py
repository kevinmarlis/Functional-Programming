from pyrsistent import pvector, v
from toolz import interleave, accumulate, last, concat
from operator import add
from pyrsistent.typing import PVector

# Maps every "character" in the string to a function that returns an int,
# and creates a PVector (immutable list) out of the resulting ints
def toDigits(n: int) -> PVector[int]:
    return pvector(map(lambda c: int(c), str(n)))

# Interleave joins a sequence of sequences by alternating between the two. Here,
# interleave is called on a list of two lists. The first list, ints[::-1][0::2],
# is made of the even indeces of the reversed "ints" list. The second is made of
# the odd indeces of the reversed "ints" list, mapped so that they are doubled,
# and made into a PVector. A single PVector is made from the interleavened sequences,
# as interleave returns a lazy iterator.
def doubleEveryOther(ints: PVector[int]) -> PVector[int]:
    return pvector(interleave([ints[::-1][0::2],
        pvector(map(lambda x: x * 2, ints[::-1][1::2]))]))

# Concat reduces a list of lists of ints into a single list.
# Accumulate applies the add function such that the first element is added to the
# second, that value is added to the third, etc, and last returns the final sum
# of all vaues in the list.
def sumDigits(ints: PVector[int]) -> int:
    return last(accumulate(add, concat(map(lambda c: toDigits(c), ints))))

# isValid converts the potential credit card number to digits, doubles every other
# starting from the right, sums them up, and checks if that is divisible by 10
def isValid(int: int) -> bool:
    return sumDigits(doubleEveryOther(toDigits(int))) % 10 == 0

# An immutable PVector is created from mapping the isValid function to the list
# of potential credit card numbers.
def testCC() -> PVector[bool]:
    print(pvector(map(isValid, [1234567890123456, 1234567890123452])))

testCC()
