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
        self.island_map_ax = None  # [0.35, 0.55, 0.45, 0.45]
        self.island_map_img_ax = None
        self.island_map_exp_ax = None  # [0.85, 0.60, 0.1, 0.35]
        self.island_map_exp_img_ax = None
        self.heat_map_all_animals_ax = None  # [0.1, 0.1, 0.8, 0.45]
        self.heat_map_all_animals_img_ax = None
        self.ax4 = None  # [0.85, 0.1, 0.1, 0.35]
        self.ax41 = None

        self.setup_graphics()
        self.pixel_colors = self.make_color_pixels(island)
        self.heat_map = self.get_data_heat_map_all_animals(island)
        self.draw_geography()
        self.draw_geography_exp()
        self.draw_heat_map()

        """
        self.tot_num_ani_by_species = self.line_graph(island_map)
        self.population_map_herb = self.heatmap_herb(island_map)
        self.population_map_carn = self.heatmap_carn(island_map)
        """

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
        if self.island_map_ax is None:
            self.island_map_ax = self.figure.add_subplot(221)
            self.island_map_img_ax = None
        # The color explanation
        if self.island_map_exp_ax is None:
            self.island_map_exp_ax = self.figure.add_subplot(222)
            self.island_map_exp_img_ax = None
        # The heat map
        if self.heat_map_all_animals_ax is None:
            self.heat_map_all_animals_ax = self.figure.add_subplot(223)
            self.island_map_exp_img_ax = None

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

    def get_data_heat_map_all_animals(self, island):
        heat_map = self.empty_nested_list()
        for pos, cell in island.map.items():
            y, x = pos
            heat_map[y][x] = cell.num_animals
        self.heat_map = heat_map
        return heat_map

    def draw_heat_map(self):
        self.heat_map_all_animals_ax.axis('off')
        self.heat_map_all_animals_ax.set_title('Heatmap all animals')
        self.heat_map_all_animals_img_ax = self.heat_map_all_animals_ax.imshow(
            self.heat_map, cmap='inferno')
        plt.colorbar(self.heat_map_all_animals_img_ax)

    def update_heat_map_all_animals(self, island):
        self.get_data_heat_map_all_animals(island)
        self.heat_map_all_animals_img_ax.set_data(self.heat_map)

    def draw_geography(self):
        self.island_map_ax.axis('off')
        self.island_map_ax.set_title('Map')
        self.island_map_img_ax = self.island_map_ax.imshow(
            self.pixel_colors)
        """
        self.island_map_ax.set_xticks(range(len(self.pixel_colors[0])))
        self.island_map_ax.set_xticklabels(range(1, 1 + len(self.pixel_colors[0])))
        self.island_map_ax.set_yticks(range(len(self.pixel_colors)))
        self.island_map_ax.set_yticklabels(range(1, 1 + len(self.pixel_colors)))
        """

    def draw_geography_exp(self):
        self.island_map_exp_ax.axis('off')
        for ix, name in enumerate(self.cell_colors.keys()):
            self.island_map_exp_ax.add_patch(
                plt.Rectangle((0., 0.05 + ix * 0.2), 0.3, 0.1,
                              edgecolor=(0, 0, 0),
                              facecolor=self.cell_colors[name]))
            self.island_map_exp_ax.text(0.35, 0.05 + ix * 0.2,
                                        name, transform=self.island_map_exp_ax.transAxes)
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

    island_instance = plain.island
    visual = Visuals(island_instance, lines)
    for _ in range(70):
        island_instance.simulate_one_year()
        visual.update_heat_map_all_animals(island_instance)
        plt.pause(0.05)

    plt.show()
