# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import pytest
import textwrap
from src.biosim.island import *
from src.biosim.landscape import *


@pytest.fixture
def plain_map_string():
    return Island.clean_multi_line_string("OOOO\nOJSO\nOOOO")


@pytest.fixture
def test_island(ini_herbs, ini_carns):
    """
    Important that all animals are inserted to one cell.
    And only uses Jungle as passable cell

    Returns
    -------
    test_island: Island
        instance of Island class
    """
    geogr = """\
            OOOO
            OJJO
            OJJO
            OOOO"""
    geogr = textwrap.dedent(geogr)
    test_island = Island(geogr, ini_herbs)
    test_island.add_population(ini_carn)

    return test_island


@pytest.fixture
def ini_herbs():
    ini_herbs = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 40}
                for _ in range(100)
            ],
        }
    ]
    return ini_herbs


@pytest.fixture
def ini_carns():
    ini_carns = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Carnivore", "age": 2, "weight": 20}
                for _ in range(10)
            ],
        }
    ]
    return ini_carns

def test_check_line_length():
    lines = ['abc', 'def']
    assert check_length(lines) is True
    lines = ['abc', 'df']
    assert check_length(lines) is False
    lines = ['bc', 'def', 'gh']
    assert check_length(lines) is False


class TestIsland:
    def test_init(self):
        assert False

    def test_num_animals(self, test_island, ini_herbs):
        assert test_island.num_animals == 110
        test_island.add_population(ini_herbs)
        assert test_island.num_animals == 210

    def test_num_animals_per_species(self, test_island, ini_herbs, ini_carns):
        assert test_island.num_animals_per_species['Carnivores'] == 10
        assert test_island.num_animals_per_species['Herbivores'] == 100
        test_island.add_population(ini_herbs)
        test_island.add_population(ini_carns)
        assert test_island.num_animals_per_species['Carnivores'] == 20
        assert test_island.num_animals_per_species['Herbivores'] == 200

    def test_clean_multiline_string(self):
        string = ' OOO\nOJO\nOOO    '
        string_cleaned = Island.clean_multi_line_string(string)
        assert string_cleaned == ['OOO', 'OJO', 'OOO']

        with pytest.raises(ValueError):
            string = 'OOO\nOJO\nOOOO'
            Island.clean_multi_line_string(string)

        with pytest.raises(ValueError):
            string = 'OOJ\nOJO\nOOO'
            Island.clean_multi_line_string(string)

        with pytest.raises(ValueError):
            string = 'OOO\nJOO\nOOO'
            Island.clean_multi_line_string(string)

    def test_make_map(self, plain_map_string, ini_herbs):
        island = Island(plain_map_string, ini_herbs)
        assert isinstance(island.map[(1, 1)], Jungle)
        assert isinstance(island.map[(1, 2)], Savanna)
        assert isinstance(island.map[(3, 3)], Ocean)

    def test_probability_calc(self, ini_herbs, ini_carns):
        island = Island('OOOO\nOJJO\nOOOO', ini_carns)
        prob_list = island.probability_calc((1, 1), Herbivore)
        assert prob_list[3][1] == 1
        island = Island('OOOOO\nOJJJO\nOJJJO\nOJJJO\nOOOOO', ini_carns)
        prob_list = island.probability_calc((2, 2), Herbivore)
        for destination, prob in prob_list:
            assert prob == 0.25
        island = Island('OOOOO\nOJJJO\nOJJJO\nOJJJO\nOOOOO', ini_carns)
        prob_list = island.probability_calc((2, 2), Herbivore)
        for destination, prob in prob_list:
            assert prob == 0.25
        island = Island('OOO\nOJO\nOOO', ini_carns)
        prob_list = island.probability_calc((1, 1), Herbivore)
        for destination, prob in prob_list:
            assert prob == 0.00


    def test_add_herb_to_new_cell(self):
        assert False

    def test_add_carn_to_new_cell(self):
        assert False

    def test_migrate(self, test_island):
        assert test_island.map[(1, 2)].num_animals == 0
        assert test_island.map[(2, 1)].num_animals == 0
        assert test_island.map[(2, 2)].num_animals == 0
        test_island.simulate_one_year()
        for loc, cell in test_island.map.items():
            print(loc, cell.num_animals)
        assert test_island.map[(1, 2)].num_animals > 10
        assert test_island.map[(2, 1)].num_animals > 10

        for year in range(20):
            test_island.simulate_one_year()

        for loc, cell in test_island.map.items():
            print(loc, cell.num_animals)
        for cell in test_island.map.values():
            if isinstance(cell, (Jungle, Savanna,
                                 Desert)):
                assert cell.num_animals > 0
            else:
                assert cell.num_animals == 0

        # Uses the fact that the animals should distribute evenly in this map
        num_animals11 = test_island.map[(1, 1)].num_animals
        num_animals12 = test_island.map[(1, 2)].num_animals
        assert num_animals12 * 0.8 < num_animals11 < num_animals12 * 1.2

    def test_migrate_from_sim(self, test_island):
        assert test_island.island_map[(1, 2)].num_animals == 0
        for year in range(10):
            test_island.simulate_one_year()
        for cell in test_island.island_map.values():
            if isinstance(cell, (simulation.Jungle, simulation.Savanna,
                                 simulation.Desert)):
                assert cell.num_animals > 0
            else:
                assert cell.num_animals == 0

        # Uses the fact that the animals should distribute evenly in this map
        num_animals11 = test_island.island_map[(1, 1)].num_animals
        num_animals12 = test_island.island_map[(1, 2)].num_animals
        print(num_animals11, num_animals12)
        assert num_animals12 * 0.8 < num_animals11 < num_animals12 * 1.2

    def test_ready_for_new_year(self):
        assert False

    def test_add_population(self, test_island):
        assert test_island.island_map[(1, 2)].num_animals == 0
        test_island.add_population([{'loc': (1, 2),
                                     'pop': [{"species": "Herbivore",
                                              "age": 5,
                                              "weight": 40},
                                             {"species": "Carnivore",
                                              "age": 10,
                                              "weight": 14.5}
                                             ]
                                     }])
        for herbivore in test_island.island_map[(1, 2)].herbivores:
            assert herbivore.age == 5
            assert herbivore.weight == 40
        for carnivore in test_island.island_map[(1, 2)].carnivores:
            assert carnivore.age == 10
            assert carnivore.weight == 14.5

    def test_feed(self, test_island):
        test_island.feed()
        assert test_island.map[(1, 1)].herbivores[-1].weight > 40
        assert test_island.map[(1, 1)].herbivores[-1].weight > 20

    def test_procreation(self, test_island):
        test_island.procreate()
        assert test_island.num_animals > 110

    def test_age_animals(self, test_island):
        test_island.age_animals()
        assert test_island.map[(1, 1)].herbivores[-1].age == 6
        assert test_island.map[(1, 1)].carnivores[-1].age == 3

    def test_age_animals_from_sim(self, test_island):
        test_island.add_population([{'loc': (1, 2),
                                     'pop': [{"species": "Herbivore",
                                              "age": 5,
                                              "weight": 40},
                                             {"species": "Carnivore",
                                              "age": 10,
                                              "weight": 14.5}
                                             ]
                                     }])
        test_island.age_animals()
        assert test_island.island_map[(1, 2)].herbivores[0].age == 6
        assert test_island.island_map[(1, 2)].carnivores[0].age == 11

    def test_lose_weight(self):
        assert False

    def test_year(self, test_island):
        assert test_island.year == 0
        test_island.simulate_one_year()
        assert test_island.year == 1
        test_island.year = 5
        assert test_island.year == 5

    def test_simulate_one_year(self):
        assert False

class TestIslandInteractions:
    def test_species_separated(self, test_island):
        for _ in range(100):
            test_island.simulate_one_year()
            for cell in test_island.map.values():
                for herbivore in cell.herbivores:
                    assert isinstance(herbivore, Herbivore)
                for carnivore in cell.carnivores:
                    assert isinstance(carnivore, Carnivore)

    def test_something(self):
        assert False


