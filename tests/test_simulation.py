# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import pytest


@pytest.fixture
def dont_know():
    return None


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

    # Tests for the implementation-methods
    def test_migrate(self):
        assert False

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


