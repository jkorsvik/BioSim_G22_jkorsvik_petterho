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
        for year in range(10):
            test_island.simulate_one_year()
        for cell in test_island.map.values():
            if isinstance(cell, (Jungle, Savanna,
                                 Desert)):
                assert cell.num_animals > 0
            else:
                assert cell.num_animals == 0

        # Uses the fact that the animals should distribute evenly in this map
        num_animals11 = test_island.map[(1, 1)].num_animals
        num_animals12 = test_island.map[(1, 2)].num_animals
        print(num_animals11, num_animals12)
        assert num_animals12 * 0.8 < num_animals11 < num_animals12 * 1.2

    def test_feed(self):
        assert False

    def test_feed_herbivores(self):
        assert False

    def test_feed_carnivores(self):
        assert False

    def test_procreation(self):
        assert False

    def test_migration(self):
        assert False

    def test_aging(self):
        assert False

    def test_simulate_one_year(self):
        assert False
