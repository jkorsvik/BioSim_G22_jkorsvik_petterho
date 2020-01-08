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
        assert cell.num_herbivore == 0

    def test_num_animals(self):
        cell = ls.Cell()
        carnivores = cell.num_carnivore
        herbivores = cell.num_herbivore
        assert cell.num_animals == carnivores + herbivores

    def test_set_parameters(self, parameters):
        cell = ls.Cell()
        cell.set_parameters(parameters)
        assert cell.f_max == parameters['f_max']
        assert cell.alpha == parameters['alpha']


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


class TestMoreThanOneCell:
    def test_set_parameters_only_changes_one_class(self, parameters):
        jungle = ls.Jungle()
        savanna = ls.Savanna()

        savanna.set_parameters(parameters)
        assert savanna.f_max == parameters['f_max']
        assert savanna.alpha == parameters['alpha']
        assert jungle.f_max == 800
