#
# Example: The Object(ive) of the Game
#

# All code from the Example: The Object(ive) of the Game section is
# elaborated on below.

#
#Type Hints for Methods
#

# With methods, parameters are typed in the same way they are for functions, but self
# does not need annotating because it is always an instance of a class which automatically
# has the type of that class.
# The .split() method creates a list of elements from a string. The default splitter is a whitespace
# but whatever is passed into .split() as an argument will act as splitter.
 6 class Card:
 7     SUITS = "♠ ♡ ♢ ♣".split()
 8     RANKS = "2 3 4 5 6 7 8 9 10 J Q K A".split()
 9
# Here, the parameters are typed (excluding self) and the "return" value is typed as None
# since the __init__() method always has a return type of None.
# __init__() is an example of a dunder. Dunders let you emulate certain common built in methods,
# and add common functionalities to classes via operator overloading (defining methods
# for operators). Some common dunders are __init__, __len__, __str__, __repr__,
# __getitem__, __eq__, __lt__, etc.
10     def __init__(self, suit: str, rank: str) -> None:
11         self.suit = suit
12         self.rank = rank
13
# Here, the method returns a string and is typed as such
# The __repr__() dunder sets the formal string representation of an object and is used
# by calling repr().
14     def __repr__(self) -> str:
# The f-string returns the string consisting of "suitrank".
15         return f"{self.suit}{self.rank}"

#
# Classes as Types
#

# Classes are used as types in that every instance of a class is of the type that is
# the name of the class. A problem arises when trying to use the type of a class within
# that class before it is finished being defined. One work around is to use the
# name of the class as a string literal that will later be evaulated by the type checker.

17 class Deck:
#  The cards parameter is typed as a list of Card objects using the Card class as the type
18     def __init__(self, cards: List[Card]) -> None:
19         self.cards = cards

20 class Deck:
# The @classmethod decorator is used to define methods inside a class
# that are not connected to an instance of that class. The class is always the first
# argument.
21     @classmethod
# Here, a string literal is used as the return type because the Deck class is still
# being defined.
22     def create(cls, shuffle: bool = False) -> "Deck":
23         """Create a new deck of 52 cards"""
# This list comprehension uses two nested loops to make Card objects for all pairs
# of Rank and Suit
24         cards = [Card(s, r) for r in Card.RANKS for s in Card.SUITS]
25         if shuffle:
26             random.shuffle(cards)
# A new Deck made of cards is returned.
27         return cls(cards)

34 class Player:
# Here, the Deck type can be used without the string because the Player class is defined
# after the completion of the Deck class definition
35     def __init__(self, name: str, hand: Deck) -> None:
36         self.name = name
37         self.hand = hand

# There is another work around for using a class type before it is finished being defined.
# Importing annotations from __future__ allows the use of a class type without the need for
# string literals as if the type has already been defined. This will be a feature in a future
# Python release.
# __future__ tells the interpreter to backport features from higher Python versions
# to the current interpreter. Since they change how the code is interpreted, they must
# be at the top of the file.
# https://www.pythonsheets.com/notes/python-future.html

from __future__ import annotations

class Deck:
    @classmethod
# A string literal is not used because of the __future__ import
    def create(cls, shuffle: bool = False) -> Deck:
        ...

#
# Returning self or cls
#

# Although self is generally not annotated because it implicitly has the type of the class as it
# is an instance of that class, in the case of superclasses, typing errors can occur. The fix is to
# use a type variable as shown below.

# In this code, the Dog class inherits from the Animal class.
 1 # dogs.py
 2
 3 from datetime import date
 4
 5 class Animal:
 6     def __init__(self, name: str, birthday: date) -> None:
 7         self.name = name
 8         self.birthday = birthday
 9
10     @classmethod
# newborn and twin return the string "Animal" as the class Animal is not yet finished being defined.
# There is a Mypy error where both fido and pluto have annotations of type Animal,
# not their actual type of Dog.
11     def newborn(cls, name: str) -> "Animal":
12         return cls(name, date.today())
13
14     def twin(self, name: str) -> "Animal":
15         cls = self.__class__
16         return cls(name, self.birthday)
17
18 class Dog(Animal):
19     def bark(self) -> None:
20         print(f"{self.name} says woof!")
21
22 fido = Dog.newborn("Fido")
23 pluto = fido.twin("Pluto")
24 fido.bark()
25 pluto.bark()

# Shell:
$ mypy dogs.py
dogs.py:24: error: "Animal" has no attribute "bark"
dogs.py:25: error: "Animal" has no attribute "bark"

# Here is the solution to that problem:

# dogs.py

from datetime import date
from typing import Type, TypeVar

# TAnimal is a type variable which can be instances of Animal or subclasses of Animal,
# as defined in the bound parameter. These type variablesensure that the return type
# matches the type of self or the instance type of cls.
TAnimal = TypeVar("TAnimal", bound="Animal")

class Animal:
    def __init__(self, name: str, birthday: date) -> None:
        self.name = name
        self.birthday = birthday

    @classmethod
    # Here, the type of Type[TAnimal] says that the class expects a type of the type of TAnimal.
    # Something of the type TAnimal is returned.
    def newborn(cls: Type[TAnimal], name: str) -> TAnimal:
        return cls(name, date.today())

    def twin(self: TAnimal, name: str) -> TAnimal:
        cls = self.__class__
        return cls(name, self.birthday)

class Dog(Animal):
    def bark(self) -> None:
        print(f"{self.name} says woof!")

fido = Dog.newborn("Fido")
pluto = fido.twin("Pluto")
fido.bark()
pluto.bark()

#
#Annotating *args and **kwargs
#

# Only each argument in *args or **kwargs should be annotated,
# not the tuple that contains them. That is, strings passed in as
# *args or **kwargs should be typed as str, not Tuple[str]
# *args are variable length non keyworded arguments passed into a function
# **kwargs are variable length keyworded argumetns passed into a function, useful
# for named arguments.
# https://wsvincent.com/python-args-kwargs/

46 class Game:
# although *names is a tuple it should be annotated as the type that the tuple contains.
47     def __init__(self, *names: str) -> None:
48         """Set up the deck and deal cards to 4 players"""
49         deck = Deck.create(shuffle=True)
# This comprehension makes a list of 4 names by converting the iterable names into a list.
# It then concatenates P1, P2, P3, P4 to the end after splitting the string. Lastly,
# it only takes the first four elements from that list
50         self.names = (list(names) + "P1 P2 P3 P4".split())[:4]
# This dictionary comprehension sets each name as a key and the value as the player
# passing in the name and corresping deck deal using the zip method to link them.
51         self.hands = {
52             n: Player(n, h) for n, h in zip(self.names, deck.deal(4))
53         }


#
# Callables
#

# The type Callable is used when passing functions, lambdas, methods or classes as
# an argument to another function etc. and looks like Callable[[type], return]. They allow
# type hints for these more complex arguments. There is an arbitrary Callable[..., return]
# similar to *args or **kwargs.
# https://mypy.readthedocs.io/en/latest/kinds_of_types.html#callable-types-and-lambdas

 1 # do_twice.py
 2
 3 from typing import Callable
 4
 # Here do_twice has two arguments, one of which is called func and is of type Callable[[str], str].
 # Callable provides the type hints for that function argument such that that function takes a parameter
 # of type str and returns a str.
 5 def do_twice(func: Callable[[str], str], argument: str) -> None:
 6     print(func(argument))
 7     print(func(argument))
 8
 # This function is an example of one that fits the parameters of the Callable func in do_twice
 9 def create_greeting(name: str) -> str:
10     return f"Hello {name}"
11
12 do_twice(create_greeting, "Jekyll")


#
# Example: Hearts
#

# This is an overview of type checking using the card game Hearts as an example.
# Most of this code has already been covered but additional comments have been added
# to sections of interest.


# hearts.py

from collections import Counter
import random
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
from typing import overload

class Card:
    SUITS = "♠ ♡ ♢ ♣".split()
    RANKS = "2 3 4 5 6 7 8 9 10 J Q K A".split()

    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit
        self.rank = rank

    @property
    def value(self) -> int:
        "The value of a card is rank as a number"""
        return self.RANKS.index(self.rank)

    @property
    def points(self) -> int:
        """Points this card is worth"""
        if self.suit == "♠" and self.rank == "Q":
            return 13
        if self.suit == "♡":
            return 1
        return 0

    # The use of Any effectively refrains from type checking
    def __eq__(self, other: Any) -> Any:
        return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other: Any) -> Any:
        return self.value < other.value

    def __repr__(self) -> str:
        return f"{self.suit}{self.rank}"

# The Deck class inherits Sequence of Cards.
class Deck(Sequence[Card]):
    def __init__(self, cards: List[Card]) -> None:
        self.cards = cards

    @classmethod
    # shuffle is of type bool with default value False and returns type Deck. Note
    # that deck is a string because Deck hasn't finished being defined yet.
    def create(cls, shuffle: bool = False) -> "Deck":
        """Create a new deck of 52 cards"""
        cards = [Card(s, r) for r in Card.RANKS for s in Card.SUITS]
        if shuffle:
            random.shuffle(cards)
        return cls(cards)

    def play(self, card: Card) -> None:
        """Play one card by removing it from the deck"""
        self.cards.remove(card)

    # a Tuple of type Deck (using the string) and arbitrary length is returned
    def deal(self, num_hands: int) -> Tuple["Deck", ...]:
        """Deal the cards in the deck into a number of hands"""
        # a tuple comprehension using slices (start:end:step) to deal a number of hands
        return tuple(self[i::num_hands] for i in range(num_hands))

    def add_cards(self, cards: List[Card]) -> None:
        """Add a list of cards to the deck"""
        self.cards += cards

    def __len__(self) -> int:
        return len(self.cards)

    @overload
    def __getitem__(self, key: int) -> Card: ...

    @overload
    def __getitem__(self, key: slice) -> "Deck": ...

    # Union means key can be of type int or slice and what is returned can be of
    # type Card or Deck (using the string)
    # __getitem__()
    def __getitem__(self, key: Union[int, slice]) -> Union[Card, "Deck"]:
        # isinstance(x, y) checks if x is an instance of y
        if isinstance(key, int):
            return self.cards[key]
        elif isinstance(key, slice):
            cls = self.__class__
            return cls(self.cards[key])
        else:
            # TypeError is raised if key is not of the type described in the Union
            raise TypeError("Indices must be integers or slices")

    def __repr__(self) -> str:
        # a string is returned consisting of each card in quotes separated by a space
        # the .join() method has an iterable as an argument and separates each item
        # by what .join() is being called on
        return " ".join(repr(c) for c in self.cards)

class Player:
    # hand is either of type Deck or None and is defaulted to None.
    def __init__(self, name: str, hand: Optional[Deck] = None) -> None:
        self.name = name
        self.hand = Deck([]) if hand is None else hand

    # played is a List of type Card, hearts_broken is a bool and a Deck is returned.
    # No string is needed for Deck because it has already been defined.
    # This section of code handles a lot of the game logic
    def playable_cards(self, played: List[Card], hearts_broken: bool) -> Deck:
        """List which cards in hand are playable this round"""
        # The hand with this card starts the round
        if Card("♣", "2") in self.hand:
            return Deck([Card("♣", "2")])

        # Hearts need to be "broken" before they can be played
        lead = played[0].suit if played else None
        # Creates a Deck of playable cards (lead suit must be followed)
        playable = Deck([c for c in self.hand if c.suit == lead]) or self.hand
        if lead is None and not hearts_broken:
            # Creates a deck if hand doesn't contain lead suit of all non heart suits
            playable = Deck([c for c in playable if c.suit != "♡"])
            # Returns playable Deck or a new Deck consisting of hand because
            # playable is null
        return playable or Deck(self.hand.cards)

    def non_winning_cards(self, played: List[Card], playable: Deck) -> Deck:
        """List playable cards that are guaranteed to not win the trick"""
        if not played:
            return Deck([])

        lead = played[0].suit

        # best_card determines the highest played card of the lead suit
        # which is the card that will take the hand
        best_card = max(c for c in played if c.suit == lead)

        # a list comprehension building a deck of playable cards that are less than
        # the best card, or is a different suit from the lead
        return Deck([c for c in playable if c < best_card or c.suit != lead])

    def play_card(self, played: List[Card], hearts_broken: bool) -> Card:
        """Play a card from a cpu player's hand"""
        playable = self.playable_cards(played, hearts_broken)
        non_winning = self.non_winning_cards(played, playable)

        # Strategy
        if non_winning:
            # Highest card not winning the trick, prefer points
            card = max(non_winning, key=lambda c: (c.points, c.value))
        elif len(played) < 3:
            # Lowest card maybe winning, avoid points
            card = min(playable, key=lambda c: (c.points, c.value))
        else:
            # Highest card guaranteed winning, avoid points
            card = max(playable, key=lambda c: (-c.points, c.value))
        self.hand.cards.remove(card)

        # f-string prints the name and the card they played
        print(f"{self.name} -> {card}")
        return card

    def has_card(self, card: Card) -> bool:
        return card in self.hand

    # dunder __repr__() sets the formal string representation
    def __repr__(self) -> str:
        # f-string uses the !r flag to use __repr__() instead of __str__()
        # https://realpython.com/python-f-strings/
        return f"{self.__class__.__name__}({self.name!r}, {self.hand})"

class HumanPlayer(Player):
    def play_card(self, played: List[Card], hearts_broken: bool) -> Card:
        """Play a card from a human player's hand"""
        playable = sorted(self.playable_cards(played, hearts_broken))
        # f-string of space separated cards numbered in sorted order
        # enumerate adds a counter to an iterable and returns the count and iterated item
        p_str = "  ".join(f"{n}: {c}" for n, c in enumerate(playable))
        np_str = " ".join(repr(c) for c in self.hand if c not in playable)
        print(f"  {p_str}  (Rest: {np_str})")
        while True:
            try:
                # user input with an f-string prompt where the user selects
                # a card based on the enumerated number from playable cards
                card_num = int(input(f"  {self.name}, choose card: "))
                card = playable[card_num]
            except (ValueError, IndexError):
                pass
            else:
                break
        self.hand.play(card)
        print(f"{self.name} => {card}")
        return card

class HeartsGame:
    # the __init__() dunder has a *args where each argument is of type str
    def __init__(self, *names: str) -> None:
        self.names = (list(names) + "P1 P2 P3 P4".split())[:4]
        self.players = [Player(n) for n in self.names[1:]]
        self.players.append(HumanPlayer(self.names[0]))

    def play(self) -> None:
        """Play a game of Hearts until one player go bust"""
        # Counter is a container, here initialized as a dictionary with keys
        # as player names, and values as score (initially zero)
        score = Counter({n: 0 for n in self.names})
        while all(s < 100 for s in score.values()):
            print("\nStarting new round:")
            # Here, a dictionary of player:score key value pairs is established
            # from a round and stored in round_score. The update() method on the
            # score Counter repopulates score with the new end of round dictionary
            round_score = self.play_round()
            score.update(Counter(round_score))
            print("Scores:")
            # The most_common() method creates a frequency distribution and
            # returns a sequence of the 4 most common values from greatest to least
            # Here, most_common() is used to create a sorted Sequence from highest
            # points to lowest.
            for name, total_score in score.most_common(4):
                print(f"{name:<15} {round_score[name]:>3} {total_score:>3}")
        # This list comprehension creates a list of names of players with the
        # lowest score.
        winners = [n for n in self.names if score[n] == min(score.values())]
        # join() only appends the separator if there is another remaining item
        # in the iterable
        print(f"\n{' and '.join(winners)} won the game")

    def play_round(self) -> Dict[str, int]:
        ""Play a round of the Hearts card game"""
        deck = Deck.create(shuffle=True)
        for player, hand in zip(self.players, deck.deal(4)):
            player.hand.add_cards(hand.cards)
            # next() returns the next item from the iterator
        start_player = next(
            p for p in self.players if p.has_card(Card("♣", "2"))
        )
        tricks = {p.name: Deck([]) for p in self.players}
        hearts = False

        # Play cards from each player's hand until empty
        while start_player.hand:
            played: List[Card] = []
            turn_order = self.player_order(start=start_player)
            for player in turn_order:
                card = player.play_card(played, hearts_broken=hearts)
                played.append(card)
            start_player = self.trick_winner(played, turn_order)
            tricks[start_player.name].add_cards(played)
            print(f"{start_player.name} wins the trick\n")
            # any() returns true if any iterable item is true
            hearts = hearts or any(c.suit == "♡" for c in played)
        return self.count_points(tricks)

        # the optional type means start can be either of type Player or None
        # and has an initial value of None
    def player_order(self, start: Optional[Player] = None) -> List[Player]:
        """Rotate player order so that start goes first"""
        if start is None:
            start = random.choice(self.players)
        start_idx = self.players.index(start)
        # the player with the starting index and the player with the ending index
        # are returned in a single list
        return self.players[start_idx:] + self.players[:start_idx]

    @staticmethod
    def trick_winner(trick: List[Card], players: List[Player]) -> Player:
        lead = trick[0].suit
        # this list comprehension makes a list of tuples card value and player
        # of all played cards that are the same suit as the lead
        valid = [
            (c.value, p) for c, p in zip(trick, players) if c.suit == lead
        ]
        # The player with the maximum valid card is returned
        return max(valid)[1]

    @staticmethod
    def count_points(tricks: Dict[str, Deck]) -> Dict[str, int]:
        return {n: sum(c.points for c in cards) for n, cards in tricks.items()}

if __name__ == "__main__":
    # Read player names from the command line
    player_names = sys.argv[1:]
    game = HeartsGame(*player_names)
    game.play()



#
# Running Mypy or some notes about Mypy
#


# adding the type:ignore to an import statement will have mypyignore the warning
# that a third party package does not contain type hints
 3 import numpy as np  # type: ignore

# mypy reads a config file where it is easier and cleaner to deal with multiple
# imports and what to ignore using module specific sections such as [mypy-numpy].
# Many options can be set for each package in the config file
# https://mypy.readthedocs.io/en/stable/config_file.html

# Config file
# mypy.ini
#
# [mypy]
#
# [mypy-numpy]
# ignore_missing_imports = True

#
# Adding Stubs
#

# Stubs allow the user to add types for a non standard Python library using a text
# file that contains method and function signatures. The stub file only contains
# type hints for variables, attributes, functions, and methods. The implementations
# are replaced by ... markers. This lets Mypy recognize type bugs on imported
# modules.

# A stub example:
# parse.pyi

from typing import Any, Mapping, Optional, Sequence, Tuple, Union

class Result:
    def __init__(
        self,
        fixed: Sequence[str],
        named: Mapping[str, str],
        spans: Mapping[int, Tuple[int, int]],
    ) -> None: ...
    def __getitem__(self, item: Union[int, str]) -> str: ...
    def __repr__(self) -> str: ...

def parse(
    format: str,
    string: str,
    evaluate_result: bool = ...,
    case_sensitive: bool = ...,
) -> Optional[Result]: ...

#
# Typeshed
#

# Typeshed is a Github repository that contains type hints, allowing these user
# created or package owner created stubs to be shareable, although adding type
# hints into the source code itself is preferred.
