data FibElement = I Integer | Fib Integer | Plus deriving Show

fib_top_down_iter_v2 :: Integer -> Integer
fib_top_down_iter_v2 n = helper ([Fib n], [])


helper :: ([FibElement], [FibElement]) -> Integer
helper ([I n], _) = n
helper (Fib n : fibs, stack) | n <= 2 = helper (I 1 : fibs, stack)
                             | otherwise = helper (Fib (n - 2) : Fib (n - 1 ) : Plus : fibs, stack)
helper (I n : fibs, stack) = helper (fibs, I n : stack)
helper (Plus : fibs, I n1 : I n2 : stack) = helper (I (n1 + n2) : fibs, stack)
