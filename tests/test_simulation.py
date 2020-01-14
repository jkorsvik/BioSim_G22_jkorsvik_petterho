# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import pytest
import textwrap
import src.biosim.simulation as simulation


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

@pytest.fixture
def test_island(ini_carns, ini_herbs):
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

    test_island = simulation.BioSim(geogr, ini_herbs, 1)
    test_island.add_population(ini_carns)

    return test_island


class TestSimulation:
    def test_set_animal_parameters(self):
        assert False

    def test_set_landscape_parameters(self):
        assert False

    def test_simulate(self):
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

    def test_year(self, test_island):
        assert test_island.year == 0
        test_island.simulate_one_year()
        assert test_island.year == 1

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


    def test_animal_distribution(self):
        assert False

    def test_make_movie(self):
        assert False


    # Tests for the implementation-methods
    def test_migrate(self, test_island):
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

        # Does not test if it checks for all animals to migrate

    def test_feed(self):
        assert False

    def test_procreation(self):
        assert False

    def test_aging(self, test_island):
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

    def test_simulate_one_year(self):
        assert False