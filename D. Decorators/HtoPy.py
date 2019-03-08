from itertools import count, islice, tee
from typing import Any, Iterable, Iterator, List, TypeVar
T = TypeVar("T")

def take_all_at_once(n: int, iterable: Iterable[T]) -> List[T]:
    """ Return first n items of iterable as a list  """
    result = [next(iterable) for _ in range(n)]
    return result

def take_one_at_a_time(n: int, iterable: Iterable[T]) -> Iterator[T]:
    """ Return first n items of iterable as an Iterable """
    result = islice(iterable, n)
    return result

z = 0

def sieve(k:int, inp:Iterable[int])->Iterable[int]:
#    print('Initial', k)
#    p = z
#    print('Outer P', p)
    while 1:
 #       if z != p:
 #           print('Inner P', p)
 #           print('Z', z)
 #           print('Subsequent', k)
        n = next(inp)
#        print(n)
        is_prime = n%k != 0
        print("sieve",k,'passes' if is_prime else 'blocks', n)
        if is_prime:
            yield n

def primes() -> Iterable[int]:
    odd_ints = count(3,2)
    while 1:
        n = next(odd_ints)
        print("\n{} is prime\n".format(n))
        yield n
        test, odd_ints = tee(sieve(n,odd_ints))
#        global z
#        z += 1
##        print(next(test))

primes_a = take_all_at_once(10, primes())
primes_b = take_one_at_a_time(10, primes())
compare = '==' if primes_a == primes_b else '!='
print(f'\nprimes_a {compare} primes_b')
print(f'primes_a: {primes_a}')
print(f'primes_b: {primes_b}')

# Test statements were ran to check how is both function is running

# The two functions are running in tandem (primes and sieve). Primes is called first and prints out 3 then passes it onto
# sieve function where it is taking in n and the iterable odd_ints. The sieve function will check if the integer
# n being passed from iterable odd_ints is prime or not. If it is, the print statement will say passes, else it is false.
# Checks if isPrime true or not and yields n and stops the execution. Once it stops the execution, it moves back into primes and grabs
# next(odd_ints). This process continues from all prime number checking the new n number that could be a potential prime number. If
# it blocks, then it ignores the number n that is not prime and moves onto the next n. It does not yield n and it is all done in
# the sieve statement then passes to primes once it is done checking.
# prime_b prints out a memory location instead of a list like primes_a because take_one_at_a_time function does not have a list wrapper
