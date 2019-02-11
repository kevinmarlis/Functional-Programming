from typing import List, Callable, Any
import operator, itertools, math

def myZipWith(function: Callable, listA: List, listB: List) -> List:
    return [function(a,b) for (a,b) in zip(listA, listB)]

print("myZipWith: ", myZipWith(operator.add, [1, 2, 3], [1, 2, 3]))


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
print("myCycle: ", list(itertools.islice(cyc12, 5)))

# Function Pairs

def functionPairsA(func, list):
    return [(x, func(x)) for x in list]
print("functionPairsA: ", functionPairsA((lambda x: x + 1), [1,2,3]))

def functionPairsB(func, lst):
    return list(map(lambda x : (x, func(x)), lst))
print("functionPairsB: ", functionPairsB((lambda x: x + 1), [1,2,3]))

def functionPairsC(func, lst):
    return list(zip(lst, map(lambda x: func(x), lst)))
print("functionPairsC: ", functionPairsC((lambda x: x + 1), [1,2,3]))


# While Loops


def myWhile(x: Any, boolFunc: Callable, updateFunc: Callable, resultsFunc: Callable) -> Any:
    if (boolFunc(x)):
        return myWhile(updateFunc(x), boolFunc, updateFunc, resultsFunc)
    else:
        return (resultsFunc(x))


# Squares using while


def updateFunction(x: Any) -> Any:
    x[1].insert(0, x[0] ** 2)
    x[0] = x[0] + 1
    return x

def returnFunction(x: Any) -> Any:
    x[1].reverse()
    return x[1]

# The while function takes four arguments: a list of two elements (index, and an empty list), a boolean check function
# an update function and a return function. 
def nSquares(n: int) -> [int]:
    return myWhile([1, []], (lambda x: x[0] <= n), (lambda x : updateFunction(x)), (lambda x: returnFunction(x)))

print("While loop squares: ", nSquares(10))


# Map using while


def updateFunctionMyMap3(x: Any, func: Callable) -> Any:
    x[1].insert(0, func(x[0]))
    x[0] = x[0] + 1
    return x

def returnFunctionMyMap3(x: Any) -> Any:
    x[1].reverse()
    return x[1]

def myMap3(func: Callable, list: List) -> List:
    return myWhile([1, []], (lambda x: x[0] <= len(list)), (lambda x : updateFunctionMyMap3(x, func)), (lambda x : returnFunctionMyMap3(x)))

print("While loop map: ", myMap3((lambda x: x + 1), [1,2,3]))


# Foldl using while


def updateFunctionWhileFoldl(x: Any, func: Callable) -> Any:
    x[1] = func(x[0], x[1])
    x[0] = x[0] + 1
    return x

def returnFunctionWhileFoldl(x: Any) -> Any:
    return x[1]

def whileFoldl(func: Callable, accum: int, list: [int]) -> int:
    return myWhile([1, accum], (lambda x: x[0] <= len(list)), (lambda x : updateFunctionWhileFoldl(x, func)), (lambda x : returnFunctionWhileFoldl(x)))

print("While loop Foldl: ", whileFoldl((lambda x, y: x * y), 1, [1,2,3,4,5]))


# Fibonacci using while


def updateFunctionFibs(x: Any) -> Any:
    if (x[0] == 0 or x[0] == 1):
        x[1].insert(0, 1)
    else:
        x[1].insert(0, (x[1][0] + x[1][1]))
    x[0] = x[0] + 1
    return x

def returnFunctionFibs(x: Any):
    x[1].reverse()
    return x[1]

def whileFibs(index: int) -> [int]:
    return myWhile([0, []], (lambda x: x[0] < index), (lambda x : updateFunctionFibs(x)), (lambda x : returnFunctionFibs(x)))

print("While loop Fibonacci: ", whileFibs(10))


# Primes using while


def updateFunctionPrimes(x: Any) -> Any:
    if x[0] % 2 != 0:
        if not [p for p in x[1] if x[0] % p == 0]:
            x[1].insert(0, x[0])

    x[0] = x[0] + 1
    return x

def returnFunctionPrimes(x: Any) -> Any:
    x[1].reverse()
    return x[1]

def whilePrimes(index: int) -> [int]:
    return myWhile([2, []], (lambda x : len(x[1]) < index), (lambda x : updateFunctionPrimes(x)), (lambda x : returnFunctionPrimes(x)))

print("While loop primes: ", whilePrimes(10))
