from math import sqrt, pow
from typing import Callable
from functools import reduce
import operator
from pymonad.Maybe import *

# Dr. Abbott's cleaned up Infix "hack" from the forum
# Uses the two pipes to create an infix work around
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

# Square root function that uses the Maybe monad
def safeSqrt(x: int) -> Maybe:
    if x < 0:
        return Nothing
    else:
        return Just(sqrt(x))

# Uses PyMonad's bind function (>>) to call safeSqrt twice on a number
def testSafeSqrt0(x: int) -> Maybe:
    return safeSqrt(x) >> safeSqrt

# Another more convoluted/explicit way of doing testSafeSqrt0
def testSafeSqrt1(x: int) -> Maybe:
    if safeSqrt(x) is not Nothing:
        return safeSqrt(safeSqrt(x).value)
    else:
        return Nothing

# Test for equivalence between two tests above:

# Checks if all in comprehension checking for equivalence are true
# testEq0 a b = all (\x -> testSafeSqrt0 x == testSafeSqrt1 x) [a .. b]
def testEq0(a: int, b: int) -> bool:
    return all(testSafeSqrt0(x) == testSafeSqrt1(x) for x in range(a,b + 1))

# Checks if the values from the Maybe monad are equivalent using a sort of ID function
# testEq1 a b = all id [testSafeSqrt0 x == testSafeSqrt1 x | x <- [a .. b]]
def testEq1(a: int, b: int) -> bool:
    return all(x == x for x in [testSafeSqrt0(x).value == testSafeSqrt1(x).value for x in range(a,b + 1)])

# Uses reduce function (function, sequence, initial) on the and operator and a list comprehension of bools
# testEq2 a b = foldl (&&) True [testSafeSqrt0 x == testSafeSqrt1 x | x <- [a .. b]]
def testEq2(a: int, b: int) -> bool:
    return reduce(operator.and_, [testSafeSqrt0(x) == testSafeSqrt1(x) for x in range(a,b + 1)], True)

print("testEq0: ", testEq0(-5,5))
print("testEq1: ", testEq1(-5,5))
print("testEq2: ", testEq2(-5,5))


# Composition function used by Infix hack.
def comp(f1: Callable, f2: Callable):
    return lambda x: f2(x) >> f1

# Declare variable to be used as "operator" in Infix
c = Infix(comp)

# safeRoot works recursively to return a function. The base case (when n is 0)
# returns the function Just. Otherwise it calls itself on the decremented value.
# When the base case is reached Just is applied to 2^2^0 = 2
# It basically builds up a stack of n-1 safeSqrt calls on the initial 2^2^n value,
# always returning Just 2.
def safeRoot(n: int) -> Callable[[float], Maybe]:
    if n is 0:
        return Just
    else:
        return safeSqrt |c| safeRoot(n-1)

# helper function that calls safeRoot
def testSafeRoot(n: int) -> Maybe:
    return safeRoot(n)(pow(2, pow(2, n)))

# tester function that checks if all values return from calling testSafeRoot on
# 0-9 are Just(2)
def testSafeRootTo9():
    print("testSafeRootTo9: ", all(x == Just(2) for x in [testSafeRoot(n) for n in range(0,10)]))

testSafeRootTo9()
