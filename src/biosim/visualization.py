# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class Visuals:
    cell_colors = {
        "Ocean": 'c',
        "Savanna": 'yellowgreen',
        "Mountain": 'silver',
        "Desert": 'darkkhaki',
        "Jungle": 'darkgreen'
    }

    def __init__(self, island_map):
        self.geography = self.draw_geography(island_map)
        self.tot_num_ani_by_species = self.line_graph(island_map)
        self.population_map_herb = self.heatmap_herb(island_map)
        self.population_map_carn = self.heatmap_carn(island_map)
        self.figure = plt.figure

    def draw_geography(self, island_map):
        pixel_colors = [[None for _ in range(num_X)] for _ in range(num_Y)]
        for pos, cell in island_map.items():
            y, x = pos
            name_of_class = cell.__class__.__name__
            color_name = self.cell_colors[name_of_class]
            color_code_rgb = mcolors.to_rgba(colors_name)
            pixel_colors[y][x].append(color_code_rgb)
        print(pixel_colors)
        return pixel_colors

    def line_graph(self, island_map):
        pass

    def heatmap_herb(self, island_map):
        pass

    def heatmap_carn(self, island_map):
        pass


if __name__ == '__main__':
