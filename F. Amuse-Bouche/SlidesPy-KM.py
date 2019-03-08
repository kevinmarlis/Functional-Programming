from datetime import date, timedelta
from toolz import first, drop, second

def firstOne(list):
    if len(list) > 0:
        return first(list)
    else: pass

print(firstOne([1,2,3]))



def findAfterElem(m, rest):
    while len(rest) > 1:
        if first(rest) == m:
            return second(rest)
        else: rest = list(drop(1,rest))

print(findAfterElem(2, [1,2,3,4]))



# Two cases for interestingDates:
# interestingDates = []
interestingDates = [date(1966, 9, 8), date(1969, 6, 21), date(1969, 10, 29)]

def addAWeek(day):
    if day:
        return day + timedelta(days=7)
    else: return None

def anInterestingDate():
    if interestingDates:
        return firstOne(interestingDates)
    else: return None

def maybeAddAWeek(date):
    return addAWeek(date)

def aWeekLater():
    return maybeAddAWeek(anInterestingDate())

print(anInterestingDate())
print(aWeekLater())


# Slide 45:
tvShows = [(1966, "Star Trek"), (1969, "Monty Python's Flying Circus"),
    (1989, "The Simpsons")]

def showForYear(year):
    for show in tvShows:
        if first(show) == year:
            return second(show)
    else: return None

def showWithName(name):
    shows = filter(lambda s: name in s, list(map(lambda s: second(s), tvShows)))
    if shows:
        return first(shows)
    else: return None

print(showWithName("S"))

def favoriteShow(name):
    if name == "Amy":
        return "Batman"
    elif name == "Bob":
        return "Iron Chef"
    else: return None

class Person:
    def __init__(self, name, year):
        self.name = name
        self.year = year

amy = Person("Amy", 1971)
cam = Person("Cam",1989)
deb = Person("Deb", 1969)
monty = Person("Monty", 1973)


def pickShow(person):
    return favoriteShow(person.name) or showWithName(person.name) or showForYear(person.year)

print(pickShow(amy))
