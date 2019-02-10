from math import sqrt
from time import time

def is_a_square(n: int) -> bool:
        return round(sqrt(n))**2 == n

def is_prime(n: int) -> bool:
    if n % 2 == 0 and n > 2:
        return False
    # Anything with a remainder of 0 will return False
    return all(n % i for i in range(3, int(sqrt(n)) + 1, 2))

# takes argument for number of fails to include in output list
def goldbach_fails(bound: int) -> [int]:
    primes: [int] = [2]
    oddNumber: int = 3
    fails: [int] = []

    while len(fails) < bound:
        if is_prime(oddNumber):
            primes.append(oddNumber)
        else:
            for prime in primes:
                if is_a_square(((oddNumber-prime)//2)):
                    break
            # optional else that executes if above for loop completes without a break
            else:
                fails.append(oddNumber)
        oddNumber += 2
    return fails

print("Goldbach failures: ", goldbach_fails(2))

# Time testing using the average of 10 trials
results = 0
for _ in range(10):
    start = time()
    goldbach_fails(2)
    end = time()
    results += end - start

print("Average time: ", round(results/10, 3))
