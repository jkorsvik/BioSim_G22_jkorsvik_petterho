# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


class Cell:
    def __init__(self):
        raise NotImplementedError


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
    def __init__(self):
        raise NotImplementedError

    def grow(self):
        raise NotImplementedError


class Jungle(Cell):
    def __init__(self):
        raise NotImplementedError

    def grow(self):
        raise NotImplementedError
