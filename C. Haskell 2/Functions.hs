myZipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
myZipWith f [] _ = []
myZipWith f _ [] = []
myZipWith f (x:xs) (y:ys) = f x y : myZipWith f xs ys

-- The order matters when there are multiple cases because of the way Haskell
-- function definitions fall through.



myFoldl :: (b -> a -> b) -> b -> [a] -> b
myFoldl f y [] = y
myFoldl f y (x:xs) = myFoldl f (f y x) xs

-- This is tail recursive because it works from left to right with no need to
-- return to finish processing.



myFoldr :: (a -> b -> b) -> b -> [a] -> b
myFoldr f y [] = y
myFoldr f y (x:xs) = f x (myFoldr f y xs)

-- This is not tail recursive because it has to return from the last element
-- before completing the previous element and so on.

-- myFoldr' requires myFlip in order to get the correct signature to use myFoldl
myFoldr' :: (a -> b -> b) -> b -> [a] -> b
myFoldr' f y xs = myFoldl (myFlip f) y $ reverse xs

myFlip :: (a -> b -> c) -> (b -> a -> c)
myFlip f = g
        where g x y = f y x



myCycle :: [a] -> [a]
myCycle xs = xs' where xs' = xs ++ xs'

-- xs ++ (xs ++ (xs ++ (xs ++ ...)))
-- Haskell's laziness keeps it from becoming an infinite loop, hence
-- no need for a base case. It will keep repeating as it is needed.

-- cyc12 = myCycle [1,2] is not an infinite loop in Haskell, again
-- because of laziness. It only generates what is needed.

-- Step by step evaluation of take 5 cyc12:
-- > take 5 cyc12
-- > take 5 (cyc12 ++ myCycle cyc 12)
-- > take 5 ([1,2] ++ myCycle [1,2])
-- > take 5 (1 : ([2] ++ myCycle [1,2]))
-- > 1 : take 4 ([2] ++ myCycle [1,2])
-- > 1 : 2 : take 3 ([] ++ myCycle [1,2])
-- > 1 : 2 : take 3 ([1, 2] ++ myCycle [1,2])
-- > 1 : 2 : take 3 (1 : ([2] ++ myCycle [1,2]))
-- > 1 : 2 : 3 : take 2 ([2] ++ myCycle [1,2])
-- > 1 : 2 : 1 : take 2 (2 : [] ++ myCycle [1,2])
-- > 1 : 2 : 1 : 2 : take 1 ([1, 2] ++ myCycle [1,2])
-- > 1 : 2 : 1 : 2 : take 1 (1 : ([2] ++ myCycle [1,2]))
-- > 1 : 2 : 1 : 2 : 1 : take 0 ([2] ++ myCycle [1,2]))
-- > 1 : 2 : 1 : 2 : 1 : []



compose :: (b -> c) -> (a -> b) -> (a -> c)
compose f g = \x -> f (g x)

-- Given g :: b -> c, f:: a -> b, and h = g `compose` f, h is the type of c
-- because g returns type c



functionPairsA :: (a -> b) -> [a] -> [(a, b)]
functionPairsA f xs = [(x,y) | x <- xs, let y = f x]
-- List comprehension making tuples

functionPairsB :: (a -> b) -> [a] -> [(a, b)]
functionPairsB f xs = map (\x -> (x, f x)) xs
-- Map where function creates tuple of element and passed function to element

functionPairsC :: (a -> b) -> [a] -> [(a, b)]
functionPairsC f xs = zip xs (map f xs)

functionPairsD :: (a -> b) -> [a] -> [(a, b)]
functionPairsD f xs = zipWith (\x y -> (x,y)) xs [f x | x <- xs]
-- lambda function to create tuples and the two lists are the xs and a comprehension
-- of the passed function applied to the xs

functionPairsE :: (a -> b) -> [a] -> [(a, b)]
functionPairsE f xs = foldr (\x xs -> [(x, f x)] ++ xs) [] xs

functionPairsF :: (a -> b) -> [a] -> [(a, b)]
functionPairsF f xs = foldl (\xs x -> xs ++ [(x, f x)]) [] xs



while :: state -> (state -> Bool) -> (state -> state) -> (state -> result) -> result
while state checkFunc updateFunc resultsFunc =
  if (checkFunc state)
      then while (updateFunc state) checkFunc updateFunc resultsFunc
      else (resultsFunc state)

-- The while function is tail recursive because it doesn't need to return to get the
-- output, it just updates the state variable as it recurses.

nSquares :: Int -> [Int]
nSquares n =
  while (1, [])
        (\(index, _) -> index <= n)
        (\(index, squares) -> (index + 1, index^2 : squares))
        (reverse . snd)

-- The state in nSquares is a tuple containing an index and the resulting list.
-- The index is checked to see if it is less than n, if it is, the square of the
-- index is added to the front of the list and the index is incremented. Once the
-- index surpasses n, the list is extracted from the tuple and then reversed so it is
-- in the proper order.


functionPairsWhile :: (t -> b) -> [t] -> [(Int, b)]
functionPairsWhile f xs =
  while (0, [])
        (\(index, _) -> index < length xs)
        (\(index, list) -> (index + 1, (index + 1, (f (xs!!index))) : list))
        (reverse . snd)

myMap3 :: (a -> b) -> [a] -> [b]
myMap3 f xs =
  while (0, [])
        (\(index, _) -> index < length xs)
        (\(index, list) -> (index + 1, (f (xs!!index)) : list))
        (reverse . snd)

myWhileFoldl :: (b -> a -> b) -> b -> [a] -> b
myWhileFoldl f y xs =
  while (0, [y])
        (\(index, _) -> index < length xs)
        (\(index, list) -> (index + 1, ((f (head list) (xs!!index))) : list))
        (head . snd)

nFibs :: Int -> [Int]
nFibs n | n == 0 = []
        | n == 1 = [1]
        | otherwise =
            while (2, [1,1])
                  (\(index, _) -> index < n)
                  (\(index, fibs) -> (index + 1, (fibs!!0 + fibs!!1) : fibs))
                  (reverse . snd)

-- Update primes function to use filters to properly do the Sieve as posted on
-- CSNS forum
nPrimes :: Int -> [Int]
nPrimes n = while (2:[3,5..], 0, [])
              (\(_, pCount, _) -> n > pCount)
              (\(p:nums, pCount, primes) -> (filter (\x -> x `mod` p /= 0) nums, pCount + 1, p : primes ))
              (\(_, _, primes) -> reverse primes)
