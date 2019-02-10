--Notes--


-- listA is an infinite list of odds
listA = [3, 5 ..]
-- listB is also an infinite list of odds
listB = [x | x <- [3, 5 ..]]
-- listC is a list of odds from 3 through 5999
listC = [x | x <- [3, 5 .. 5999]]
-- listD is a list of odds from 3 through 5999
listD = [x | x <- [3, 5 .. 6000]]
-- listE never breaks because the list of odds is infinite and only checks if x is less than 6000
listE = [x | x <- [3, 5 ..], (x < 6000)]
-- listF stops generating odds because of the takeWhile and is a list of odds from 3 through 5999
listF = [x | x <- takeWhile (\x -> x < 6000) [3, 5 ..] ]

-- lists c) d) and f) are equivalent and return true

-- lists a) and b) are equivalent infinite lists but won't return true because
-- they never stop evaluating

-- list e) is a list of odds from 3 though 5999 won't stop generating odds, they
-- just aren't added to the list
