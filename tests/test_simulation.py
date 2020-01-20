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
