from math import sqrt
from time import time

# Checks if an int is a perfect square by checking if the rounded square root
# is equivalent to the original int
def isASquare(n: int) -> bool:
    return round(sqrt(n))**2 == n

# Checks if an int is prime, first by seeing if the int is an even number greater
# than 2. Otherwise it checks for any odd divisors smaller than the square root
# of the int. As soon as something evenly divides the int, true is returned
def is_prime(n: int) -> bool:
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(sqrt(n)) + 1, 2))

# Returns a list of primes ranging from 2 through 6000
def primes() -> [int]:
    return [2] + [n for n in range(3, 6000, 2) if is_prime(n)]

# Returns a list of odd composite numbers between 3 and 6000
def odd_composites() -> [int]:
    return [n for n in range(3, 6000, 2) if not is_prime(n)]

# Returns whether or not there are any primes that satisfy goldbach's
# equation. As soon as there is, true is returned.
def primes_that_satisfy(g: int, primeNumbers: [int]) -> bool:
    return any(p for p in primeNumbers if p < g and isASquare((g-p)//2))

# Maintains a list of ints that disprove goldbach's other conjecture by
# iterating through odd composite numbers
# Takes argument for number of fails to include in output list
def goldbach_fails(n: int) -> [int]:
    fails = []
    primeNumbers = primes()
    oddNotPrimes = odd_composites()

    while len(fails) < n:
        for g in oddNotPrimes:
            if not primes_that_satisfy(g, primeNumbers):
                fails.append(g)
    return fails

results = 0


for _ in range(10):
    start = time()
    goldbach_fails(2)
    end = time()
    results += end - start

print(results/10)
