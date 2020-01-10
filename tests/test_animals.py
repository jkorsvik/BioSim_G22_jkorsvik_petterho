# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


from src.biosim.animals import Animal, Carnivore, Herbivore
import pytest
from pprint import pprint


@pytest.fixture
def carnivore_parameters_right():
    return {'eta': 0.03, 'phi_age': 0.3, 'DeltaPhiMax': 8.0}

@pytest.fixture
def carnivore_parameters_wrong():
    return {'zettet': 7}


class TestAnimal:
    def test_init(self):
        test_animal = Animal(10, 20)
        assert hasattr(test_animal, 'age')
        assert test_animal.age is not None
        assert hasattr(test_animal, 'weight')
        assert test_animal.weight is not None
        assert hasattr(test_animal, 'fitness')
        assert test_animal.fitness is not None
        assert 0 <= test_animal.fitness <= 1


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

    def test_weight_prop(self):
        test_animal = Animal()
        test_animal.weight = 20
        assert test_animal.weight == 20

    def test_add_weight(self):
        test_animal = Animal()
        test_animal.weight = 20
        test_animal.weight += 20
        assert test_animal.weight == 40

    def test_fitness_calc(self):
        test_animal = Animal()
        old = test_animal.fitness
        test_animal.feed(200)
        new = test_animal.fitness
        print(old, new)
        assert new != old

    def test_fitness_unchanged(self):
        """ Checks if calling fitness without updating weight
            or age will produce the same result."""
        test_animal = Animal()
        old = test_animal.fitness
        new = test_animal.fitness
        print(old, new)
        assert old == new

    def test_reset_of_has_moved(self):
        test_animal = Animal()
        test_animal._has_moved = True
        test_animal.reset_has_moved()
        assert not test_animal._has_moved

    def test_birth(self):
        animal = Animal(10, 40)
        value = animal.birth(10000)
        print(value)
        assert value != 0

    def test_death(self):
        animal = Animal(50, 1.4)
        list_ = []
        for _ in range(100):
            list_.append(animal.death())
        assert True in list_

        animal_2 = Animal(50, 0)
        for _ in range(100):
            assert animal_2.death()

    def test_set_param(self, carnivore_parameters_right):
        animal = Carnivore(30, 10)
        animal.set_parameters(carnivore_parameters_right)
        assert animal.eta == 0.03
        assert animal.phi_age == 0.3


class TestHerbivore:
    def _init__herb(self):
        test_herbivore = Herbivore(10, 20)
        assert hasattr(test_herbivore, 'age')
        assert test_herbivore.age is not None
        assert hasattr(test_herbivore, 'weight')
        assert test_herbivore.weight is not None
        assert hasattr(test_herbivore, 'fitness')
        assert test_herbivore.fitness is not None
        assert 0 <= test_herbivore.fitness <= 1

    def test_feed(self):
        herb = Herbivore()
        a = herb.weight
        food = herb.feed(15)
        b = herb.weight
        assert food == 5
        assert a < b

class TestCarnivore:
    def test_init(self):
        test_herbivore = Herbivore(10, 20)
        assert hasattr(test_herbivore, 'age')
        assert test_herbivore.age is not None
        assert hasattr(test_herbivore, 'weight')
        assert test_herbivore.weight is not None
        assert hasattr(test_herbivore, 'fitness')
        assert test_herbivore.fitness is not None
        assert 0 <= test_herbivore.fitness <= 1

    def test_feed(self):

