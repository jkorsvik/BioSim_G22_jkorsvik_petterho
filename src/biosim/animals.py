# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


class Animal:
    def __init__(self):
        raise NotImplementedError

    def migration(self):
        raise NotImplementedError

    def birth(self):
        raise NotImplementedError

    def death(self):
        raise NotImplementedError

    def feed(self):
        raise NotImplementedError


class Herbivore(Animal):
    def __init__(self):
        raise NotImplementedError

    def feed(self):
        raise NotImplementedError


class Carnivore(Animal):
    def __init__(self):
        raise NotImplementedError

    def feed(self):
        raise NotImplementedError
