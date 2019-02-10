-- Returns the rounded, integer square root of an integer
iSqrt :: (Integral b, Integral a) => a -> b
iSqrt n = round (sqrt (fromIntegral n))

-- Checks if an integer is a perfect square
isASquare :: Integral a => a -> Bool
isASquare n = (iSqrt n) ^ 2 == n

-- Checks if an integer is prime
isPrime :: Integer -> Bool
isPrime n = n `elem` takeWhile (<= n) primes

-- Returns a list of integers that divide an integer
smallPrimeDivisors :: Integer -> [Integer]
smallPrimeDivisors n = [d | d <- takeWhile (\x -> x^2 <= n) primes, n `mod` d == 0]

-- Creates a list of all integers. Will need to use takeWhile when calling to
-- avoid an infinite list
primes :: [Integer]
primes = 2 : [n | n <- [3,5..], null (smallPrimeDivisors n)]

-- Returns a list of primes that satisfy Goldbach's equation (g = p + 2 * k^2) by
-- looking for a prime such that (g - p) `div` 2 is a square
primesThatSatisfy :: Integer -> [Integer]
primesThatSatisfy g = [p | p <- takeWhile (< g) primes, isASquare((g-p) `div` 2)]

-- Returns a list of all odd numbers that are not prime. Will need to use
-- takeWhile when calling to avoid an infinite list
oddComposites :: [Integer]
oddComposites = [n | n <- [3,5..], not (isPrime n)]

-- Returns a list of numbers that disprove Goldbach's other conjecture. Only two
-- numbers are known to disprive (5777, 5993) but function needs to be called using
-- 'take' to avoid an infinite list.
goldbach :: [Integer]
goldbach = [g | g <- oddComposites, null (primesThatSatisfy g)]

--0.47 seconds, 290,031,288 bytes
