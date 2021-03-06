import Data.Time.Calendar
import Data.Maybe
import Control.Applicative
import Data.List

--
-- Slides 43 - 44
--

-- firstOne' uses Maybe to return the element if it exists, and Nothing when the empty list.

firstOne' :: [a] -> Maybe a
firstOne' (a:_) = Just a
firstOne' [] = Nothing


-- addDays comes from Data.Time.Calendar

addAWeek :: Day -> Day
addAWeek d = addDays 7 d

interestingDates :: [Day]
interestingDates =
    [ fromGregorian 1966  9  8 -- first episode of Star Trek airs
    , fromGregorian 1969  6 21 -- first person on the moon
    , fromGregorian 1969 10 29 -- first ARPANET message sent
    ]


-- This function is of the type Maybe Day because firstOne' returns a type of
-- Maybe. If there are no interestingDates, Nothing will be returned.
anInterestingDate :: Maybe Day
anInterestingDate = firstOne' interestingDates

-- fmap :: (a -> b) -> f a -> f b
-- fmap applies the function addAWeek to anInterestingDate which holds either
-- nothing (hence the Maybe type) or a Day, hence fmap instead of map.
aWeekLater :: Maybe Day
aWeekLater = fmap addAWeek anInterestingDate


-- Further abstraction with point free notation
maybeAddAWeek :: Maybe Day -> Maybe Day
maybeAddAWeek = fmap addAWeek

aWeekLater' :: Maybe Day
aWeekLater' = maybeAddAWeek anInterestingDate

--
-- Slides 45: <|>
--

tvShows :: [(Int, String)]
tvShows =
    [ (1966, "Star Trek")
    , (1969, "Monty Python's Flying Circus")
    , (1989, "The Simpsons")
    ]

-- lookup: Eq a => a -> [(a,b)] -> Maybe b
-- showforYear looks in the list at the first element in each pair for equality.
-- It returns the second element of the first pair that equates.

showForYear :: Int -> Maybe String
showForYear y = lookup y tvShows


-- listToMaybe returns the Maybe of that list
-- filter keeps the members of a list that satisfy a condition
-- isInfixOf takes two lists and returns true if the first list is contained
-- wholly and intact within the second list
-- showWithName maps the function snd over tvShows resulting in a list of the
-- tv show titles. filter keeps the tv shows with the word n in a title in the
-- list. listToMaybe is called on the resulting list, returning either Nothing or
-- the first show in the list.

showWithName :: String -> Maybe String
showWithName n = (listToMaybe . filter (isInfixOf n) . map snd) tvShows


-- This has "named" fields, which act as accessor functions
data Person = Person { name :: String, year :: Int }

amy = Person { name = "Amy", year = 1971 }
cam = Person { name = "Cam", year = 1989 }
deb = Person { name = "Deb", year = 1967 }
monty = Person { name = "Monty", year = 1973 }

favoriteShow :: String -> Maybe String
favoriteShow "Amy" = Just "Batman"
favoriteShow "Bob" = Just "Iron Chef"
favoriteShow _     = Nothing

-- The (<|>) Applicative acts as a short circuiting or. Looking at the example,
-- each function called within pickShow returns a Maybe. If favoriteShow returns
-- a Just, pickShow returns that Just. If favoriteShow returns Nothing, showWithName
-- is called and the process repeats until either a Just is returned or there are
-- no more functions to call, which simply returns Nothing.

pickShow :: Person -> Maybe String
pickShow p =
    favoriteShow (name p)
    <|> showWithName (name p)
    <|> showForYear (year p)


-- pickShow using custom <=> operator instead of <|>

pickShow' :: Person -> Maybe String
pickShow' p =
    favoriteShow (name p)
    <=> showWithName (name p)
    <=> showForYear (year p)


-- Custom short circuit infix or operator

(<=>) ::  Maybe a -> Maybe a -> Maybe a
f <=> g | isJust f = f
        | isJust g = g
        | otherwise = Nothing


--
-- Slide 46: >>=
--

-- Custom infix bind operator

(>=>) :: Maybe a -> (a -> Maybe a) -> Maybe a
Nothing >=> _ = Nothing
Just a >=> f  = f a

num n | n > 12 = Just (n - 5)
      | otherwise = Nothing


--
-- Slide 47: fmap
--

-- Functor is used for types that can be mapped over
-- fmap is like map but applies to all Functors, not just lists
-- fmap :: Functor f => (a -> b) -> f a -> f b

-- fmap implementation for Maybe:

myfMap :: (a -> b) -> Maybe a -> Maybe b
myfMap f (Just a) = Just (f a)
myfMap f Nothing = Nothing


-- fmap implementation for List:

myfMapL :: (a -> b) -> [a] -> [b]
myfMapL f [] = []
myfMapL f xs = map f xs


--
-- Slides 50 - 53
--

-- This example highlights the usefulness of Haskell's typing system in keeping
-- code clean and concise without useless repetition. runLengthEncode takes a
-- list of a type that derives Eq and returns a list of pairs of that type and
-- an Int. Implementing in C++ is twice as long and much uglier.

runLengthEncode :: Eq a => [a] -> [(a, Int)]
runLengthEncode [] = []
runLengthEncode (x:xs) = nextGroup x 1 xs
  where
    nextGroup e n [] = [(e, n)]
    nextGroup e n (y:ys)
      | e == y    =          nextGroup e (n + 1) ys
      | otherwise = (e, n) : nextGroup y  1      ys


-- These functions are examples of properties that should hold regardless of input,
-- in order to use the quickCheck feature of Haskell. quickCheck automatically
-- generates random values which are run to verify the property. Use command
-- cabal install QuickCheck to install.

-- Function that sums the length of each runs and checks if it is the total
-- length of the list.

rlePropLengthPreserved :: [Int] -> Bool
rlePropLengthPreserved as = length as == (sum $ map snd $ runLengthEncode as)


-- The first guard (when n `mod` 100 == 0) returns the bool for runLengthEncode
-- on an empty string, checking for equality to the empty list. When
-- n `mod` 100 /= 0, it checks if runLengthEncode run on n `mod` 100 'x's is
-- equivalent to the list with tuple of 'x' and the number of 'x's.

rlePropDupesCollapsed :: Int -> Bool
rlePropDupesCollapsed n
  | m == 0    = runLengthEncode "" == []
  | otherwise = runLengthEncode (replicate m 'x') == [('x', m)]
  where m = n `mod` 100


-- The list is mapped to the function n `mod` 100 + 1 which is then zipped with
-- the infinite list of unicode characters starting from lowercase a and continuing
-- into ints (abcdefghijklmnopqrstuvwxyz{|}~\DEL\128\129...).
-- ex: zip ['a'..] $ map (\n -> n `mod` 100 + 1) [1,2,2,1]
-- [('a',2),('b',3),('c',3),('d',2)]
-- The resulting list of pairs is concatMapped over where the function replicates
-- the first element of the pair, the second element times.
-- ex: concatMap (\(i,n) -> replicate n i) [('a',2),('b',3),('c',3),('d',2)]
-- "aabbbcccdd"
-- The property checks if runLengthEncode on the concatMap function is equivalent
-- to the zipped list of pairs.

rlePropRoundTrip :: [Int] -> Bool
rlePropRoundTrip ns = runLengthEncode xs == is
  where is = zip ['a'..] $ map (\n -> n `mod` 100 + 1) ns
        xs = concatMap (\(i,n) -> replicate n i) is


-- quickCheck results:
-- > quickCheck rlePropRoundTrip
-- +++ OK, passed 100 tests.
--
-- > quickCheck rlePropDupesCollapsed
-- +++ OK, passed 100 tests.
--
-- > quickCheck rlePropRoundTrip
-- +++ OK, passed 100 tests.
