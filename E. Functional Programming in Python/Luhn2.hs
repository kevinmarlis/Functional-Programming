-- Point free in Haskell:
-- Point free functions perform the same operations as functions with
-- explicit arguments but is generally cleaner.

-- Declaration lets read know to return an Int from the single character string
-- created from the character.
toDigit :: Char -> Int
toDigit c = read [c]

-- Point free notation where the nondeclared argument gets passed to show, creating
-- a String. Each characgter in the string gets passed to toDigit via map, which
-- will return a list of Ints.
toDigits :: Int -> [Int]
toDigits = map toDigit . show

-- The nondeclared argument is initially passed to reverse, which reverses the list
-- of Ints. zipWith then multiplies the cycling [1,2] with the reversed Int list
-- so that the first element is multiplied by 1, the next by 2, the next by 1, etc.
doubleEveryOther :: [Int] -> [Int]
doubleEveryOther = zipWith (*) (cycle [1,2]) . reverse

-- Apply toDigits to all elements in the results of doubleEveryOther which results
-- in a list of lists of digits. Concat combines them into a single list which
-- is then summed.
sumDigits :: [Int] -> Int
sumDigits = sum . concat . map toDigits

-- Point free notation where the argument gets passed to toDigits and the return
-- gets passed to doubleEveryOther and the return gets passed to sumDigits
checkSum :: Int -> Int
checkSum = sumDigits . doubleEveryOther . toDigits

-- Simply checks if checkSum is divisible by 10, thereby validating the number
isValid :: Int -> Bool
isValid n = checkSum n `mod` 10 == 0

-- Tests cases using map to run each Int in the list through the isValid function
testCC :: [Bool]
testCC = map isValid [1234567890123456, 1234567890123452] -- => [False, True]
