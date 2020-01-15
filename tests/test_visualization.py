# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import pytest
import textwrap
from src.biosim.visualization import Visuals
from src.biosim.simulation import BioSim
from src.biosim.island import Island


@pytest.fixture
def plain_map_string():
    return Island.clean_multi_line_string("OOOO\nOJSO\nOOOO")


@pytest.fixture
def plain_sim():
    """Return a simple island for used in various tests below"""
    return BioSim(island_map="OOOO\nOJSO\nOOOO", ini_pop=[], seed=1)


def test_pixel_color(plain_sim, plain_map_string):
    class_ = Visuals(plain_sim.island, plain_map_string)
    assert class_.pixel_colors[0][0] == (0.0, 1.0, 1.0)


def test_draw_map(plain_sim, plain_map_string):
    class_ = Visuals(plain_sim.island, plain_map_string)
    assert True
