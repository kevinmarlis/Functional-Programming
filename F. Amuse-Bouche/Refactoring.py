from functools import reduce
from typing import List, Tuple

#
# Iterate through the indices
#
def doubleAndSum_1a(xs: List[int]) -> int:
    """
    indexed loop
    local variables: i, acc.
    """
    (acc, i) = (0, 0)
    while i < len(xs):
        (acc, i) = (acc + (i%2 + 1) * xs[i], i+1)
    return acc

# Note: (1 if i%2==0 else 2) == (0 if i%2==0 else 1) + 1 == i%2 + 1

def doubleAndSum_1b(xs: List[int]) -> int:
    """
    use a for statement
    local variables: i, acc.
    """
    acc = 0
    for i in range(len(xs)):
        acc += (i%2 + 1) * xs[i]
    return acc

def doubleAndSum_1c(xs: List[int]) -> int:
    """
    recursion
    local variables: i, acc.
    """

    def doubleAndSum_1c_aux(acc, i) -> int:
        if i >= len(xs):
            return acc
        return doubleAndSum_1c_aux(acc + (i%2 + 1) * xs[i], i+1)

    return doubleAndSum_1c_aux(0, 0)

def doubleAndSum_1d(xs: List[int]) -> int:
    """
    reduce
    local variables: i, acc.
    """
    result = reduce(lambda acc, i: acc + (i%2 + 1) * xs[i], range(len(xs)), 0)
    return result

def doubleAndSum_1e(xs: List[int]) -> int:
    """
    comprehension and sum
    local variables: i.
    """
    total = sum( (i%2 + 1) * xs[i] for i in range(len(xs)) )
    return total

#
# Iterate through the indices two steps at a time,
#
def doubleAndSum_2a1(xs: List[int]) -> int:
    """
    two elements of xs at a time
    local variables: i, acc.
    """
    (acc, i) = (0, 0)
    while i < len(xs):
        acc += xs[i]
        if i+1 < len(xs):
            acc += 2*xs[i+1]
        i += 2
    return acc

#
# Can you explain how the *'s work in the next example?
#
def doubleAndSum_2a2(xs: List[int]) -> int:
    """
    iteration with pattern matching in body
    local variables: x0, x1, xs, total.
    """
    total = 0
    while len(xs) >= 2:
        (x0, x1, *xs) = xs
        total += x0 + 2*x1
    if len(xs) == 1:
        total += xs[0]
    return total

# xs = [1,2,3,4,5]
# [a, b, *xs] = xs
# print(xs)

def doubleAndSum_2b(xs: List[int]) -> int:
    """
    two elements of xs at a time using for
    local variables: i, acc.
    """
    acc = 0
    for i in range(0, len(xs), 2):
        acc += xs[i]
        if i+1 < len(xs):
            acc +=2*xs[i+1]
    return acc

def doubleAndSum_2c1(xs: List[int], acc: int=0) -> int:
    """
    recursion without pattern matching.
    local variables: xs.
    """
    if len(xs) == 0:
        return acc
    if len(xs) == 1:
        return acc + xs[0]
    return doubleAndSum_2c1(xs[2:], acc + xs[0] + 2*xs[1])

#
# Can you explain how the *'s work in the next example?
#
def doubleAndSum_2c2(xs: List[int]) -> int:
    """
    recursion with pattern matching in signature.
    Don't have to ensure list length is even.
    local variables: x0, x1, total.
    """

    def doubleAndSum_2c2_aux(x0: int=0, x1: int=0, *xs_aux: List[int]) -> int:
        print(xs_aux)
        total = x0 + 2*x1
        if len(xs_aux) > 0:
            total += doubleAndSum_2c2_aux(*xs_aux)
        return total

    return doubleAndSum_2c2_aux(*xs)

print(doubleAndSum_2c2([1,2,3,4]))

def doubleAndSum_2d(xs: List[int]) -> int:
    """
    reduce
    local variables: i, acc
    """

    def incr_acc(acc, i):
        acc += xs[i]
        if i+1 < len(xs):
            acc += 2*xs[i+1]
        return acc

    result = reduce(incr_acc, range(0, len(xs), 2), 0)
    return result

def doubleAndSum_2e(xs: List[int]) -> int:
    """
    sum and comprehension
    local variables: i.
    """
    total = sum( xs[i] + (2*xs[i+1] if i+1 < len(xs) else 0) for i in range(0, len(xs), 2) )
    return total

#
# iteration on enumerated list (and a variant)
#
def doubleAndSum_3a(xs: List[int]) -> int:
    """
	local variables: i, enum_xs, total, x.
	"""
    total = 0
    enum_xs = list(enumerate(xs))
    while enum_xs != []:
        (i, x) = enum_xs[0]
        total += (i%2+1)*x
        enum_xs = enum_xs[1:]
    return total

def doubleAndSum_3b(xs: List[int]) -> int:
    """
	local variables: i, total.
	"""
    total = 0
    for (i, x) in enumerate(xs):
        total += (i%2+1)*x
    return total

def doubleAndSum_3c(xs: List[int]) -> int:
    """
	recursion on enumerated list
	local variables: i, total, x.
	"""

    def doubleAndSum_3c_aux(ixs: List[Tuple[int, int]], acc) -> int:
        if ixs == []:
            return acc
        (i, x) = ixs[0]
        return doubleAndSum_3c_aux(ixs[1:], acc + (i%2 + 1) * x)

    return doubleAndSum_3c_aux(list(enumerate(xs)), 0)

def doubleAndSum_3d(xs: List[int]) -> int:
    """
	reduce on enumerated list
	local variables: i, x, acc.
	"""

    def incr_acc(acc, ix):
        (i, x) = ix
        acc += (i%2 + 1) * x
        return acc

    result = reduce(incr_acc, enumerate(xs), 0)

    return result

def doubleAndSum_3e1(xs: List[int]) -> int:
    """
	comprehension and sum on enumerated list
	local variables: i, x.
	"""
    total = sum( (i%2+1)*x for (i, x) in enumerate(xs) )
    return total

from itertools import cycle
def doubleAndSum_3e2(xs: List[int]) -> int:
    """
    comprehension and sum on a function of list
    local variables: i, x.
    """
    total = sum( i*x for (i, x) in zip(cycle([1, 2]), xs) )
    return total

# Note: map(fn, xs, ys) is the same as zipWith(fn, xs, ys).
# Python doesn't have (and doesn't need) a pre-defined zipWith.
from operator import mul
def doubleAndSum_4a1(xs: List[int]) -> int:
    """
    combination of sum and map
    local variables: none.
    """
    total = sum( map(mul, cycle([1, 2]), xs) )
    return total

# Define some useful functions.
def ident(x):
    return x

def double(x):
    return 2 * x

def apply(f, x):
    return f(x)

def doubleAndSum_4a2(xs: List[int]) -> int:
    """
    combination of sum and map
    local variables: none.
    """
    total = sum( map(apply, cycle([ident, double]), xs) )
    return total

from operator import add
def doubleAndSum_4b1(xs: List[int]) -> int:
    """
    combination of reduce and map
	local variables: none.
	"""
    total = reduce(add, map(mul, cycle([1, 2]), xs), 0)
    return total

def doubleAndSum_4b2(xs: List[int]) -> int:
    """
    combination of reduce and map
	local variables: none.
    """
    total = reduce(add, map(apply, cycle([ident, double]), xs), 0)
    return total

#
# Construct our own framework function
#
def transformAndReduce(reduceBy, transformFns, xs):
    """
    Apply the transformFns to the xs and reduce the result by reduceFn.
	local variables: none.
    """
    total = reduce(reduceBy, map(apply, transformFns, xs), 0)
    return total

def doubleAndSum_5(xs: List[int]) -> int:
    """
	a more general reduction
	local variables: none.
	"""
    total = transformAndReduce(add, cycle([ident, double]), xs)
    return total


doubleAndSums = [doubleAndSum_1a, doubleAndSum_1b, doubleAndSum_1c, doubleAndSum_1d, doubleAndSum_1e,
                 doubleAndSum_2a1, doubleAndSum_2a2,
                                   doubleAndSum_2b,
                                   doubleAndSum_2c1, doubleAndSum_2c2,
                                   doubleAndSum_2d, doubleAndSum_2e,
                 doubleAndSum_3a, doubleAndSum_3b, doubleAndSum_3c, doubleAndSum_3d,
                                  doubleAndSum_3e1, doubleAndSum_3e2,
                 doubleAndSum_4a1, doubleAndSum_4a2,
                                   doubleAndSum_4b1, doubleAndSum_4b2,
                 doubleAndSum_5]



# if __name__ == '__main__':
#     from random import choice, randint
#
#     numlists = [[randint(0, 100) for _ in range(listSize)] for listSize in range(21)]
#     for numlist in numlists:
#         selectedDAndS = choice(doubleAndSums)
#         referenceAnswer = selectedDAndS(numlist)
#         print( f'\n{selectedDAndS.__name__}({numlist}) = {referenceAnswer}' )
#         otherAnswers = [dAndS(numlist) for dAndS in doubleAndSums if dAndS is not selectedDAndS]
#         if all( referenceAnswer == eachAnswer for eachAnswer in otherAnswers ):
#             print('All the same.')
#         else:
#             discrepancies = [f'{dAndS.__name__}({numlist}) = {dAndS(numlist)}' for dAndS in doubleAndSums
#                                                                                if dAndS(numlist) != referenceAnswer]
#             for discrepancy in discrepancies:
#                 print(discrepancy)
