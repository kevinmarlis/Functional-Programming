-- zipWith applies the lambda function x y to the two lists where x is an element
-- from the cycling list of functions id and fn and y is the reversed list of
-- digits from the Int n. The resulting list from zipWith is summed and then checked
-- for divisibility by 10.
myLuhn :: Int -> Bool
myLuhn n = (sum $ zipWith (\x y -> x y) (cycle [id, fn]) $ reverse $ digits n) `mod` 10 == 0

-- Function that converts an Int into a list of the digits of that Int
digits :: Int -> [Int]
digits = map (read . (:[])) . show

-- Function that doubles an Int digit, using divMod to take care of the case
-- when the doubling results in a two digit Int using uncurry to sum the two
-- digits. Uncurry: (a -> b -> c) -> (a,b) -> c
-- ex: fn 10 = uncurry (+) (2, 0) = 2 + 0 = 2
-- ex: fn 3  = uncurry (+) (0, 6) = 0 + 6 = 6
fn :: Int -> Int
fn x = uncurry (+) (divMod (2 * x) 10)

-- 1234567890123452 -> true, 1234567890123456 -> false
