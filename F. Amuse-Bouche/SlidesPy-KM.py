from typing import Optional, List, Tuple, Sized, Any, Union
from datetime import date, timedelta
from toolz import first, drop, second, last, accumulate, compose
from toolz.curried import *
from operator import add
from itertools import count, islice
from functools import singledispatch, update_wrapper
from types import GeneratorType

"""
Slides 43 - 44
"""

# Two cases for interestingDates:
# interestingDates = []
interestingDates = [date(1966, 9, 8), date(1969, 6, 21), date(1969, 10, 29)]

def firstOne(list):
    return first(list) if len(list) > 0 else None

def addAWeek(day: Optional[date]) -> Optional[date]:
        return day + timedelta(days=7) if day else None

def anInterestingDate() -> Optional[date]:
        return firstOne(interestingDates) if interestingDates else None

def maybeAddAWeek(date: Optional[date]) -> Optional[date]:
    return addAWeek(date)

def aWeekLater() -> Optional[date]:
    return maybeAddAWeek(anInterestingDate())

print("AWeekLater: ", anInterestingDate(), "->", aWeekLater())

"""
Slide 45 - 46 (Short circuit <|> python and bind >>= implementation using
operator overloading)
"""
# Class used to overload operators
class Show:
    def __init__(self, func):
        self.func = func
        update_wrapper(self, func)

    # Overload the | operator for short-circuit
    def __or__(self, other):
        return lambda *args, **kw: self.func(*args, **kw) if self.func(*args, **kw) else other(*args, **kw)

    # Overload the // operator for bind
    def __floordiv__(self, other):
        return lambda *args, **kw: other(self.func(*args, **kw)) if self.func(*args, **kw) else None

    def __call__(self, *args, **kw):
        return self.func(*args, **kw)

class Person:
    def __init__(self, name, year):
        self.name = name
        self.year = year

amy: Person = Person("Amy", 1971)
cam: Person = Person("Cam",1989)
deb: Person = Person("Deb", 1969)
monty: Person = Person("Monty", 1973)

tvShows : List[Tuple[int, str]] = [(1966, "Star Trek"),
    (1969, "Monty Python's Flying Circus"), (1989, "The Simpsons")]

# @Show decorator allows the functions to be applied to the overloaded operators
@Show
def showForYear(person) -> Optional[str]:
    for show in tvShows:
        if first(show) == person.year:
            return second(show)
    else: pass

@Show
def showWithName(person) -> Optional[str]:
    shows = list(filter(lambda s: person.name in s, list(map(lambda s: second(s), tvShows))))
    return first(shows) if shows else None

@Show
def favoriteShow(person) -> Optional[str]:
    if person.name == "Amy":
        return "Batman"
    elif person.name == "Bob":
        return "Iron Chef"
    else: pass

# Example showing short circuiting or
def pickShow(person) -> Optional[str]:
    return (favoriteShow | (showForYear | showWithName))(person)

# Example showing bind operator
@Show
def loveShows(str) -> Optional[str]:
    return str + " is my favorite show!" if str else None

def showBuilder(person) -> Optional[str]:
    return (favoriteShow // loveShows)(person)

print("PickShow: ", pickShow(deb))
print("Show Builder: ", showBuilder(amy))

"""
Slide 47 (fmap implementation using singledispatch decorator)
"""

# singledispatch dispatches based on the type of the first argument
@singledispatch
def fmap(functor, func):
    pass

@fmap.register(list)
def _(functor, func):
    return [func(elem) for elem in functor]

@fmap.register(tuple)
def _(functor, func):
    return tuple((func(elem) for elem in functor))

@fmap.register(str)
def _(functor, func):
    return ''.join((func(char) for char in functor))

@fmap.register(set)
def _(functor, func):
    return {func(elem) for elem in functor}

@fmap.register(dict)
def _(functor, func):
    return {k: func(v) for k, v in functor.items()}

@fmap.register(GeneratorType)
def _(functor, func):
    for elem in functor:
        yield func(elem)

@fmap.register(range)
def _(functor, func):
    for elem in functor:
        yield func(elem)

print("None:", fmap(None, lambda x: x + 1))
print("String:", fmap([1,2,3], lambda x: x + 1))
print("Tuple:", fmap((1,2,3), lambda x: x + 1))
print("Set:", fmap({1,2,3}, lambda x: x + 1))
print("Dict:", fmap({1:1,2:2,3:3}, lambda x: x + 1))
print("Str:", fmap("Hello", lambda x: x.upper()))
print("Range:", list(fmap(range(15), lambda x: x + 1)))

def countdown(num):
    while num > 0:
        yield num
        num -= 1

print("Generator:", list(fmap(countdown(10), lambda x: x + 1)))

"""
Slides 50 - 53 (There are testing libraries for Python, but they aren't included
here. Hypothesis and Pytest-quickcheck are some.)
"""
# Function that encodes lengths of runs of characters. Returns tuple of
# character and run length.
def runLengthEncode(lst: Union[List, str]) -> List[Tuple[Any, int]]:
    n: int = 1
    newList: List = []
    while len(lst) > 0:
        if len(lst) == 1:
            newList.append((first(lst), n))
            return newList
        elif first(lst) == second(lst):
            n += 1
            lst = list(drop(1,lst))
        else:
            newList.append((first(lst), n))
            lst = list(drop(1,lst))
            n = 1
    return newList

print("RLE:", runLengthEncode(["a", "a", "b", "a", "a"]))

# Function that checks if runLengthEncode has the property of maintaining the
# length of the input
def rlePropLengthPreserved(ints: List) -> bool:
    return len(ints) == last(accumulate(add, [b for a,b in runLengthEncode(ints)]))

print("Legnth Preserved:", rlePropLengthPreserved(["a", "a", "b", "a", "a"]))

# Function that checks if runLengthEncode has the property of returning the
# correct length of a run
def rlePropDupesCollapsed(n: int) -> bool:
    if n % 100 == 0:
        return runLengthEncode("") == []
    else:
        return runLengthEncode(['x']*(n % 100)) == [('x', n % 100)]

print("Dupes Collapsed:", rlePropDupesCollapsed(175))

# Function that checks if runLengthEncode returns the same list of run length
# tuples when passed that list of tuples
def rlePropRoundTrip(lst: List) -> bool:
    # iS: ord('a') returns Unicode (97), count starts an iterator at 97, map maps each
    # yielded element of the iterator to chr. islice takes a len(lst) slice from
    # the iterator, zips it with the lambda function mapping on the list, and
    # returns the list of that zip.
    iS: List = list(zip(
        islice(compose(map(chr), count, ord)('a'), len(lst)),
        map(lambda x: (x % 100) + 1, lst)))
    # xs: the list comprehension repeats the charater, the second element of the tuple
    # times, for each tuple in iS. The resulting list is then made into a string
    xs: str = "".join([first(x) * second(x) for x in iS])
    return runLengthEncode(xs) == iS

print("Round Trip:", rlePropRoundTrip([3,2,2,2,1,1,2,1]))
