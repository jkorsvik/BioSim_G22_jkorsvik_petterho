# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import pytest
import textwrap
from src.biosim.simulation import BioSim
from src.biosim.island import *
from src.biosim.landscape import *

@pytest.fixture
def plain_map_string():
    return Island.clean_multi_line_string("OOOO\nOJSO\nOOOO")

@pytest.fixture
def test_island():
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
    ini_herbs = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 40}
                for _ in range(100)
            ],
        }
    ]
    ini_carn = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Carnivore", "age": 2, "weight": 20}
                for _ in range(10)
            ],
        }
    ]
    test_island = Island(geogr, ini_herbs)
    test_island.add_population(ini_carn)

    return test_island


class TestIsland:

    # Tests for the implementation-methods

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


    def test_simulate_one_year(self):
        assert False
