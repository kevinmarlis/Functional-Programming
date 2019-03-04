from pyrsistent import pvector
from toolz import interleave, accumulate, last, concat
from operator import add

# Converts a string to an int
def toDigit(c: str) -> int:
    return int(c)

# Maps every "character" in the string to toDigit, and creates a PVector
# (immutable list) out of the resulting ints
def toDigits(int: int) -> [int]:
    return pvector(map(lambda c: toDigit(c), str(int)))

# Interleave joins a sequence of sequences by alternating between the two. Here,
# interleave is called on a list of two lists. The first list, ints[::-1][0::2],
# is made of the even indeces of the reversed "ints" list. The second is made of
# the odd indeces of the reversed "ints" list, mapped so that they are doubled,
# and made into a PVector. A single PVector is made from the interleavened sequences,
# as interleave returns a lazy iterator. Concat from toolz would also work (order
# doesn't matter since we will just sum the list), but interleave seemed more interesting.
def doubleEveryOther(ints: [int]) -> [int]:
    return pvector(interleave(
        [ints[::-1][0::2], pvector(map(lambda x: x * 2, ints[::-1][1::2]))]))

# Here, concat is used to reduce a list of lists of ints into a single list.
# Accumulate applies the add function such that the first element is added to the
# second, that value is added to the third, etc, and last returns the final sum
# of all vaues in the list.
def sumDigits(ints: [int]) -> int:
    return last(accumulate(add, concat(map(lambda c: toDigits(c), ints))))

# The int is passed to toDigits and the resulting list is passed to doubleEveryOther,
# and the resulting list is passed to sumDigits.
def checkSum(int: int) -> int:
    return sumDigits(doubleEveryOther(toDigits(int)))

# Checks if the summed value is divisible by 10.
def isValid(int: int) -> bool:
    return checkSum(int) % 10 == 0

# An immutable PVector is created from mapping the isValid function to the list
# of potential credit card numbers.
def testCC() -> [bool]:
    print(pvector(map(isValid, [1234567890123456, 1234567890123452])))

testCC()
print(pvector()[0])
