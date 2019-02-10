from typing import List, Callable, Any
import operator, itertools

def myZipWith(function: Callable, listA: List, listB: List) -> List:
    return [function(a,b) for (a,b) in zip(listA, listB)]

print(myZipWith(operator.add, [1, 2, 3], [1, 2, 3]))



def myFoldl(func: Callable, accum, list: List):
    it = iter(list)
    if accum is None:
        value = next(it)
    else:
        value = accum
    for elem in it:
        value = func(value, elem)
    return value

print(myFoldl(operator.add, 1, [1,2,3,4,5]))

# This results in an infinite list
def myCycle(list: List) -> List:
    while True:
        for elem in list:
            yield elem

# This call does not immediately make an infinite loop because of Python's laziness
# with generators
# https://swizec.com/blog/python-and-lazy-evaluation/swizec/5148
cyc12 = myCycle([1,2])

# This returns a generator, so it needs to be made into a
# Again, this doesn't create an infinite loop because of the use of islice.
print(list(itertools.islice(cyc12, 5)))


def myWhile(x: Any, func1: Callable, func2: Callable, func3: Callable):
    if (func1(x)):
        myWhile(func2(x), func1, func2, func3)
    else:
        return (func3(x))

def boolFunc(x, n):
    return x[0] < n

def updateFunc(x):
    x[0] = x[0] + 1
    return x[0]^2 + x[1]

def reverseFunc(x):
    return x[1].reverse()


def nSquares(n):
    return while((1, []), boolFunc(x, n), updateFunc(x), reverseFunc(x))
