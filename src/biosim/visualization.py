# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import src.biosim.simulation as sim
import textwrap




class Visuals:
    cell_colors = {
        "Ocean": 'cyan',
        "Savanna": 'yellowgreen',
        "Mountain": 'silver',
        "Desert": 'darkkhaki',
        "Jungle": 'darkgreen'
    }

    def __init__(self, island, map_string):
        self.x_len = len(map_string[0])
        self.y_len = len(map_string)
        # For setup in setup_graphics
        # Plan on using subplots
        self.figure = None
        self.ax1 = [0.35, 0.55, 0.45, 0.45]
        self.ax11 = None
        self.ax2 = [0.85, 0.60, 0.1, 0.35]
        self.ax21 = None
        self.ax3 = [0.1, 0.1, 0.8, 0.45]
        self.ax31 = None
        self.ax4 = [0.85, 0.1, 0.1, 0.35]
        self.ax41 = None

        self.setup_graphics()
        self.pixel_colors = self.make_color_pixels(island)
        self.heatmap = self.get_data_heatmap_all_animals(island)
        self.draw_geography()
        self.draw_heatmap()

        #self.tot_num_ani_by_species = self.line_graph(island_map)
        #self.population_map_herb = self.heatmap_herb(island_map)
        #self.population_map_carn = self.heatmap_carn(island_map)
        #self.figure = plt.figure

    def empty_nested_list(self):
        empty_nested_list = []
        for y in range(self.y_len):
            empty_nested_list.append([])
            for x in range(self.x_len):
                empty_nested_list[y].append(None)
        return empty_nested_list

    def setup_graphics(self):
        if self.figure is None:
            self.figure = plt.figure()

        # The map
        if self.ax1 is None:
            self.ax1 = self.figure.add_subplot()
            self.ax11 = None
        # The color explanation
        if self.ax2 is None:
            self.ax2 = self.figure.add_subplot()
            self.ax21 = None
        # The heat map
        if self.ax2 is None:
            self.ax2 = self.figure.add_subplot()
            self.ax21 = None

    def make_color_pixels(self, island):
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
        pixel_colors = self.empty_nested_list()

        for pos, cell in island.map.items():
            y, x = pos
            name_of_class = cell.__class__.__name__
            color_name = self.cell_colors[name_of_class]
            color_code_rgb = mcolors.to_rgb(color_name)
            pixel_colors[y][x] = color_code_rgb
        return pixel_colors

    def get_data_heatmap_all_animals(self, island):
        heat_map = self.empty_nested_list()
        for pos, cell in island.map.items():
            y, x = pos
            heat_map[y][x] = cell.num_animals
        self.heatmap = heat_map
        return heat_map

    def draw_heatmap(self):
        axim = self.figure.add_axes(self.ax3)
        plt.imshow(self.heatmap, cmap='inferno')
        # axim.set_xticks(range(len(self.heatmap[0])))
        # axim.set_xticklabels(range(1, 1 + len(self.heatmap[0])))
        # axim.set_yticks(range(len(self.heatmap)))
        # axim.set_yticklabels(range(1, 1 + len(self.heatmap)))
        axim.axis('off')
        axim.set_title('Heatmap all animals')
        colorbar = plt.colorbar()

    def update_heatmap_all_animals(self, island):
        self.get_data_heatmap_all_animals(island)
        plt.imshow(self.heatmap, cmap='inferno')


    def draw_geography(self):
        axim = self.figure.add_axes(self.ax1)
        plt.imshow(self.pixel_colors)
        axim.set_xticks(range(len(self.pixel_colors[0])))
        axim.set_xticklabels(range(1, 1 + len(self.pixel_colors[0])))
        axim.set_yticks(range(len(self.pixel_colors)))
        axim.set_yticklabels(range(1, 1 + len(self.pixel_colors)))
        axim.axis('off')

        axlg = self.figure.add_axes(self.ax2)
        axlg.axis('off')
        for ix, name in enumerate(self.cell_colors.keys()):
            axlg.add_patch(plt.Rectangle((0., 0.05 + ix * 0.2), 0.3, 0.1,
                                         edgecolor=(0, 0, 0),
                                         facecolor=self.cell_colors[name]))
            axlg.text(0.35, 0.05 + ix * 0.2, name, transform=axlg.transAxes)
        """


    def line_graph(self, island_map):
        pass

    def heatmap_herb(self, island_map):
        pass

    def heatmap_carn(self, island_map):
        pass
    """


if __name__ == '__main__':
    geogr = """\
            OOOOOOOOOOOOOOOOOOOOO
            OOOOOOOOSMMMMJJJJJJJO
            OSSSSSJJJJMMJJJJJJJOO
            OSSSSSSSSSMMJJJJJJOOO
            OSSSSSJJJJJJJJJJJJOOO
            OSSSSSJJJDDJJJSJJJOOO
            OSSJJJJJDDDJJJSSSSOOO
            OOSSSSJJJDDJJJSOOOOOO
            OSSSJJJJJDDJJJJJJJOOO
            OSSSSJJJJDDJJJJOOOOOO
            OOSSSSJJJJJJJJOOOOOOO
            OOOSSSSJJJJJJJOOOOOOO
            OOOOOOOOOOOOOOOOOOOOO
            """
    string = textwrap.dedent(geogr)
    ini_herbs = [
        {
            "loc": (2, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 40}
                for _ in range(200)
            ],
        }
    ]
    plain = sim.BioSim(island_map=string, ini_pop=ini_herbs, seed=1)
    lines = plain.island.clean_multi_line_string(string)

    island = plain.island
    # visual = Visuals(island, lines)
    for _ in range(30):
        island.simulate_one_year()
        #visual.update_heatmap_all_animals()
        #plt.pause(0.05)
    visual = Visuals(island, lines)

    plt.show()

