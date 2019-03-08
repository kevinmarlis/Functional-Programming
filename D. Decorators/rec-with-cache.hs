import Data.Map as Map
import Data.Maybe
import Data.Typeable


-- Top Down Recursive with Cache Implementation --

-- >> fib_top_down_rec_with_cache 32
-- 2178309 (0.00 secs, 123,664 bytes)
-- >> fib_top_down_rec_with_cache 92
-- 7540113804746346429 (0.01 secs, 283,656 bytes)

-- This function takes in argument 'n', and returns the value of the 'nth' fibinacci number.
-- First it checks whether n is less than or equal to 2, if yes, then it simply returns 1; otherwise,
-- it calls the helper function and passes it the value of n and an initial Map containing [ (1,1) , (2,1) ].
-- So once the cache is calculted, it simply looks up the value with the key of 'n', and returns that value.
fib_top_down_rec_with_cache :: Int -> Int
fib_top_down_rec_with_cache n
    | n <= 2 = 1
    | otherwise = sum . removeMaybe $ Map.lookup n cache
    where cache = rec_cache_helper n $ Map.insert 1 1 $ Map.insert 2 1 $ Map.empty


-- This is the helper function for the Top Down Recursive with Cache implementation
-- It takes in arguments 'n' and 'cache', where n is the 'nth' fibinacci number that we are looking for
-- and 'cache' is the stored values of previously cached fibinacci numbers.
-- This function recursively calculates the 'nth' fibinacci if it is not yet in the cache, then inserts
-- it into the cache and finally returns the updated cache, which will eventually contain the 'nth'
-- fibinacci number
rec_cache_helper :: Int -> Map Int Int -> Map Int Int
rec_cache_helper n cache
    | n <= 2 = cache
    | val /= Nothing = cache
    | otherwise = Map.insert n k new_cache
    where val = Map.lookup n cache
          new = rec_cache_helper (n-2) cache
          new_cache = rec_cache_helper (n-1) new
          a = sum . removeMaybe $ Map.lookup (n-1) new_cache
          b = sum . removeMaybe $ Map.lookup (n-2) new_cache
          k = a + b

-- This function is used to remove the Maybe 'boxed' around the actuall value, and returns the wrapped value
-- as a list. This value will be extracted later by composing the 'sum' function with this 'removeMaybe' function
removeMaybe :: Maybe a -> [a]
removeMaybe Nothing = []
removeMaybe (Just x) = [x]

{-

-- A Failed implementation of The Top Down Iterative with Cache Implementation --

A unique, yet unsuccessfull, implementation.
(May be appended to in the future, is this approach is successful)

Here I attempted to create a custom Stack data structure in Haskell, which would be able to Push and Pop, 'Node'
elements which contain data of Type 'Input', where these elements could either be of type 'Word' or 'Num'.

The idea was to implement a stack that could be used for both the 'inp' and 'stack' stacks as shown in the
iPyNb, and simplify the functionality of pushing and poping to the stacks. However, this proved to be
somewhat convoluted in Haskell; although I do believe it is possible to do so in this way, I (Jesus) was
unable to properly implement it.

This was my atempt:

data Stack i = EmptyStack | Node Input (Stack i) deriving (Show, Read, Eq)

--Created input as either a word or integer value
data Input = Word String | Num Integer deriving (Show, Read, Eq, Ord)

word :: Input -> String
word (Word w) = w

num :: Input -> Integer
num (Num n) = n
num (Word w) = -1

makeNode :: Input -> Stack Input
makeNode x = Node x EmptyStack

push :: Input -> Stack Input -> Stack Input
push x EmptyStack = makeNode x
push x stack = Node x stack

pop :: Stack Input -> (Maybe Input, Stack Input)
pop EmptyStack = (Nothing, EmptyStack)
pop (Node x s) = (Just x, s)

value :: (Maybe Input, Stack Input) -> [Input]
value (a, s) = removeMaybe a

isEmpty :: Stack Input -> Bool
isEmpty stack = stack == EmptyStack

removeMaybe :: Maybe x -> [x]
removeMaybe Nothing = []
removeMaybe (Just x) = [x]

hasVal :: [a] -> Bool
hasVal [] = False
hasVal [x] = True

get :: [a] -> a
get [x] = x


--While loop
while :: state -> (state -> Bool) -> (state -> state) -> (state -> result) -> result
while state checkFunc updateFunc resultsFunc
  | checkFunc state = while (updateFunc state) checkFunc updateFunc resultsFunc
  | otherwise = resultsFunc state


func n = while ( ( push (Num n) $ push (Word "fib") EmptyStack ) , EmptyStack , (insert 1 1 $ insert 2 1 empty) )
               ( \(inp, _, _) -> not ( isEmpty inp ) )
               ( \(inp, stack, cache) -> func_helper (inp, stack, cache) )
               ( \(_, stack, _) -> num $ get $ value $ pop stack )


func_helper (inp, stack, cache)
    | token > Word "any" = ( i , push token stack , cache )
    | token == Word "cache" = (i, s, insert (num n1) (num n2) cache)
    | token == Word "+" = ( (push n3 i), (snd $ pop s) , cache )
    | token == Word "fib" && found /= Nothing = ( ( push ( Num $ get $ removeMaybe found  ) inp ) , y , cache )
    | otherwise = ( added , y , cache )
    where token = get $ value $ pop inp
          i = snd $ pop inp
          n1 = get $ value $ pop stack
          s = snd $ pop stack
          n2 = get $ value $ pop s
          n3 = Num ( (num n1) + (num n2) )
          (x,y) = pop stack
          x1 = get $ value (x,y)
          found = Map.lookup (num x1) cache
          added = push (Num (num x1 - 2)) $ push (Word "fib") $ push (Num (num x1 - 1)) $ push (Word "+") $ push x1 $ push (Word "cache") i

-}
