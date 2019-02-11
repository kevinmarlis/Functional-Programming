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
-- Value is the last element to be processed in the list.



myFoldr :: (a -> b -> b) -> b -> [a] -> b
myFoldr f y [] = y
myFoldr f y (x:xs) = f x (myFoldr f y xs)

-- This is not tail recursive because it has to return from the last element
-- before completing the previous element and so on.
-- Value is first element to be processed

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
-- > take 5 cyc12 - generate the first element of cyc12 to get:
-- > take 5 (1 ++ xs) - apply the recursive take case to get:
-- > 1 : take 4 (xs) - generate the next element of cyc12 to get:
-- > 1 : take 4 (2 ++ xs) - apply the recursive take case to get:
-- > 1 : 2 : take 3 (xs) - generate the next element of cyc12 to get:
-- > 1 : 2 : take 3 (1 ++ xs) - apply the recursive take case to get:
-- > 1 : 2 : 1 : take 2 (xs) - generate the next element of cyc12 to get:
-- > 1 : 2 : 1 : take 2 (2 ++ xs) - apply the recursive take case to get:
-- > 1 : 2 : 1 : 2 : take 1 (xs) - generate the next element of cyc12 to get:
-- > 1 : 2 : 1 : 2 : take 1 (1 ++ xs) - apply the recursive take case to get:
-- > 1 : 2 : 1 : 2 : 1 take 0 (xs) - apply the base take case to get:
-- > 1 : 2 : 1 : 2 : 1 : [] - Nothing left to evaluate



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



while :: a -> (a -> Bool) -> (a -> a) -> (a -> b) -> b
while x f1 f2 f3 =
  if (f1 x)
      then while (f2 x) f1 f2 f3
      else (f3 x)

-- The while function is tail recursive because it doesn't need to return to get the
-- output, it just updates the state variable as it recurses.

nSquares :: Int -> [Int]
nSquares n =
  while (1, [])
        (\(index, _) -> index <= n)
        (\(index, list) -> (index + 1, index^2 : list))
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
nFibs n =
  while (2, [1,1])
        (\(index, _) -> index < n)
        (\(index, list) -> (index + 1, (list!!0 + list!!1) : list))
        (reverse . snd)

-- not a great implementation because it relies on an unnecessary else function
nPrimes :: Int -> [Int]
nPrimes n =
  while (2, [])
        (\(index, list) -> length list < n)
        (\(index, list) -> (index + 1, if null[p | p <- list, index `mod` p == 0]
            then (index : list) else drop 1 (index : list)))
        (reverse . snd)
