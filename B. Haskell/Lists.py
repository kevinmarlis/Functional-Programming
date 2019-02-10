from itertools import count, takewhile

# listA = list(count(3,2))
#
# listB = [x for x in count(3,2)]

listC = [x for x in range(3,6000,2)]

listD = [x for x in range(3,6001,2)]

# listE = [x for x in list(count(3,2)) if x < 6000]

# listF = [x for x in takewhile(lambda x: x < 6000, list(count(3,2)))]

print(listC == listD)
