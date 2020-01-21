# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


from src.biosim.animals import BaseAnimal, Carnivore, Herbivore
import pytest
import unittest.mock as mock

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
    Carnivore.set_parameters(**carnivore_parameters_right)
    Herbivore.set_parameters(**herbivore_parameters_right)


def return_0():
    return 0

def return_negative(arg1, arg2):
    return -1

class TestAnimal:
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
        reset_parameters()
        # Will fail if parameters are given as a dictionary and not unpacked

    def test_init(self):
        test_animal = BaseAnimal(10, 20)
        assert hasattr(test_animal, 'age')
        assert test_animal.age is not None
        assert hasattr(test_animal, 'weight')
        assert test_animal.weight is not None
        assert hasattr(test_animal, 'fitness')
        assert test_animal.fitness is not None
        assert 0 <= test_animal.fitness <= 1

    def test_fitness(self):
        """ Checks if calling fitness without updating weight
            or age will produce the same result."""
        test_animal = BaseAnimal()
        old = test_animal.fitness
        test_animal.feed(200)
        new = test_animal.fitness
        assert new > old

        test_animal = BaseAnimal()
        old = test_animal.fitness
        new = test_animal.fitness
        assert old == new

    def test_age(self):
        test_animal = BaseAnimal()
        test_animal.age = 20
        assert test_animal.age == 20
        test_animal.age += 20
        assert test_animal.age == 40
        assert test_animal._compute_fitness

    def test_age_one_year(self):
        test_animal = BaseAnimal()
        test_animal.age_one_year()
        assert test_animal.age == 1

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
        weight = animal.weight
        birth = animal.birth(10000)
        assert isinstance(birth, BaseAnimal)
        assert animal.weight == weight - birth.weight * birth.xi

        animal = BaseAnimal(10, 8.2)
        birth = animal.birth(10000)
        assert birth == 0

        animal.set_parameters(zeta=0.5)
        for _ in range(1000):
            animal = BaseAnimal(10, 60)
            birth = animal.birth(10000)
            try:
                baby_baby = birth.birth(10000)
                assert baby_baby == 0
            except AttributeError:
                pass
        reset_parameters()

        with mock.patch('random.random', return_0()):
            animal = BaseAnimal()
            assert animal.birth(10) == 0

    def test_death(self):
        animal = BaseAnimal(50, 1.4)
        list_ = []
        for _ in range(100):
            list_.append(animal.death())
        assert True in list_
        assert False in list_

        animal_2 = BaseAnimal(50, 0)
        for _ in range(100):
            assert animal_2.death()

    def test_lose_weight(self):
        animal = BaseAnimal()
        weight = animal.weight
        animal.lose_weight()
        assert animal.weight == weight - animal.eta * weight


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
        weight_start = herb.weight
        food = herb.feed(15)
        weights_end = herb.weight
        assert food == 5
        assert weight_start < weights_end
        assert pytest.approx(weights_end - weight_start, 1e-06) == herb.beta * herb.F

        herb = Herbivore()
        weight_start = herb.weight
        food = herb.feed(5)
        weights_end = herb.weight
        assert food == 0
        assert weight_start < weights_end
        assert pytest.approx(weights_end - weight_start, 1e-06) == herb.beta * 5

        herb = Herbivore()
        weight_start = herb.weight
        food = herb.feed(0)
        weights_end = herb.weight
        assert food == 0
        assert weight_start == weights_end


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
        assert length_b < length_a
        assert weight_a < weight_b
        assert weight_b - weight_a <= carnivore.F * carnivore.beta
        # Should add tests that changes DeltaPhiMax and checks
        # that part of the code
        carnivore.set_parameters(DeltaPhiMax=0.5)
        carnivore = Carnivore(5, 100)
        assert carnivore.fitness > 0.5
        sorted_list = sorted(herbivore_list, key=lambda var: var.fitness)
        for herbivore in sorted_list:
            herbivore.weight = 200
            herbivore._compute_fitness = False
            herbivore._fitness = 0.0
        times_to_eat = len(sorted_list)
        herbivores_eaten = 0
        while len(sorted_list) > 0:
            carnivore.feed(sorted_list)
            herbivores_eaten += 1
        assert herbivores_eaten == times_to_eat
        reset_parameters()


class TestAnimalSpecialCases:
    def test_birth_weight_0(self):
        with mock.patch('random.gauss', return_negative):
            animal = BaseAnimal()
            assert animal.weight == 0

