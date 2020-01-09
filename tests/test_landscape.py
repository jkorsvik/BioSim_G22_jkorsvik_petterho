# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


import src.biosim.landscape as ls
import src.biosim.animals as ani
import pytest


@pytest.fixture
def parameters():
    return {'f_max': 100,
            'alpha': 1
            }


@pytest.fixture
def animal_list():
    return [
        {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 8.1},
            ]


class TestCell:
    def test_init(self):
        cell = ls.Cell()
        assert type(cell.herbivores) is list
        assert type(cell.carnivores) is list
        assert cell.fodder == 0

    def test_feed_herbivores(self):
        jungle = ls.Jungle()
        jungle.herbivores.append(ani.Herbivore())
        jungle.fodder = 1
        jungle.feed_herbivores()
        assert jungle.fodder == 0

    def test_num_carnivore(self):
        cell = ls.Cell()
        assert cell.num_carnivores == 0

    def test_num_herbivore(self):
        cell = ls.Cell()
        assert cell.num_herbivores == 0

    def test_num_animals(self):
        cell = ls.Cell()
        carnivores = cell.num_carnivores
        herbivores = cell.num_herbivores
        assert cell.num_animals == carnivores + herbivores

    def test_set_parameters(self, parameters):
        savanna = ls.Savanna()
        savanna.set_parameters(parameters)
        assert savanna.f_max == parameters['f_max']
        assert savanna.alpha == parameters['alpha']

    def test_add_animals(self, animal_list):
        jungle = ls.Jungle()
        jungle.add_animals(animal_list)
        assert jungle.num_herbivores == 2
        assert jungle.num_carnivores == 1
        assert jungle.num_animals == len(animal_list)

    def test_sort_by_fitness(self, animal_list):
        jungle = ls.Jungle()
        jungle.add_animals(animal_list)
        jungle.sort_by_fitness(jungle.herbivores)
        assert jungle.herbivores[0].age == 9


class TestOcean:
    def test_init(self):
        assert False


class TestMountain:
    def test_init(self):
        assert False


class TestDesert:
    def test_init(self):
        assert False


class TestSavanna:
    def test_init(self):
        savanna = ls.Savanna()
        assert type(savanna.herbivores) is list
        assert type(savanna.carnivores) is list
        assert savanna.fodder == ls.Savanna.f_max

    def test_grow(self):
        savanna = ls.Savanna()
        savanna.fodder = 0
        savanna.grow()
        assert savanna.fodder < ls.Savanna.f_max
        assert savanna.fodder > 0


class TestJungle:
    def test_init(self):
        jungle = ls.Jungle()
        assert type(jungle.herbivores) is list
        assert type(jungle.carnivores) is list
        assert jungle.fodder == ls.Jungle.f_max

    def test_grow(self):
        jungle = ls.Jungle()
        jungle.fodder = 0
        jungle.grow()
        assert jungle.fodder == ls.Jungle.f_max

    def test_feed_herbivore(self, animal_list):
        test_jungle = ls
        test_jungle.add_animals(animal_list)
        test_jungle.fodder = 15
        test_jungle.herbivores = (
            test_jungle.sort_by_fitness(test_jungle.herbivores)
        )
        a_weight = test_jungle.herbivores[1].weight
        b_weight = test_jungle.herbivores[0].weight
        # herbivore F is 10 and beta is 0.9
        #a will eat 10 and gain 10*0.9 weight
        #b will eat 5 and gain 5*0.9 weight
        test_jungle.feed_herbivores()
        #assert test_jungle.fodder == 0
        a, b = test_jungle.herbivores
        assert a.weight == a_weight + 10 * 0.9
        assert b.weight == b_weight + 5 * 0.9


class TestMoreThanOneCell:
    def test_set_parameters_only_changes_one_class(self, parameters):
        jungle = ls.Jungle()
        savanna = ls.Savanna()

        savanna.set_parameters(parameters)
        assert savanna.f_max == parameters['f_max']
        assert savanna.alpha == parameters['alpha']
        assert jungle.f_max == 800
