
-- safeSqrt returns Just (sqrt x) if x >= 0. If x < 0, it returns Nothing.
safeSqrt :: Double -> Maybe Double
safeSqrt x
    | x < 0     = Nothing
    | otherwise = Just (sqrt x)


-- Two equivalent ways to execute 2 safeSqrt calls in sequence.
testSafeSqrt0 :: Double -> Maybe Double
testSafeSqrt0 x = safeSqrt x >>= safeSqrt

testSafeSqrt1 :: Double -> Maybe Double
testSafeSqrt1 x = do
                     y <- safeSqrt x
                     safeSqrt y

-- Three tests (all equivalent) to ensure testSafeSqrt0 and testSafeSqrt1 are the same
testEq0 a b = all (\x -> testSafeSqrt0 x == testSafeSqrt1 x) [a .. b]

testEq1 a b = all id [testSafeSqrt0 x == testSafeSqrt1 x | x <- [a .. b]]

testEq2 a b = foldl (&&) True [testSafeSqrt0 x == testSafeSqrt1 x | x <- [a .. b]]

-- > testEq0 (-5) 5
-- True


-- Define a function that composes two "safe" functions.
-- This is slightly different from >>=.
--
-- The type of >>= is
-- (>>=) :: Monad m => m b -> (b -> m c) -> m c
-- which takes a wrapped value and a function.
-- Here we will define a function that takes two functions and produces
-- their composition.
--
-- First let's define an infix operator (<.>) for the function. Defining it with
-- infixr 1 <.>   declares it to associate to the right and to have precedence 1.
-- Notice that (<.>) takes two functions as arguments. It returns a function
-- that takes an argument to the first function and returns the output
-- of the two functions in sequence, with the appropriate unwrapping between them.
infixr 1 <.>
(<.>) :: Monad m => (a -> m b) -> (b -> m c) -> (a -> m c)
-- Two definitions: in do notation and using explicit >>=.
-- Either one will do the job.
-- f1 <.> f2 = \x -> do y <- f1 x
--                      f2 y
f1 <.> f2 = \x -> f1 x >>= f2

-- Let's create a function that builds a safe function that takes the
-- (1/2)^n the root of its argument.
-- safeRoot 0 == Take no roots; wrap the argument in Just.
--                         (safeRoot 0) (2^1) => Just 2.0
-- safeRoot 1 == safeSqrt; (safeRoot 1) (2^2) => Just 2.0
-- safeRoot 2 == safeFourthRoot; (safeRoot 2) (2^4) => Just 2.0
-- safeRoot 3 == safeEighthRoot; (safeRoot 3) (2^8) => Just 2.0
-- safeRoot 4 == safeSixteenthRoot; (safeRoot 4) (2^16) => Just 2.0
-- safeRoot n == safeNthRoot; (safeRoot n) (2^(2^n)) => Just 2.0
-- Biuld the new function by recursive composition with safeSqrt.
-- The parentheses are not necessary since -> associates to the right.
-- They are inteded to make it clear that safeRoot takes an Int and
-- returns a function from Double to Maybe Double.
safeRoot :: Int -> (Double -> Maybe Double)
safeRoot n
    | n == 0 = Just  -- Just is a function, a type constructor. Just :: a -> Maybe a
    | otherwise = safeSqrt <.> safeRoot (n - 1)

-- Test safeRoot by asking it to generate a function (safeRoot n), which
-- when given an input should return Just 2.0
testSafeRoot :: Int -> Maybe Double
testSafeRoot n = (safeRoot n) (2^(2^n)) -- Should return Just 2.0 for any n.

-- > testSafeRoot 5
-- Just 2.0

-- Test for multiple n's. Limit to a maximum value of 9 becaues 2^(2^10)
-- is too large for a Double. Haskell can represent 2^(2^10) as an Integer,
-- but (safeRoot n) is a function that expects a Double as input.
testSafeRootTo9 :: Bool
testSafeRootTo9 = all (== Just 2) [testSafeRoot n | n <- [0 .. 9]]

-- > testSafeRootTo9
-- True
