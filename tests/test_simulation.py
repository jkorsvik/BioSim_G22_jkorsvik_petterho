# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import pytest
import textwrap
import os
from src.biosim.simulation import BioSim, load_sim, save_sim
from src.biosim.landscape import Ocean, Mountain, Jungle, Desert, Savanna
from src.biosim.animals import Herbivore, Carnivore


def test_save_sim():
    # Cant be checked from here with the current setup
    assert False


def test_load_sim():
    # Didnt bother
    assert False


class TestSimulation:
    def test_init(self):
        assert False

    def test_set_animal_parameters(self):
        BioSim.set_animal_parameters('Herbivore', {'mu': 3.9})
        assert Herbivore.mu == 3.9
        with pytest.raises(KeyError):
            BioSim.set_animal_parameters('Shark',
                                         {'mu': 0.5, 'lambda_': 0.5})
        with pytest.raises(ValueError):
            BioSim.set_animal_parameters('Herbivore',
                                         {'mu': 45, 'lambda_': -5})
        with pytest.raises(TypeError):
            BioSim.set_animal_parameters('Herbivore',
                                         {'mu': 45, 'badabom': 0.5})
        assert Herbivore.mu == 3.9
        BioSim.set_animal_parameters('Herbivore', {'mu': 0.4})
        assert Herbivore.mu == 0.4

    def test_set_landscape_parameters(self):
        BioSim.set_landscape_parameters('S', {'alpha': 3.9})
        assert Savanna.alpha == 3.9
        with pytest.raises(KeyError):
            BioSim.set_landscape_parameters('B',
                                         {'alpha': 42, 'f_max': 42})
        with pytest.raises(ValueError):
            BioSim.set_landscape_parameters('S',
                                         {'alpha': 42, 'f_max': -5})
        with pytest.raises(TypeError):
            BioSim.set_landscape_parameters('S',
                                         {'alpha': 42, 'maximus':42})
        assert Savanna.alpha == 3.9
        BioSim.set_landscape_parameters('S',
                                        {'alpha': 0.3, 'f_max': 300})
        assert Savanna.alpha == 0.3

    def test_clean_simulation(self):
        assert False

    def test_simulate(self):
        assert False

    def test_add_population(self):
        sim = BioSim()
        assert sim.island.map[(1, 2)].num_animals == 0
        sim.add_population([{'loc': (1, 2),
                             'pop': [{"species": "Herbivore",
                                      "age": 5,
                                      "weight": 40},
                                     {"species": "Carnivore",
                                      "age": 10,
                                      "weight": 14.5}
                                     ]
                             }])
        assert sim.island.map[(1, 2)].num_animals == 2

    def test_year(self):
        sim = BioSim()
        assert sim.year == 0
        sim.clean_simulation(1)
        assert sim.year == 1

    def test_num_animals(self):
        sim = BioSim()
        assert sim.num_animals == 190

    def test_num_animals_per_species(self):
        sim = BioSim()
        num_animals = sim.num_animals_per_species
        assert num_animals['Herbivore'] == 150
        assert num_animals['Carnivore'] == 40

    def test_animal_distribution(self):
        sim = BioSim()
        sim.clean_simulation(30)
        animal_distribution = sim.animal_distribution
        assert False

    def test_make_movie(self):
        sim = BioSim(img_base=r'..\images_and_movies\test_sim')
        sim.simulate(50)
        sim.make_movie()
        assert os.path.isfile(r'..\images_and_movies\test_sim.mp4')
