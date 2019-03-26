from functools import reduce, wraps
from typing import Any, Callable, List, Tuple, TypeVar

# Road derives from type. Type is a metaclass, so Road is a metaclass. A metaclass
# is basically the class of a class, defining how that class behaves.
class Road(type):
    """
    There are three Roads (i.e., Road Types) in the problem: A, B, and C.

    Each Road Type is both an instance of the type Road as well as a class with its own (Segment) instances.

    The Road type itself, i.e., this class, is considered a metatype (and is a subtype of type) because it
    has types (A, B, and C) as instances.

    Roads are divided into Segments. We use the types A, B, and C when we declare those instances,
    i.e., theose Segments. The A-Road and B-Road Segments are each connected to each other.
    The Segments of the C road are not connected to each other.

    The Segment type enables us to talk about all segments as instances of a common type, i.e., the Segment type.
    To do that we make the Segment type a supertype of each of the Road types.

    The Road type also defines __str__ on Segments. This could also be done at the Segment level.
    """
    def __str__(cls):
        return cls.__name__

# Explicitly defines Segment's metaclass to be Road rather than the default type.
# The metaclass works as a template for class creations.
class Segment(metaclass=Road):
    """
    The Segment class is an artifical class used to represent the common features of Segments of the
    three Road types.

    As indicated above, each Road type is an instance of the metatype Road. (Road is a metatype because
    it has types, i.e., classes, as instances.

    Segment has three subtypes: A, B, and C.

    Since each Road type is an instance of the type Road, a Segment is also an instance of the type Road.
    In other words, a Segment is both an instance of Road and a type for Segment instances.

    Each Segment instance has a distance.
    """

    def __init__(self, dist: int):
        self.dist = dist

    def __str__(self):
        """
        This defines the string representation of a segment, i.e., A/5.
        (The format is the same as in the Haskell code.)

        Note: In the following, type(self) is the class itself, i.e., A, B, or C.
        When we call str(type(class)) we access __str__ in Road.
        The result is the same as calling type(self).__name__
        """
        return f'{str(type(self))}/{self.dist}'


class A(Segment):
    """
    This class itself is an instance of the metaclass Road.

    This class also has instances, each of which is a Segment.

    Similarly for the B and C classes.
    """
    def __init__(self, dist: int):
        super().__init__(dist)

class B(Segment):
    """
    A segment of the B road.
    """

    def __init__(self, dist: int):
        super().__init__(dist)

class C(Segment):
    """
    A segment of the C road.
    """

    ...   # This is like pass


class Path:

    # Methods that begin and end with double underscores are defined and used at the Python level.
    def __init__(self, startingRoad: Road, endingRoad: Road, steps: List[Segment]):
        """
        Here we are using Road objects as parameters. Those Road objects are instances of
        the metatype Road.
        """
        self.startingRoad = startingRoad
        self.endingRoad = endingRoad
        self.steps = steps

    def __add__(self, otherPath: 'Path') -> 'Path':
        """
        The method that implements to the (+) operator for this class.
        """
        return Path(self.startingRoad, otherPath.endingRoad, self.steps + otherPath.steps)

    def __str__(self) -> str:
        """
        The method that returns the common printable form of instances for this class.
        It's like toString() and Java and show() in Haskell.
        """
        st = f'{self.startingRoad}->{self.endingRoad}. Dist: {self._dist()}. ' + \
             listToString(self.steps, start='', end='')
        return st

    # Methods that begin with single underscores are taken by convention to be private.
    def _dist(self) -> int:
        return sum( (step.dist for step in self.steps) )

    def _numSteps(self):
        return len(self.steps)

    # This method is taken as the equivalent of public.
    def figureOfMerit(self) -> Tuple[int, int]:
        """
        When comparing two paths, the one with the shorter distance is better.
        If they have the same distance, the one with the fewer steps is better.
        This function returns a value that can be compared to that of other Paths.
        """
        return (self._dist(), self._numSteps())


class QuadPaths:
    """
    The shortest Paths from A and B to A and B in all combinations.

    The class name is plural because each instance contains four Paths.
    """

    def __init__(self, paths: List[Path]):
        self.paths = paths

    def __str__(self) -> str:
        st = listToString(self.paths, start='QuadPaths:\n    ', sep='\n    ', end='')
        return st

# T2 can be any type
T2 = TypeVar('T2')
def trace(func: Callable[..., T2]) -> Callable[..., T2]:
    """
    Print the function signature and return value.
    Adapted from the @debug decorator of Hjelle, Primer on Python Decorators
    (https://realpython.com/primer-on-python-decorators/#debugging-code)
    """
    # https://docs.python.org/2/library/functools.html
    @wraps(func)
    def wrapper_trace(*args: List[Any], **kwargs: List[Any]) -> T2:
        # make list of strings of args
        args_str = [str(a) for a in args]
        # make list of strings of k=v for each entry in kwargs
        kwargs_str = [f'{k}={str(v)}' for (k, v) in kwargs.items()]
        # makes string from list by concatenating the above, using \n to start, end,
        # and delimite each item in the list
        fullArgsStr = listToString(args_str + kwargs_str, start='\n', sep=',\n', end='\n')
        print(f'\nCalling {func.__name__}({fullArgsStr})')
        # value = the return of calling the actual function
        value = func(*args, **kwargs)
        # uses custom listToString if list, otherwise use class defined __str__
        valueStr = str(value) if type(value) is not list else listToString(value, start='', sep=',\n', end='\n')
        print(f'{func.__name__} returned: \n{valueStr}\n')
        return value

    # Prints the trace info from wrapper_trace and returns actual return from func
    return wrapper_trace

def bestPath(startingRoad: Road, endingRoad: Road, qp1: QuadPaths, qp2: QuadPaths) -> Path:
    """
    Find the pair of Paths from qp1 and qp2 such that:
      o the qp1 Path starts at the startingRoad;
      o the qp2 Path starts where the qp1 Path ends;
      o the qp2 Path ends at the endingRoad.
      o the combined Path is the shortest such combination.

    Join those two Paths into a single combined Path and return that combined Path.

    Note: (+) is defined for Path to join two Paths into a new Path.
    See Path.__add__().
    """
    paths = [p1 + p2 for p1 in qp1.paths if p1.startingRoad == startingRoad
                     for p2 in qp2.paths if p1.endingRoad == p2.startingRoad and p2.endingRoad == endingRoad]

    # Python is smart enough to know that Path.figureOfMerit is a method of the Path class
    # and should be applied to a path p as p.figureOfMerit()

    # sorted() returns a new list and takes an iterable, optional key for basing
    # comparison, and optional bool for reverse. sortd[0] returns the first path
    # of the sorted list which is the "best" (shortest/least steps) path
    sortd = sorted(paths, key=Path.figureOfMerit)
    return sortd[0]

# @trace wraps joinQuadPaths in the trace wrapper
@trace
def joinQuadPaths(qp1: QuadPaths, qp2: QuadPaths) -> QuadPaths:
    """
    Joins two adjacent QuadPaths objects into a combined QuadPaths object.
    """
    # list comp applying bestPath to each possible start and end combination on
    # the two adjoining QuadPaths. A QuadPath is constructed from the list
    joinedQuadPaths = QuadPaths([bestPath(s, e, qp1, qp2) for s in [A, B] for e in [A, B]] )
    return joinedQuadPaths

# T1 can be any type
T1 = TypeVar('T1')
def listToString(aList: List[T1], start='[', sep=', ', end=']') -> str:
    """
    A utility that allows one to add start and end strings to a joined string.
    The default is to use '[' and ']' as start and end as a way to print lists.
    """
    return start + sep.join([str(elt) for elt in aList]) + end

#
def optimalPath(allSegs: List[int]) -> Path:
    """
    Returns a Path with the shortest dist from Heathrow to London.

    The allSegs input is a list of Road segment distances. Even though it is a flat
    list of ints, allSegs should be understood in groups of three: A segment, B segment, C segment.
    """
    qpList = toQPList(allSegs)
    # Join the QuadPaths together and then extract the final paths.
    heathrowToLondonPaths = reduce(joinQuadPaths, qpList).paths
    # min takes an iterable, optional additional iterables, optional key for basing
    # comparison, optional default if iterable is empty
    return min(heathrowToLondonPaths, key=Path.figureOfMerit)

def segsToQP(aDist: int, bDist: int=0, cDist: int=0) -> QuadPaths:
    """
    Convert three segment distances into a QuadPaths.
    """
    # for each of the four paths that makes up a QuadPaths, the passed in segment
    # distance is used to create the respective A, B, or C, as a list of the
    # segments needed to get from start to end. The Path is then created by passing
    # in the start, end, and list of steps.
    return QuadPaths([Path(A, A, [A(aDist)]),             # A -> A
                      Path(A, B, [A(aDist), C(cDist)]),   # A -> B
                      Path(B, A, [B(bDist), C(cDist)]),   # B -> A
                      Path(B, B, [B(bDist)])              # B -> B
                      ])

# Allows trace wrapper
@trace
def toQPList(allSegs: List[int]) -> List[QuadPaths]:
    """
    Convert a list of Segment distances into a list of QuadPaths.

    If len(allSegs)%3 != 0, assumes additional segments of length 0.

    Doing it iteratively rather than recursively so that @trace will be called only once.
    """
    qpList: List[QuadPaths] = []
    while len(allSegs) > 0:
        # Uses qpList and allSegs mutably
        # Do you understand how the arguments to segsToQP are passed?

        # segsToQP takes the first three segments in the list of allSegs, unpacks
        # them as arguments using * and appends the resulting QuadPaths to the qpList.
        # allSegs is then updated to be the rest of allSegs after the first three.
        qpList.append(segsToQP(*allSegs[:3]))
        # Do you understand what the following line does?
        allSegs = allSegs[3:]
    return qpList


if __name__ == '__main__':
  # The example from the book.
  dists = [50, 10, 30, 5, 90, 20, 40, 2, 25, 10, 8]
  print(optimalPath(dists))
  # => B->B. Dist: 75. [B/10, C/30, A/5, C/20, B/2, B/8],
