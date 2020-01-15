# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


import src.biosim.landscape as ls
import src.biosim.animals as ani
import pytest


@pytest.fixture
def parameters_savanna():
    return {'passable': False,
            'f_max': 100,
            'alpha': 1
            }


@pytest.fixture
def default_parameters_savanna():
    return {'f_max': 300,
            'alpha': 0.3
            }


@pytest.fixture
def animal_list():
    """
    Must be to herbivores and one carnivore. (At least that maybe)

    Returns
    -------

    """
    return [
        {'species': 'Herbivore', 'age': 10, 'weight': 100},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 50},
            ]


@pytest.fixture
def carnivore_list():
    return [
        {'species': 'Carnivore', 'age': 10, 'weight': 100},
        {'species': 'Carnivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 50},
            ]


@pytest.fixture
def jungle_many_animals():
    list_tuple = []
    for x in range(10):
        for y in range(5, 20):
            list_tuple.append((x, y))
    jungle = ls.Jungle()
    for x, y in list_tuple:
        jungle.herbivores.append(ani.Herbivore(x, y))
    return jungle


@pytest.fixture
def jungle_with_animals(animal_list):
    jungle = ls.Jungle()
    jungle.add_animals(animal_list)
    return jungle


class TestCell:
    def test_init(self):
        cell = ls.BaseCell()
        assert type(cell.herbivores) is list
        assert type(cell.carnivores) is list
        assert cell.fodder == 0

    def test_feed_herbivores(self):
        jungle = ls.Jungle()
        jungle.herbivores.append(ani.Herbivore())
        jungle.fodder = 1
        jungle.feed_herbivores()
        assert jungle.fodder == 0

    def test_feed_carnivores(self, jungle_many_animals, carnivore_list):
        jungle_many_animals.add_animals(carnivore_list)
        num_herbivores = jungle_many_animals.num_herbivores
        for _ in range(10):
            jungle_many_animals.feed_carnivores()
        print(jungle_many_animals.num_herbivores, num_herbivores)
        assert jungle_many_animals.num_herbivores < num_herbivores

    def test_feed_all(self, jungle_many_animals, carnivore_list):
        self.test_feed_herbivores()
        self.test_feed_carnivores(jungle_many_animals, carnivore_list)

    def test_age_pop(self, jungle_with_animals):
        age_herbivore0 = jungle_with_animals.herbivores[0].age
        age_herbivore1 = jungle_with_animals.herbivores[1].age
        age_carnivore0 = jungle_with_animals.carnivores[0].age
        jungle_with_animals.age_pop()
        assert age_herbivore0 < jungle_with_animals.herbivores[0].age
        assert age_herbivore1 < jungle_with_animals.herbivores[1].age
        assert age_carnivore0 < jungle_with_animals.carnivores[0].age

    def test_die(self, jungle_many_animals, carnivore_list):
        num_animals = jungle_many_animals.num_animals
        jungle_many_animals.die()
        assert num_animals > jungle_many_animals.num_animals
        jungle = ls.Jungle()
        jungle.add_animals(carnivore_list)
        carnivore0 = jungle.carnivores[0]
        carnivore0._fitness = 0
        carnivore0._compute_fitness = False
        carnivore1 = jungle.carnivores[1]
        carnivore1._fitness = 1
        carnivore0._compute_fitness = False
        jungle.die()
        assert carnivore0 not in jungle.carnivores
        assert carnivore1 in jungle.carnivores

    def test_num_carnivore(self):
        cell = ls.BaseCell()
        assert cell.num_carnivores == 0

    def test_num_herbivore(self):
        cell = ls.BaseCell()
        assert cell.num_herbivores == 0

    def test_num_animals(self):
        cell = ls.BaseCell()
        carnivores = cell.num_carnivores
        herbivores = cell.num_herbivores
        assert cell.num_animals == carnivores + herbivores

    def test_meat_for_carnivores(self):
        jungle = ls.Jungle()
        jungle.add_animals([{'species': 'Herbivore',
                             'age': 10, 'weight': 100}])
        assert type(jungle.meat_for_carnivores) is float or \
            type(jungle.meat_for_carnivores) is int
        assert jungle.meat_for_carnivores == 100

    def test_set_parameters(self, parameters_savanna,
                            default_parameters_savanna):
        savanna = ls.Savanna()
        savanna.set_parameters(**parameters_savanna)
        assert savanna.f_max == parameters_savanna['f_max']
        assert savanna.alpha == parameters_savanna['alpha']
        savanna.set_parameters(**default_parameters_savanna)
        assert savanna.f_max == default_parameters_savanna['f_max']
        assert savanna.alpha == default_parameters_savanna['alpha']
        with pytest.raises(TypeError):
            savanna.set_parameters(sun=0)

    def test_add_animals(self, animal_list):
        jungle = ls.Jungle()
        jungle.add_animals(animal_list)
        assert jungle.num_herbivores == 2
        assert jungle.num_carnivores == 1
        assert jungle.num_animals == len(animal_list)
        herbivore0 = jungle.herbivores[0]
        herbivore1 = jungle.herbivores[1]
        carnivore0 = jungle.carnivores[0]
        assert herbivore0.age == animal_list[0]['age']
        assert herbivore0.weight == animal_list[0]['weight']
        assert herbivore1.age == animal_list[1]['age']
        assert herbivore1.weight == animal_list[1]['weight']
        assert carnivore0.age == animal_list[2]['age']
        assert carnivore0.weight == animal_list[2]['weight']

    def test_lose_weight(self, jungle_with_animals):
        herbivore0_weight = jungle_with_animals.herbivores[0].weight
        herbivore1_weight = jungle_with_animals.herbivores[1].weight
        carnivore0_weight = jungle_with_animals.carnivores[0].weight
        jungle_with_animals.lose_weight()
        assert herbivore0_weight > jungle_with_animals.herbivores[0].weight
        assert herbivore1_weight > jungle_with_animals.herbivores[1].weight
        assert carnivore0_weight > jungle_with_animals.carnivores[0].weight

    def test_procreate(self, jungle_with_animals, animal_list):
        # Works only with two or more herbivores and one or zero carnivores
        num_herbivores_start = jungle_with_animals.num_herbivores
        num_carnivores_start = jungle_with_animals.num_carnivores
        for _ in range(100):
            jungle_with_animals.procreate()
        assert jungle_with_animals.num_herbivores > num_herbivores_start
        assert jungle_with_animals.num_carnivores == num_carnivores_start
        jungle_with_animals.add_animals(animal_list)
        for _ in range(100):
            jungle_with_animals.procreate()
        assert jungle_with_animals.num_herbivores > num_herbivores_start
        assert jungle_with_animals.num_carnivores > num_carnivores_start

    def test_sort_by_fitness(self, jungle_many_animals):
        jungle = jungle_many_animals
        jungle.herbivores = jungle.sort_by_fitness(jungle.herbivores)
        x = 0
        for herbivore in jungle.herbivores:
            assert x < herbivore.fitness
            x = herbivore.fitness


class TestOcean:
    def test_init(self):
        ocean = ls.Ocean()
        assert type(ocean.herbivores) is list
        assert type(ocean.carnivores) is list
        assert ocean.fodder == 0


class TestMountain:
    def test_init(self):
        mountain = ls.Mountain()
        assert type(mountain.herbivores) is list
        assert type(mountain.carnivores) is list
        assert mountain.fodder == 0


class TestDesert:
    def test_init(self):
        desert = ls.Desert()
        assert type(desert.herbivores) is list
        assert type(desert.carnivores) is list
        assert desert.fodder == 0


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
    def test_set_parameters_only_changes_one_class(self, parameters_savanna,
                                                   default_parameters_savanna):
        jungle = ls.Jungle()
        savanna = ls.Savanna()

        savanna.set_parameters(parameters_savanna)
        assert savanna.f_max == parameters_savanna['f_max']
        assert savanna.alpha == parameters_savanna['alpha']
        assert jungle.f_max == 800
        savanna.set_parameters(default_parameters_savanna)
