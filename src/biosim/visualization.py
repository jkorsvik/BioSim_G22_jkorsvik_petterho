# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import src.biosim.simulation as sim


class Visuals:
    cell_colors = {
        "Ocean": 'cyan',
        "Savanna": 'yellowgreen',
        "Mountain": 'silver',
        "Desert": 'darkkhaki',
        "Jungle": 'darkgreen'
    }

    def __init__(self, island, map_string):
        self.pixel_colors = self.make_color_pixels(island, map_string)
        self.geography = self.draw_geography()
        #self.tot_num_ani_by_species = self.line_graph(island_map)
        #self.population_map_herb = self.heatmap_herb(island_map)
        #self.population_map_carn = self.heatmap_carn(island_map)
        #self.figure = plt.figure

    def make_color_pixels(self, island, map_string):
        """
        Creates a list indexed by [y][x] that represents an color by type of
        cell. The color is collected from a class variable called color_params

        For example: pixel_colors[0][0] = the color code for cyan in rgba
                    (since all cell at the edges shall be ocean)

        Parameters
        ----------
        island_map - instance of a map
        map_string - cleaned lines of string

        Returns
        -------
        pixel_colors - nested list with quadruplets of rgba-values

        """
        pixel_colors = []
        for y in range(len(map_string)):
            pixel_colors.append([])
            for x in range(len(map_string[0])):
                pixel_colors[y].append(None)

        for pos, cell in island.map.items():
            y, x = pos
            name_of_class = cell.__class__.__name__
            color_name = self.cell_colors[name_of_class]
            color_code_rgb = mcolors.to_rgba(color_name)
            pixel_colors[y][x] = color_code_rgb
        return pixel_colors

    def draw_geography(self):
        return plt.imshow(self.pixel_colors)

    def line_graph(self, island_map):
        pass

    def heatmap_herb(self, island_map):
        pass

    def heatmap_carn(self, island_map):
        pass


if __name__ == '__main__':
    string = ("OOOO\nOJSO\nOOOO")
    plain = sim.BioSim(island_map="OOOO\nOJSO\nOOOO", ini_pop=[], seed=1)

    island = plain.island

    visual = Visuals(island, string)

    plt.show()