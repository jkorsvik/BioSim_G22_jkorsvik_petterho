# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


import src.biosim.landscape as ls


class TestCell:
    def test_init(self):
        cell = ls.Cell()
        assert cell.herbivores is list
        assert cell.carnivores is list
        assert cell.fodder == 0
        
    def test_num_carnivore(self):
        cell = ls.Cell()
        assert cell.num_carnivore == 0

    def test_num_herbivore(self):
        cell = ls.Cell()
        assert cell.num_herbivore == 0

    def test_num_animals(self):
        cell = ls.Cell()
        carnivores = cell.num_carnivore
        herbivores = cell.num_herbivore
        assert cell.num_animals == carnivores + herbivores


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
        assert savanna.herbivores is list
        assert savanna.carnivores is list
        assert savanna.fodder == ls.Savanna.f_max

    def test_grow(self):
        savanna = ls.Savanna()
        savanna.fodder = 0
        savanna.grow()
        assert savanna.fodder < ls.Savanna.f_max
        assert savanna.fodder > 0

    def test_change_parameters(self):
        assert False


class TestJungle:
    def test_init(self):
        jungle = ls.Jungle()
        assert jungle.herbivores is list
        assert jungle.carnivores is list
        assert jungle.fodder == ls.Jungle.f_max

    def test_grow(self):
        jungle = ls.Jungle()
        jungle.fodder = 0
        jungle.grow()
        assert jungle.fodder == ls.Jungle.f_max

