# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"
from src.biosim.animals import Animal


class MyList(list):
    def __init__(self, *args):
        super(MyList, self).__init__(args)

    def __sub__(self, other):
        return self.__class__(*[item for item in self if item not in other])

class TestAnimal:
    def test_init(self):
        test_animal = Animal(10, 20, (1, 3))
        assert hasattr(test_animal, 'age')
        assert test_animal.age is not None
        assert hasattr(test_animal, 'weight')
        assert test_animal.weight is not None
        assert hasattr(test_animal, 'fitness')
        assert test_animal.fitness is not None
        assert 0 <= test_animal.fitness <= 1
        assert hasattr(test_animal, 'location')
        assert test_animal.location is not None

    def test_migration(self):
        """
        Test if location has not changed more than by a increment of 1. will
        fail if location has changed by one in x- and in y-direction.

        """
        test_animal = Animal(10, 20, (1, 3))
        old = test_animal.position
        test_animal.migrate()
        new = test_animal.position
        delta = [a - b for a, b in zip(new, old)]
        assert abs(sum(delta)) == 1 or sum(delta) == 0


    def test_birth(self):
        assert False

    def test_death(self):
        assert False


class TestHerbivore:
    def test_init(self):
        assert False

    def test_feed(self):
        assert False


class TestCarnivore:
    def test_init(self):
        assert False

    def test_feed(self):
        assert False
