
-- Implementation of Credit Card Number Validation --
-- Follows guide at http://ozark.hendrix.edu/~yorgey/490/static/Haskell-intro.pdf --

-- toDigits works using point free notation. The unnamed argument will get passed
-- to show, creating a String from the Integer. Map will cause each character in that
-- String to be made as the head of an empty list which will be then passed to
-- read, which will make that list into an Integer.
toDigits :: Integer -> [Integer]
toDigits = map (read . (:[])) . show

-- toDigitsRev works the same way as toDigits, it simply reverses the list
toDigitsRev :: Integer -> [Integer]
toDigitsRev = reverse . map (read . (:[])) . show

-- doubleEveryOther utilizes a cycle and the zipWith function. zipWith is applied
-- to the reversed list and a cycle of 1 and 2. The first element in the list is
-- multiplied by 1 and the next by 2 and the next by 1 and so on until the list
-- is exhausted. The list is reversed in order to work from right to left.
doubleEveryOther :: [Integer] -> [Integer]
doubleEveryOther list = zipWith (*) (reverse list) (cycle [1,2])

-- sumDigits uses the map function to apply toDigits to all elements in list. This
-- creates lists of lists so concat is used to get a list of single nonlist elements.
-- The sum of this list is then returned.
sumDigits :: [Integer] -> Integer
sumDigits list = sum $ concat $ map toDigits list

-- validate takes a potential cc number, converts it to digits, doubles every other
-- digit from right to left, sums the digits and finally checks if it is divisible
-- by 10.
validate :: Integer -> Bool
validate number = (sumDigits $ doubleEveryOther $ toDigits number) `mod` 10 == 0
