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
        list_tuple = []
        for x in range(10):
            for y in range(5, 20):
                list_tuple.append((x, y))
        jungle = ls.Jungle()
        for x, y in list_tuple:
            jungle.herbivores.append(ani.Herbivore(x, y))
        jungle.herbivores = jungle.sort_by_fitness(jungle.herbivores)
        x = 0
        for herbivore in jungle.herbivores:
            print(herbivore.fitness)
            assert x < herbivore.fitness
            x = herbivore.fitness


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
        test_jungle = ls.Jungle()
        test_jungle.herbivores.append(ani.Herbivore(5, 40))
        test_jungle.herbivores.append(ani.Herbivore(50, 4))
        test_jungle.herbivores = (
            test_jungle.sort_by_fitness(test_jungle.herbivores)
        )
        test_jungle.fodder = 15
        a_weight = test_jungle.herbivores[0].weight
        b_weight = test_jungle.herbivores[1].weight
        #  herbivore F is 10 and beta is 0.9
        #  b will eat 10 and gain 10*0.9 weight
        #  a will eat 5 and gain 5*0.9 weight
        a, b = test_jungle.herbivores
        print(a_weight)
        print(b_weight)
        test_jungle.feed_herbivores()
        print(a.weight)
        print(b.weight)
        assert test_jungle.fodder == 0
        #  b will be last because its fitness will be higher
        assert b.weight == b_weight + 10 * 0.9
        assert a.weight == a_weight + 5 * 0.9


class TestMoreThanOneCell:
    def test_set_parameters_only_changes_one_class(self, parameters):
        jungle = ls.Jungle()
        savanna = ls.Savanna()

        savanna.set_parameters(parameters)
        assert savanna.f_max == parameters['f_max']
        assert savanna.alpha == parameters['alpha']
        assert jungle.f_max == 800
