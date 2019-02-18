import qualified Data.Map as Map
import Debug.Trace

-- 1.87 secs, 958,527,848 bytes
fib_top_down_rec :: Int -> Int
fib_top_down_rec n | n <= 2 = 1
                   | otherwise = fib_top_down_rec (n-1) + fib_top_down_rec (n-2)


-- 0.00 secs, 79,640 bytes
-- Iterate creates an infinite list of tuples where the first item is the
-- Fib number at that index and the second is the following fib number.
-- Calling this function with n = 32 generates the infinite list of Fib numbers
-- bottom up, and stops at n because of Haskell's laziness. Iterate returns the
-- tuple so we take the first element to get the nth Fib number.
fib_bottom_up_iter :: Int -> Int
fib_bottom_up_iter n = fst $ (iterate (\(x, y) -> (y, x + y)) (0, 1)) !! n


-- Functions needed for top down iterations
-- Creating type called Input which can be of value Word or Num (note that these
-- are not types). Word and Num are value constructors for the type Input. Each
-- take a parameter of the given type (String or Integer). In summary, the type
-- Input can be made from the function Word, which takes a string, or Num which
-- takes an Integer. Deriving Show and Eq makes the type Input part of the Show
-- and Eq typeclass, allowing for String representation and equivalence checks.
data Input = Word String | Num Integer deriving (Show, Eq)

-- These two functions allow us to essentially cast something of type Input back
-- into the original type. They are used to get the original elements out of a
-- list of type Input.
word :: Input -> String
word (Word w) = w

num :: Input -> Integer
num (Num num) = num

-- While loop implementation
while :: state -> (state -> Bool) -> (state -> state) -> (state -> result) -> result
while state checkFunc updateFunc resultsFunc
  | checkFunc state = while (updateFunc state) checkFunc updateFunc resultsFunc
  | otherwise = resultsFunc state


-- 81.16 secs, 67,716,869,416 bytes
-- Very poor, convoluted implementation that utilizes the previously implemented
-- while loop and a helper function.
fib_top_down_iter :: Integer -> Integer
fib_top_down_iter n =  while ([Word "fib", Num n], [])
                             (\(inp, _) -> not $ null inp)
                             (\(inp, stack) -> helper (inp, stack))
                             (\(_, stack) -> head stack)

helper :: ([Input], [Integer]) -> ([Input], [Integer])
helper (inp, stack) | last inp == Word "fib" && head stack <= 2 = (init inp ++ [Num 1], tail stack)
                    | last inp == Word "fib" = (init inp ++
                        [Word "plus", Word "fib", Num $ head stack - 1, Word "fib", Num $ head stack - 2], tail stack)
                    | last inp == Word "plus" = (init inp ++ [Num $ head stack + stack !! 1], drop 2 stack)
                    | otherwise = (init inp, (num $ last inp) : stack)




-- 23.61 secs, 20,940,003,848 bytes
fib_top_down_iter_with_opt_1 :: Integer -> Integer
fib_top_down_iter_with_opt_1 n = while ([Word "fib", Num n], [])
                                       (\(inp, _) -> not $ null inp)
                                       (\(inp, stack) -> helper_opt_1 (inp, stack))
                                       (\(_, stack) -> head stack)

helper_opt_1 :: ([Input], [Integer]) -> ([Input], [Integer])
helper_opt_1 (inp, stack) | last inp == Word "fib" = (init inp ++ lister [Num (x - 1) | x <-[head stack, (head stack - 2)..2]], 1 : stack)
                          | last inp == Word "plus" = (init inp, (head stack + (head $ tail stack)) : stack)
                          | otherwise = (init inp, (num $ last inp) : stack)

lister :: [Input] -> [Input]
lister [x] = [x]
lister (x:xs) = Word "plus" : Word "fib" : x : lister xs


-- 0.01 secs, 90,504 bytes
fib_top_down_iter_with_opt_2 n = while (n, 1, 0)
                                       (\(n, _, _) -> n > 1)
                                       (\(n, ka, kb) -> (n - 1, ka + kb, ka))
                                       (\(_, ka, _) -> ka)
