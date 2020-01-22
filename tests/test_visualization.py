# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import pytest
from biosim.visualization import Visuals


class TestVisualization:
    """
    This was made test the visualization, but we didnt find the time to test
    it more than visually.
    """
    def test_init(self):
        assert False

    def test_empty_nested_list(self):
        assert False

    def test_setup_graphics(self):
        assert False

    def test_make_color_pixels(self, test_island):
        class_ = Visuals(test_island, 10)
        assert class_.pixel_colors[0][0] == (0.0, 1.0, 1.0)

    def test_draw_geography(self, test_island):
        class_ = Visuals(test_island, 10)
        assert False

    def test_draw_geography_exp(self):
        assert False

    def test_update_year(self):
        assert False

    def test_draw_animals_over_time(self):
        assert False

    def test_update_animals_over_time(self):
        assert False

    def test_get_data_heat_map(self):
        assert False

    def test_draw_heat_map_herbivore(self):
        assert False

    def test_draw_heat_map_carnivore(self):
        assert False

    def test_update_heat_maps(self):
        assert False

    def test_update_fig(self):
        assert False

    def test_save_fig(self):
        assert False
