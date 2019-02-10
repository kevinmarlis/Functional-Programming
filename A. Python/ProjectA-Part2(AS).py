#Type Aliases

def deal_hands(
     # The annotation for deck (List[Tuple[str, str]]) is not clear.
     # List[Tuple[str, str]] is supposed to represent a deck of cards
     # To make this code more clear-cut, we can create type aliases as in the code
     # using the variables Card and Deck
     deck: List[Tuple[str, str]]
) -> Tuple[
     List[Tuple[str, str]],
     List[Tuple[str, str]],
     List[Tuple[str, str]],
     List[Tuple[str, str]],
 ]:
     """Deal the cards in the deck into four hands"""
     return (deck[0::4], deck[1::4], deck[2::4], deck[3::4])


from typing import List, Tuple
#Create type aliases to represent a card and a deck of cards
Card = Tuple[str, str]
Deck = List[Card]

#The annotations for deal_hands() are now much more concise and readable using
#these type aliases
def deal_hands(deck: Deck) -> Tuple[Deck, Deck, Deck, Deck]:
     """Deal the cards in the deck into four hands"""
     #deck[0::4] start at index 0, go through end of list, and append every fourth element...
     return (deck[0::4], deck[1::4], deck[2::4], deck[3::4])



#Shell
>>> from typing import List, Tuple
>>> Card = Tuple[str, str]
>>> Deck = List[Card]

#calling the type alias from the shell allows you to inspect the type alias
#to check what it represents
>>> Deck
typing.List[typing.Tuple[str, str]]


#Functions Withour Return Values
#In python, Functions without an explicit return will return None

#play() does not specify a return value, so this function will return None
#Shell
>>> def play(player_name):
...     print(f"{player_name} plays")
...

>>> ret_val = play("Jacob")
Jacob plays

>>> print(ret_val)
None


# play.py
#Functions without a return value should add the return type hint "None"
def play(player_name: str) -> None:
         print(f"{player_name} plays")

#ret_val is being assigned the return value "None"
#mypy will warn you about this return value as in the following lines
ret_val = play("Filip")

#Shell
$ mypy play.py
play.py:6: error: "play" does not return a value




# play.py
#If a type hint for the return value is not added, mypy will have no information
#about the return value, therefore, no warning will be given
def play(player_name: str):
    print(f"{player_name} plays")

ret_val = play("Henrik")

#Shell
#No type hint was given for the return value of play(), so mypy does not generate
#any warnings
$ mypy play.py
$



from typing import NoReturn
#The NoReturn type is used for functions that are never expected to return normally
def black_hole() -> NoReturn:
    #an Exception is raised, so the function will never return properly
    raise Exception("There is no going back ...")


# game.py

import random
from typing import List, Tuple

SUITS = "♠ ♡ ♢ ♣".split()
RANKS = "2 3 4 5 6 7 8 9 10 J Q K A".split()

#Create type aliases Card and Deck
Card = Tuple[str, str]
Deck = List[Card]

def create_deck(shuffle: bool = False) -> Deck:
     """Create a new deck of 52 cards"""
     #Create a list of tupples (s,r) for every Rank and Suit
     deck = [(s, r) for r in RANKS for s in SUITS]
     if shuffle:
         #the shuffle() method randomizes items in a list. This is effectively
         #shuffling our deck of cards
         random.shuffle(deck)
     return deck

def deal_hands(deck: Deck) -> Tuple[Deck, Deck, Deck, Deck]:
     """Deal the cards in the deck into four hands"""
     #deck[0::4] start at index 0, go through end of list, and append every fourth element...
     return (deck[0::4], deck[1::4], deck[2::4], deck[3::4])

def choose(items):
     """Choose and return a random item"""
     return random.choice(items)

def player_order(names, start=None):
     """Rotate player order so that start goes first"""
     if start is None:
         #randomly assign a starting player to the start variable
         start = choose(names)
    #assign the index of the starting player to start_idx
     start_idx = names.index(start)
     #Rotate player order so that start goes first
     return names[start_idx:] + names[:start_idx]

def play() -> None:
     """Play a 4-player card game"""
     deck = create_deck(shuffle=True)
     #create a list of 4 players [P1, P2, P3, P4]
     names = "P1 P2 P3 P4".split()
     #create a dictionary with player names as the key and the corresponding player
     #hand as the value
     hands = {n: h for n, h in zip(names, deal_hands(deck))}
     start_player = choose(names)
     turn_order = player_order(names, start=start_player)

     # Randomly play cards from each player's hand until empty
     while hands[start_player]:
        for name in turn_order:
            card = choose(hands[name])
            hands[name].remove(card)
            print(f"{name}: {card[0] + card[1]:<3}  ", end="")
        print()
# When the python interpreter reads a source file, it defines a "__name__"
# variable and assigns it the string "__main__", so if this is the source file,
# the play() function will run and a game will being
if __name__ == "__main__":
     play()


#The Any Type

import random
from typing import Any, Sequence
#the choose() function takes a Sequence(list, tupple, string...) as an argument
#This sequence can be composed of any types, as indicated by the keyword Any,
#and returns and item of any type
def choose(items: Sequence[Any]) -> Any:
    return random.choice(items)


# choose.py
import random
from typing import Any, Sequence

def choose(items: Sequence[Any]) -> Any:
     return random.choice(items)

names = ["Guido", "Jukka", "Ivan"]
reveal_type(names)

name = choose(names)
reveal_type(name)

#Shell
#Mypy will correctly infer that names is a list of strings but that information
#will be lost after the call to chooose because of the use of the Any type
$ mypy choose.py
choose.py:10: error: Revealed type is 'builtins.list[builtins.str*]'
choose.py:13: error: Revealed type is 'Any'




#---Type Theory---

#Subtypes
#T is a subtype of U if:
#Every value from T is also in the set of values of U type
#Every function from U type is also in the set of functions of T type

#bool is a subtype of int
>>> int(False)
0
>>> int(True)
1
>>> True + True
2
>>> issubclass(bool, int)
True

#a subtype can always pretend to be its supertype
def double(number: int) -> int:
    return number * 2

print(double(True))  # Passing in bool instead of int, returns 2



#---Playing With Python Types, Part 2---
import random
from typing import Any, Sequence
#the choose() function takes a Sequence(list, tupple, string...) as an argument
#This sequence can be composed of any types, as indicated by the keyword Any,
#and returns and item of any type
def choose(items: Sequence[Any]) -> Any:
    return random.choice(items)

#Type Variables
# choose.py

import random
#A type variable is a special variable that can take on any type, depending on
# the situation
from typing import Sequence, TypeVar
#Define a type variable using TypeVar from the typing module.
Choosable = TypeVar("Chooseable")

def choose(items: Sequence[Choosable]) -> Choosable:
      return random.choice(items)

names = ["Guido", "Jukka", "Ivan"]
reveal_type(names)

#because a type variable was used (instead of Any), mypy will recognize that name
#is a str type, no information is lost when choose() is called
name = choose(names)
reveal_type(name)
#Shell
$ mypy choose.py
choose.py:12: error: Revealed type is 'builtins.list[builtins.str*]'
choose.py:15: error: Revealed type is 'builtins.str*'


# choose_examples.py
from choose import choose
#revealed type will be str
reveal_type(choose(["Guido", "Jukka", "Ivan"]))
#revealed type will be int
reveal_type(choose([1, 2, 3]))
#Because bool is a subtype of float, the return value of choose() is guaranteed
#to be something that can be thought of as a float
reveal_type(choose([True, 42, 3.14]))
#There is no subtype relationship between str and int, so the revealed type will
#be an object
reveal_type(choose(["Python", 3, 7])
#Shell
$ mypy choose_examples.py
choose_examples.py:5: error: Revealed type is 'builtins.str*'
choose_examples.py:6: error: Revealed type is 'builtins.int*'
choose_examples.py:7: error: Revealed type is 'builtins.float*'
choose_examples.py:8: error: Revealed type is 'builtins.object*'


# choose.py
import random
from typing import Sequence, TypeVar
#Constrain the Choosable type variable by listing the acceptable types str and float
Choosable = TypeVar("Choosable", str, float)

def choose(items: Sequence[Choosable]) -> Choosable:
     return random.choice(items)
#ok
reveal_type(choose(["Guido", "Jukka", "Ivan"]))
#although all ints, int is a subtype of float, so this is still acceptable
reveal_type(choose([1, 2, 3]))
#ok
reveal_type(choose([True, 42, 3.14]))
#Mypy will raise a type error because "object" is not an acceptable type
reveal_type(choose(["Python", 3, 7]))
#Shell
$ mypy choose.py
choose.py:11: error: Revealed type is 'builtins.str*'
choose.py:12: error: Revealed type is 'builtins.float*'
choose.py:13: error: Revealed type is 'builtins.float*'
choose.py:14: error: Revealed type is 'builtins.object*'
choose.py:14: error: Value of type variable "Choosable" of "choose"
                     cannot be "object"


#Constrain the Choosable TypeVar to strings and cards
Choosable = TypeVar("Choosable", str, Card)
def choose(items: Sequence[Choosable]) -> Choosable:
    ...



#Duck Types and Protocols
#len() can return the length of any object that has implemented the .__len__()
# method, How can we add type hints to the job argument?
#In a structural system (as opposed to nominal), comparisons between types are
#based on structure. You could define a structural type Sized that includes
#all instances that define .__len__(), irrespective of their nominal type.
def len(obj):
    return obj.__len__()

#A protocol specifies one or more methods that must be implemented. All classes
#defining .__len__() fullfill the typing.Sized protocol
from typing import Sized
#len() will accept arguments of type Sized and return type int
def len(obj: Sized) -> int:
    return obj.__len__()


from typing_extensions import Protocol
#Define your own protocols by inheriting from Protocol and defining the function
#signatures (with empty function bodies) that the protocol expects
class Sized(Protocol):
    def __len__(self) -> int: ...

    def len(obj: Sized) -> int:
        return obj.__len__()

#The Optional Type
#A common pattern is to use None as a default value for an argument, but this
#creates a challenge for type hinting because "start" should generally be a string
#in order to annotate an argument like this, we can use the Optional type
def player_order(names, start=None):
     """Rotate player order so that start goes first"""
     if start is None:
         start = choose(names)
     start_idx = names.index(start)
     return names[start_idx:] + names[:start_idx]

from typing import Sequence, Optional

def player_order(
#The Optional type for the "start" variable tells us that "start" will either be
#None, or the type specified, which in this case is str
#An equivalent way of specifying the same would be using the Union type:
#Union[None, str]
    names: Sequence[str], start: Optional[str] = None
) -> Sequence[str]:
    ...


# player_order.py

from typing import Sequence, Optional

def player_order(
     names: Sequence[str], start: Optional[str] = None
) -> Sequence[str]:
    #When using the type Optional (or Union), the variable in question must be checked for
    #the correct type when operating on it. In this case, "start" could be None
    #so mypy will raise a type error
     start_idx = names.index(start)
     return names[start_idx:] + names[:start_idx]
#Shell
$ mypy player_order.py
player_order.py:8: error: Argument 1 to "index" of "list" has incompatible
                          type "Optional[str]"; expected "str"
