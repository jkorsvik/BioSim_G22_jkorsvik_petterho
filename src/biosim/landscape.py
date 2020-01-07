# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


class Cell:
    def __init__(self):
        self.herbivores = []
        self.carnivore = []
        raise NotImplementedError

    @property
    def num_carnivore(self):
        return len(self.carnivore)

    @property
    def num_herbivore(self):
        return len(self.herbivores)

    @property
    def num_animals(self):
        return self.num_carnivore + self.num_herbivore

class Ocean(Cell):
    def __init__(self):
        raise NotImplementedError


class Mountain(Cell):
    def __init__(self):
        raise NotImplementedError


class Desert(Cell):
    def __init__(self):
        raise NotImplementedError


class Savanna(Cell):
    f_max = 300.0
    alpha = 0.3

    def __init__(self):
        raise NotImplementedError

    def grow(self):
        raise NotImplementedError


class Jungle(Cell):
    f_max = 800.0

    def __init__(self):
        raise NotImplementedError

    def grow(self):

        raise NotImplementedError


class Map:
    def __init__(self):pass