# Python's parser looks to the token to the right. In this case it sees a number
# followed by a dot, so it determines it to be a float literal, but throws up
# the error becuase the following character is the underscore, which can't
# be part of a float. So some workarounds are the parentheses or using a space
# between the int and the dot. To actually use a float you can use two dots.

# Parentheses
print("Parentheses: ", (1).__add__(3))

# Space
print("Space: ", 1 .__add__(3))

# floats
print("1.0: ", 1.0.__add__(3))

print("1..: ", 1..__add__(3))

print(1. __add__(3))
