# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import pytest
import textwrap
from src.biosim.visualization import Visuals
from src.biosim.simulation import BioSim


@pytest.fixture
def plain_sim():
    """Return a simple island for used in various tests below"""
    return BioSim(island_map="OOOO\nOJSO\nOOOO", ini_pop=[], seed=1)


def test_pixel_color(plain_sim):
    class_ = Visuals(plain_sim.island_map)
    assert class_.geography[0][0] == ['c']
