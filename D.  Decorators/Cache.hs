import Data.Map as Map

data Input = Word String | Num Integer deriving (Show, Eq)

-- This function allows us to essentially cast something of type Input back
-- into the original type. They are used to get the original elements out of a
-- list of type Input.
num :: Input -> Integer
num (Num num) = num



-- While loop implementation
while :: state -> (state -> Bool) -> (state -> state) -> (state -> result) -> result
while state checkFunc updateFunc resultsFunc
  | checkFunc state = while (updateFunc state) checkFunc updateFunc resultsFunc
  | otherwise = resultsFunc state


-- Top down iteration --

-- 81.16 secs, 67,716,869,416 bytes
-- A truly not optimized implementation that utilizes the previously implemented
-- while loop and a helper function.
fib_top_down_iter :: Integer -> Integer
fib_top_down_iter n =  while ([Word "fib", Num n], [])
                             (\(inp, _, _) -> inp == [])
                             (\(inp, stack, cache) -> helper (inp, stack, cache))
                             (\(_, stack, _) -> head stack)

helper :: ([Input], [Integer], Map Integer Integer) -> ([Input], [Integer], Map Integer Integer)
helper (inp, stack, cache) | last inp == Word "fib" && Nothing /= Map.lookup (head stack) cache = (init inp ++ [Map.lookup (head stack) cache], tail stack, cache)
                           | last inp == Word "fib" = (init inp ++
                              [Word "cache", head stack, Word "plus", Word "fib", Num $ head stack - 1, Word "fib", Num $ head stack - 2], tail stack, cache)
                           | last inp == Word "plus" = (init inp ++ [Num $ head stack + stack !! 1], Prelude.drop 2 stack, cache)
                           | last inp == Word "cache" = (init inp, tail stack, insert (num (head stack)) (num (stack !! 1)) cache)
                           | otherwise = (init inp, (num $ last inp) : stack, cache)
