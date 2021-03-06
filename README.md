# Functional-Programming
CS 5035 Functional Programming notes and projects

#### A. Python

This folder contains notes on Python typing.

#### B. Haskell

This folder contains Haskell and Python versions disproving Goldbach's other conjecture.
PythonVersionA attempts is Haskell inspired, but deals with infinite lists in an inelegant way - by stopping them at 6000.
PythonVersionB is slightly faster than VersionA and works by incrementing through odd numbers, checking if they are prime and if not, checking if they satisfy the Goldbach condition (if odd-prime/2 is a perfect square).
The two Lists files compare how infinite lists work in both Haskell and Python.

#### C. Haskell 2

This folder contains implementations of Haskell functions and their counterparts in Python.

#### D. Decorators

This folder contains Haskell implementations (translated from Python) of returning the nth Fibonacci number.

#### E. Functional Programming in Python

This folder contains implementations of a credit card number validation algorithm in Haskell, Python (using Pyrsistent and Toolz), and Coconut.

#### F. Amuse-Bouche

This folder contains notes on Haskell code from the 2011 talk by Mark Lentczner
(https://www.youtube.com/watch?v=b9FagOVqxmI&feature=youtu.be), and some custom
operator implementations. There is also corresponding code in Python.


#### G. Monads

This folder contains some Haskell implementations of Monads as well as monadic designs in Python, often using the PyMonad library.
