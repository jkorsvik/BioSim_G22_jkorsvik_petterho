# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


from src.biosim.animals import BaseAnimal, Carnivore, Herbivore
import pytest
from pprint import pprint


@pytest.fixture
def carnivore_parameters_right():
    return {'eta': 0.125, 'phi_age': 0.4, 'DeltaPhiMax': 10.0}


@pytest.fixture
def carnivore_parameters_wrong():
    return {'zettet': 7}


@pytest.fixture

def herbivore_list():
    list_ = []
    for x in range(10):
        for y in range(5, 20):
            list_.append((x, y))
    herb_list = []
    for x, y in list_:
        herb_list.append(Herbivore(x, y))

    return herb_list


def reset_parameters():
    herbivore_parameters_right = {'w_birth': 8.0,
                                  'sigma_birth': 1.5,
                                  'beta': 0.9,
                                  'eta': 0.05,
                                  'a_half': 40.0,
                                  'phi_age': 0.2,
                                  'w_half': 10.0,
                                  'phi_weight': 0.1,
                                  'mu': 0.25,
                                  'lambda_': 1.0,
                                  'gamma': 0.2,
                                  'zeta': 3.5,
                                  'xi': 1.2,
                                  'omega': 0.4,
                                  'F': 10.0}
    carnivore_parameters_right = {'w_birth': 6.0,
                                  'sigma_birth': 1.0,
                                  'beta': 0.75,
                                  'eta': 0.125,
                                  'a_half': 60.0,
                                  'phi_age': 0.4,
                                  'w_half': 4.0,
                                  'phi_weight': 0.4,
                                  'mu': 0.4,
                                  'lambda_': 1.0,
                                  'gamma': 0.8,
                                  'zeta': 3.5,
                                  'xi': 1.1,
                                  'omega': 0.9,
                                  'F': 50.0,
                                  'DeltaPhiMax': 10.0}
    Carnivore.set_parameters(carnivore_parameters_right)
    Herbivore.set_parameters(herbivore_parameters_right)


class TestAnimal:
    def test_set_parameters(self):
        animal = Carnivore(30, 10)
        animal.set_parameters({'eta': 0.03,
                               'phi_age': 0.3,
                               'DeltaPhiMax': 8.0})
        assert animal.eta == 0.03
        assert animal.phi_age == 0.3

        with pytest.raises(NameError):
            animal.set_parameters({'zettet': 0.5})

        with pytest.raises(ValueError):
            animal.set_parameters({'eta': 4})

        reset_parameters()
        assert animal.eta == 0.125

    def test_set_parameters(self, carnivore_parameters_right,
                            carnivore_parameters_wrong):
        carnivore = Carnivore(30, 10)
        with pytest.raises(TypeError):
            carnivore.set_parameters(**carnivore_parameters_wrong)
        carnivore.set_parameters(eta=1, phi_age=200)
        assert carnivore.eta == 1
        assert carnivore.phi_age == 200
        carnivore.set_parameters(**carnivore_parameters_right)
        assert carnivore.eta == 0.125
        assert carnivore.phi_age == 0.4

    def test_init(self):
        test_animal = BaseAnimal(10, 20)
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
        """
        test_animal = Animal(10, 20, (1, 3))
        old = test_animal.position
        test_animal.migrate()
        new = test_animal.position
        delta = [a - b for a, b in zip(new, old)]
        assert abs(sum(delta)) == 1 or sum(delta) == 0"""
        pass

    def test_fitness(self):
        """ Checks if calling fitness without updating weight
            or age will produce the same result."""
        test_animal = BaseAnimal()
        old = test_animal.fitness
        test_animal.feed(200)
        new = test_animal.fitness
        print(old, new)
        assert new > old

        test_animal = BaseAnimal()
        old = test_animal.fitness
        new = test_animal.fitness
        print(old, new)
        assert old == new

    def test_age(self):
        test_animal = BaseAnimal()
        test_animal.age = 20
        assert test_animal.weight == 20
        test_animal.weight += 20
        assert test_animal.weight == 40
        assert test_animal._compute_fitness

    def test_weight(self):
        test_animal = BaseAnimal()
        test_animal.weight = 20
        assert test_animal.weight == 20
        test_animal.weight += 20
        assert test_animal.weight == 40
        assert test_animal._compute_fitness

    def test_has_moved(self):
        test_animal = BaseAnimal()
        assert test_animal.has_moved is False
        assert test_animal.has_moved is True

    def test_reset_has_moved(self):
        test_animal = BaseAnimal()
        has_moved = test_animal.has_moved
        assert not has_moved
        assert test_animal._has_moved
        test_animal.reset_has_moved()
        assert not test_animal._has_moved

    def test_will_migrate(self):
        will_migrate = 0
        for _ in range(1000):
            test_animal = BaseAnimal()
            test_animal._compute_fitness = False
            test_animal._fitness = 1.0
            if test_animal.will_migrate():
                will_migrate += 1
        assert 200 < will_migrate < 300

    def test_birth(self):
        animal = BaseAnimal(10, 60)
        birth = animal.birth(10000)
        assert isinstance(birth, BaseAnimal)

    def test_death(self):
        animal = BaseAnimal(50, 1.4)
        list_ = []
        for _ in range(100):
            list_.append(animal.death())
        assert True in list_

        animal_2 = BaseAnimal(50, 0)
        for _ in range(100):
            assert animal_2.death()


class TestHerbivore:
    def test__init__(self):
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
        assert b - a <= herb.beta * herb.F


class TestCarnivore:
    def test_init(self):
        test_carnivore = Carnivore(10, 20)
        assert hasattr(test_carnivore, 'age')
        assert test_carnivore.age is not None
        assert hasattr(test_carnivore, 'weight')
        assert test_carnivore.weight is not None
        assert hasattr(test_carnivore, 'fitness')
        assert test_carnivore.fitness is not None
        assert 0 <= test_carnivore.fitness <= 1

    def test_kill_or_not(self):
        carnivore = Carnivore()
        carnivore._compute_fitness = False
        herbivore = Herbivore()
        herbivore._compute_fitness = False
        carnivore._fitness = 1
        herbivore._fitness = 0.5
        kills = 0
        for _ in range(1000):
            if carnivore.kill_or_not(herbivore):
                kills += 1
        assert 30 < kills < 70

    def test_eat(self):
        carnivore = Carnivore()
        carnivore.weight = 30
        carnivore.eat(1000, 0)
        assert carnivore.weight == 30 + carnivore.F * carnivore.beta
        carnivore.weight = 30
        carnivore.eat(10, 0)
        assert carnivore.weight == 30 + 10 * carnivore.beta
        carnivore.weight = 30
        carnivore.eat(1000, 45)
        assert carnivore.weight == 30 + 5 * carnivore.beta

    def test_feed(self, herbivore_list):
        carnivore = Carnivore(5, 100)
        sorted_list = sorted(herbivore_list, key=lambda var: var.fitness)
        length_a = len(sorted_list)
        weight_a = carnivore.weight
        new_list = carnivore.feed(sorted_list)
        length_b = len(new_list)
        weight_b = carnivore.weight
        print(length_a, length_b, weight_a, weight_b)
        assert length_b < length_a
        assert weight_a < weight_b
        assert weight_b - weight_a <= carnivore.F*carnivore.beta
        # Should add tests that changes DeltaPhiMax and checks
        # that part of the code
