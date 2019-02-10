# Dynamic Typing 1

if False:
    1 + "two"  # This line never runs, so no TypeError is raised
else:
    1 + 2       #  output will be 3 because if Flase condition will never run



1 + "two"  # Now this is type checked, and a TypeError is raised because + operator doesn't support between int and string .


# Dynamic Typing 2

thing = "Hello" #just decalred a variable name thing to a string "Hello"
type(thing)     #type gives the type of the variable . So this statement will not give out the output untill we print it out

#output :  <class 'str'>

thing = 28.1  #just decalred a variable name thing to a float 28.1
type(thing)   #type gives the type of the variable . So this statement will not give out the output untill we print it out

#output: <class 'float'>


# Duck Typing

class TheHobbit:
    def __len__(self):   #__len__ is a magic method . magic methods in Python are the methods having two prefix and suffix underscores in the method name .
    		return 95022			 #self represents the instance of the class.


the_hobbit = TheHobbit()
len(the_hobbit)  #len is a function to get the length of a collection. It works by calling an object's __len__ method.

#output : 95022

#len can be rougly defined as :

#def len(obj):
#    return obj.__len__()

# These are special methods that are a set of predefined methods you can use to enrich your classes.


# Hello Types

def headline(text: str, align: bool = True) -> str:      #defining a function named headline . text:str means that the text will be of type string . ->str means that the output will be of type string .
    if align:
        return f"{text.title()}\n{'-' * len(text)}"      # f is a New and Improved Way to Format Strings in Python and usually identified by f followed by curly braces
    else:
        return f" {text.title()} ".center(50, "o")



print(headline("python type checking"))
#output :  Python Type Checking
#          --------------------

#since nothing is mentioned ,it is assumed that is aligned so first the title comes and then -*len(text) in the next line

print(headline("python type checking", align=False))
#output  :  oooooooooooooo Python Type Checking oooooooooooooo

#since the align is false so the else part is considered .

print(headline("python type checking", align="left"))
#output :  Python Type Checking
#          --------------------

#since it is mentioned that align is left ,it is aligned so first the title comes and then -*len(text) in the next line

print(headline("use mypy", align="center"))
#output  :  Use Mypy
#           --------

#since it is mentioned that align is center ,it is aligned so first the title comes and then -*len(text) in the next line


# Annotations

import math   #importing library named math

pi: float = 3.142  #initalizing pi which is of float type  to the value 3.142

def circumference(radius: float) -> float:   #radius is of float type and the definaition will result in the type float
    return 2 * math.pi * radius


circumference(1.23)
#output :   7.728317927830891

circumference.__annotations__
#output :    {'radius': <class 'float'>, 'return': <class 'float'>}

#what it means is that since radius is of float type  so the annotation will be radius': <class 'float'> since the result is the type float annotation will be return': <class 'float'>

__annotations__
#output :   {'pi': <class 'float'>}

#since only __annotations__ is called so it will give the annotations of all the variables declared and in this its only pi .


nothing: str

__annotations__
#output :   {'nothing': <class 'str'>}
#since only __annotations__ is called so it will give the annotations of all the variables declared and in this its only nothing .


# Type Comments

import math

def circumference(radius):     #comments are added by adding #
    # type: (float) -> float
    return 2 * math.pi * radius


def headline(                       #comments are added by adding #
 4     text,           # type: str
 5     width=80,       # type: int
 6     fill_char="-",  # type: str
 7 ):                  # type: (...) -> str
 8     return f" {text.title()} ".center(width, fill_char)
 9
10 print(headline("type comments work", width=40))

pi = 3.142  # type: float.   #comments are added by adding #



# Playing with Python Types Part 1

import random

SUITS = "♠ ♡ ♢ ♣".split()                       #The .split() method creates a list of elements from a string. The default splitter is a whitespace
RANKS = "2 3 4 5 6 7 8 9 10 J Q K A".split()    # but whatever is passed into .split() as an argument will act as splitter.

def create_deck(shuffle=False):
     """Create a new deck of 52 cards"""
     deck = [(s, r) for r in RANKS for s in SUITS]   # in other terms it can be written as   for(s in SUITS)
     if shuffle:                                                                     #          for(r in RANKS)
         random.shuffle(deck)                                    #                                     deck = [(s,r)]
     return deck

def deal_hands(deck):
     """Deal the cards in the deck into four hands"""
     return (deck[0::4], deck[1::4], deck[2::4], deck[3::4])    # a tuple comprehension using slices (start:end:step) to deal a number of hands

def play():
     """Play a 4-player card game"""
     deck = create_deck(shuffle=True)
     names = "P1 P2 P3 P4".split()      #The .split() method creates a list of elements from a string. The default splitter is a whitespace
     hands = {n: h for n, h in zip(names, deal_hands(deck))}   #In this case hands = 4 .

     for name, cards in hands.items():
         card_str = " ".join(f"{s}{r}" for (s, r) in cards).  #this will print a suit and rank together and since join is used so a bunch of them are joined together with space in between .
         print(f"{name}: {card_str}")

if __name__ == "__main__":      #this is the start of the program . From here play() function is called .
     play()




#The zip() function returns a zip object, which is an iterator of tuples where the first item in each passed iterator is paired together,
#and then the second item in each passed iterator are paired together etc.

#    a = ("John", "Charles", "Mike")
#   b = ("Jenny", "Christy", "Monica")

#    x = zip(a, b)

#output : (('John', 'Jenny'), ('Charles', 'Christy'), ('Mike', 'Monica'))


#  Sequences and Mappings


name: str = "Guido"  #initalizing name which is of str type  to the value Guildo
pi: float = 3.142   #initalizing pi which is of float type  to the value 3.142
centered: bool = False   #initalizing centered which is of boolean type  to the value False

names: list = ["Guido", "Jukka", "Ivan"]  #initalizing names which is of list type .List is a collection which is ordered and changeable.
version: tuple = (3, 7, 1)   #initalizing versions which is of tuple type .Tuple is a collection which is ordered and unchangeable.
options: dict = {"centered": False, "capitalize": True}  #initalizing options which is of dictionary type .Dictionary is a collection which is unordered, changeable and indexed.

from typing import Dict, List, Tuple,Sequence

names: List[str] = ["Guido", "Jukka", "Ivan"]  #initalizing names which is of list type contains values which is of type string .
version: Tuple[int, int, int] = (3, 7, 1)      #initalizing version which is of tuple type contains values which is of type int.
options: Dict[str, bool] = {"centered": False, "capitalize": True}  #initalizing options which is of dictionary type contains values which is of type string and boolean.



def square(elems: Sequence[float]) -> List[float]:  #defining function named square with parameter as elems which is of sequence type contains value which is of type float giving a result of type list which contains float values.
    return [x**2 for x in elems]  #in other words   for(x in elems)
    								#              return x**2



#Sequence is an example of using duck typing . Sequences allow you to store multiple values in an organized and efficient fashion .
