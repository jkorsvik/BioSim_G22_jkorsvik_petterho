# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import pytest
import textwrap
import src.biosim.simulation as simulation


@pytest.fixture
def test_island():
    """
    Important that all animals are inserted to one cell.
    And only uses Jungle as passable cell

    Returns
    -------
    test_island: BioSim
        instance of BioSim class
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
    test_island = simulation.BioSim(geogr, ini_herbs, 1)
    test_island.add_population(ini_carn)

    return test_island


class TestSimulation:
    def test_set_animal_parameters(self):
        assert False

    def test_set_landscape_parameters(self):
        assert False

    def test_simulate(self):
        assert False

    def test_add_population(self):
        assert False

    def test_year(self):
        assert False

    def test_num_animals(self):
        assert False

    def test_num_animals_per_species(self):
        assert False

    def test_animal_distribution(self):
        assert False

    def test_make_movie(self):
        assert False

