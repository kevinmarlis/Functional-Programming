from math import sqrt

class Monad:
    # unit :: a -> M a
    # called return (somewhat confusingly) by Hutton and Lipovaca.
    # But that’s the standard term in Haskell.
    # Also called pure.
    @staticmethod
    def unit(x):
        raise Exception("unit method needs to be implemented")

    # bind :: M a -> (a -> M b) -> M b
    # generally represented by the infix operator >>=
    def bind (self, f):
        raise Exception("bind method needs to be implemented")

class Maybe(Monad):
    # unit :: a -> Maybe a
    @staticmethod
    def unit(x):
        return Just(x)

    # bind:: Maybe a -> (a -> Maybe b) -> Maybe b
    def bind (self, f):
        return f(self.value) if self.defined else Nothing()

class Just(Maybe):
    def __init__(self, value):
        self.value = value
        self.defined = True

class Nothing(Maybe):
    def __init__(self):
        self.value = None
        self.defined = False


def safeSqrt(x):
    if x < 0:
        return Nothing()
    else:
        return Just(sqrt(x))

def testSafeSqrt0(x):
    return safeSqrt(x).bind(safeSqrt)

def testSafeSqrt1(x):
    y = safeSqrt(x)
    if y.defined:
        return safeSqrt(y.value)
    else:
        return y

def testEq0(a, b):
    return all(testSafeSqrt0(x).value == testSafeSqrt1(x).value for x in range(a,b))

# FIX
def testEq1(a,b):
    return all([testSafeSqrt0(x).value == testSafeSqrt1(x).value for x in range(a,b)])

def testEq2(a,b):
    return reduce([testSafeSqrt0(x).value == testSafeSqrt1(x).value for x in range(a,b)], operator.and_ , True)

print(testEq1(-5,5))
