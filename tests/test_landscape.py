# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"


from biosim.landscape import BaseCell, Ocean, Mountain, Desert, \
    Savanna, Jungle
from biosim.animals import Herbivore, Carnivore
import pytest
import math


class TestBaseCell:
    def test_set_parameters(self, parameters_savanna,
                            default_parameters_savanna):
        savanna = Savanna()
        savanna.set_parameters(**parameters_savanna)
        assert savanna.f_max == parameters_savanna['f_max']
        assert savanna.alpha == parameters_savanna['alpha']
        savanna.set_parameters(**default_parameters_savanna)
        assert savanna.f_max == default_parameters_savanna['f_max']
        assert savanna.alpha == default_parameters_savanna['alpha']
        with pytest.raises(TypeError):
            savanna.set_parameters(sun=0)

    def test_init(self):
        cell = BaseCell()
        assert type(cell.herbivores) is list
        assert type(cell.carnivores) is list
        assert cell.fodder == 0

    def test_grow(self):
        cell = BaseCell()
        cell.grow()
        assert True

    def test_add_animals(self, animal_list):
        jungle = Jungle()
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

        animal_list_with_wrong_parameter = [
            {'species': 'Carnivore', 'age': 0.5, 'weight': 100}]
        with pytest.raises(ValueError):
            jungle.add_animals(animal_list_with_wrong_parameter)

        animal_list_with_wrong_parameter = [
            {'species': 'Carnivore', 'age': 3, 'weight': -10}]
        with pytest.raises(ValueError):
            jungle.add_animals(animal_list_with_wrong_parameter)

    def test_add_migrated_herb(self):
        cell = BaseCell()
        assert len(cell.herbivores) == 0
        cell.add_migrated_herb(Herbivore())
        assert len(cell.herbivores) == 1

    def test_add_migrated_carn(self):
        cell = BaseCell()
        assert len(cell.carnivores) == 0
        cell.add_migrated_carn(Carnivore())
        assert len(cell.carnivores) == 1

    def test_remove_migrated_herb(self):
        cell = BaseCell()
        assert len(cell.herbivores) == 0
        herbivore = Herbivore()
        cell.add_migrated_herb(herbivore)
        assert len(cell.herbivores) == 1
        cell.remove_migrated_herb(herbivore)
        assert len(cell.herbivores) == 0

    def test_remove_migrated_carn(self):
        cell = BaseCell()
        assert len(cell.carnivores) == 0
        carnivore = Carnivore()
        cell.add_migrated_carn(carnivore)
        assert len(cell.carnivores) == 1
        cell.remove_migrated_carn(carnivore)
        assert len(cell.carnivores) == 0

    def test_migrate(self, jungle_many_animals, prob_herb, prob_carn):

        moved_herb, moved_carn = jungle_many_animals.migrate(prob_herb,
                                                             prob_carn)
        for loc, herb in moved_herb:
            assert herb not in jungle_many_animals.herbivores
            assert loc != (1, 1)
            assert loc == (1, 2) or loc == (2, 1)
        for loc, carn in moved_carn:
            assert carn not in jungle_many_animals.carnivores
            assert loc != (1, 1)
            assert loc == (1, 2) or loc == (2, 1)

        moved_herb, moved_carn = jungle_many_animals.migrate(prob_herb,
                                                             prob_carn)
        assert len(moved_herb) == 0 and len(moved_carn) == 0

        moved_herb, moved_carn = jungle_many_animals.migrate(prob_herb=None,
                                                             prob_carn=None)
        assert len(moved_herb) == 0 and len(moved_carn) == 0

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

    def test_lose_weight(self, jungle_with_animals):
        herbivore0_weight = jungle_with_animals.herbivores[0].weight
        herbivore1_weight = jungle_with_animals.herbivores[1].weight
        carnivore0_weight = jungle_with_animals.carnivores[0].weight
        jungle_with_animals.lose_weight()
        assert herbivore0_weight > jungle_with_animals.herbivores[0].weight
        assert herbivore1_weight > jungle_with_animals.herbivores[1].weight
        assert carnivore0_weight > jungle_with_animals.carnivores[0].weight

    def test_sort_by_fitness(self, jungle_many_animals):
        jungle = jungle_many_animals
        jungle.herbivores = jungle.sort_by_fitness(jungle.herbivores)
        x = 0
        for herbivore in jungle.herbivores:
            assert x < herbivore.fitness
            x = herbivore.fitness

    def test_feed_all(self, jungle_many_animals, carnivore_list):
        self.test_feed_herbivores()
        self.test_feed_carnivores(jungle_many_animals, carnivore_list)

    def test_feed_herbivores(self):
        jungle = Jungle()
        jungle.herbivores.append(Herbivore())
        jungle.fodder = 1
        jungle.feed_herbivores()
        assert jungle.fodder == 0

    def test_feed_carnivores(self, jungle_many_animals, carnivore_list):
        jungle_many_animals.add_animals(carnivore_list)
        num_herbivores = jungle_many_animals.num_herbivores
        for _ in range(10):
            jungle_many_animals.feed_carnivores()
        assert jungle_many_animals.num_herbivores < num_herbivores

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
        jungle = Jungle()
        jungle.add_animals(carnivore_list)
        carnivore0 = jungle.carnivores[0]
        carnivore0._fitness = 0
        carnivore0._compute_fitness = False
        carnivore1 = jungle.carnivores[1]
        carnivore1._fitness = 1
        carnivore1._compute_fitness = False
        jungle.die()
        assert carnivore0 not in jungle.carnivores
        assert carnivore1 in jungle.carnivores

    def test_propensity(self):
        jungle = Jungle()
        jungle.add_migrated_herb(Herbivore())
        jungle.add_migrated_carn(Carnivore())
        lambda_herb = Herbivore.lambda_
        epsilon_herb = jungle.fodder / (2 * Herbivore.F)
        propensity_herbivore = math.exp(lambda_herb * epsilon_herb)
        lambda_carn = Carnivore.lambda_
        epsilon_carn = jungle.meat_for_carnivores / (2 * Carnivore.F)
        propensity_carnivore = math.exp(lambda_carn * epsilon_carn)
        propensity = jungle.propensity
        assert propensity['Herbivore'] == propensity_herbivore
        assert propensity['Carnivore'] == propensity_carnivore

    def test_reset_calculate_propensity(self):
        jungle = Jungle()
        jungle.propensity
        assert jungle._calculate_propensity is False
        jungle.reset_calculate_propensity()
        assert jungle._calculate_propensity is True

    def test_num_carnivore(self):
        cell = BaseCell()
        assert cell.num_carnivores == 0

    def test_num_herbivore(self):
        cell = BaseCell()
        assert cell.num_herbivores == 0

    def test_num_animals(self):
        cell = BaseCell()
        carnivores = cell.num_carnivores
        herbivores = cell.num_herbivores
        assert cell.num_animals == carnivores + herbivores

    def test_meat_for_carnivores(self):
        jungle = Jungle()
        jungle.add_animals([{'species': 'Herbivore',
                             'age': 10, 'weight': 100}])
        assert type(jungle.meat_for_carnivores) is float or \
            type(jungle.meat_for_carnivores) is int
        assert jungle.meat_for_carnivores == 100


class TestOcean:
    def test_init(self):
        ocean = Ocean()
        assert type(ocean.herbivores) is list
        assert type(ocean.carnivores) is list
        assert ocean.fodder == 0
        assert ocean.passable is False


class TestMountain:
    def test_init(self):
        mountain = Mountain()
        assert type(mountain.herbivores) is list
        assert type(mountain.carnivores) is list
        assert mountain.fodder == 0
        assert mountain.passable is False


class TestDesert:
    def test_init(self):
        desert = Desert()
        assert type(desert.herbivores) is list
        assert type(desert.carnivores) is list
        assert desert.fodder == 0
        assert desert.passable is True


class TestSavanna:
    def test_init(self):
        savanna = Savanna()
        assert type(savanna.herbivores) is list
        assert type(savanna.carnivores) is list
        assert savanna.fodder == Savanna.f_max

    def test_grow(self):
        savanna = Savanna()
        savanna.fodder = 0
        savanna.grow()
        assert savanna.fodder < Savanna.f_max
        assert savanna.fodder > 0


class TestJungle:
    def test_init(self):
        jungle = Jungle()
        assert type(jungle.herbivores) is list
        assert type(jungle.carnivores) is list
        assert jungle.fodder == Jungle.f_max

    def test_grow(self):
        jungle = Jungle()
        jungle.fodder = 0
        jungle.grow()
        assert jungle.fodder == Jungle.f_max

    def test_feed_herbivore(self, animal_list):
        test_jungle = Jungle()
        test_jungle.herbivores.append(Herbivore(5, 40))
        test_jungle.herbivores.append(Herbivore(50, 4))
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
        test_jungle.feed_herbivores()
        assert test_jungle.fodder == 0
        #  b will be last because its fitness will be higher
        assert b.weight == b_weight + 10 * 0.9
        assert a.weight == a_weight + 5 * 0.9


class TestCellsSpecialCases:
    def test_set_parameters_only_changes_one_class(self, parameters_savanna,
                                                   default_parameters_savanna):
        jungle = Jungle()
        savanna = Savanna()

        savanna.set_parameters(**parameters_savanna)
        jungle.set_parameters(f_max=800)
        assert savanna.f_max == parameters_savanna['f_max']
        assert savanna.alpha == parameters_savanna['alpha']
        assert jungle.f_max == 800
        savanna.set_parameters(**default_parameters_savanna)
