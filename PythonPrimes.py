from itertools import count

def primes(i):
    primes_cache = []
    yield 2
    for k in count(3, 2):
        no_divisors = not any(p for p in primes_cache if k % p == 0)      if i == 0 else \
                      not [p for p in primes_cache if k % p == 0]         if i == 1 else \
                      all(p for p in primes_cache if k % p != 0)          if i == 2 else \
                      all(k % p != 0 for p in primes_cache)               if i == 3 else \
                      (k % p != 0 for p in primes_cache)                # if i == 4
        if no_divisors:
            primes_cache.append(k)
            yield k

for i in range(5):
    print(i, [p for (_, p) in zip(range(12), primes(i))])



# Variant 0 works by checking if any of the p's in primes_cache divides k. If at least one does,
# any() will return true, meaning k is not a prime since it is divideable. Thus the not
# makes no_divisors false meaning k is not prime.

# Variant 1 works by constructing a list of all p's in primes_cache that divides k. The list
# contains numbers rather than booleans like in variant 0. If the list is not empty it will
# return a true boolean, which the not will negate.

# Variant 2 checks all() to see if the argument contains only true boolean values.
# Every p will be a true statement because Python has a boolean value of true if
# __len__() is greater than 0. So even non primes will be added to primes_cache

# Variant 3 works because the expression returns a boolean rather than the int object.

# Variant 4 does not work because it sets no_divisors to be a boolean value of true
# because it creates a genexpr object. So all values of k are added to primes_cache.
