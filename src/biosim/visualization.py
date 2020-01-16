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
        # Possibly dont need img_ax for those who are not pictures
        # Old placement using add_axis in comments
        self.figure = None
        self.island_map_ax = None  # [0.35, 0.55, 0.45, 0.45]
        self.island_map_img_ax = None
        self.island_map_exp_ax = None  # [0.85, 0.60, 0.1, 0.35]
        self.island_map_exp_img_ax = None  # Might not be needed
        self.heat_map_all_animals_ax = None  # [0.1, 0.1, 0.8, 0.45]
        self.heat_map_all_animals_img_ax = None
        self.colorbar_ax = None
        self.animals_over_time_ax = None  # [0.85, 0.1, 0.1, 0.35]

        self.herbivores_over_time = None
        self.carnivores_over_time = None
        self.years = None

        self.setup_graphics()
        self.pixel_colors = self.make_color_pixels(island)
        self.draw_geography()
        self.draw_geography_exp()
        self.draw_heat_map(self.get_data_heat_map(island, 'num_animals'))
        self.draw_animals_over_time()

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
            self.island_map_exp_ax = self.figure.add_subplot(243)
            self.island_map_exp_img_ax = None
        # The heat map
        if self.heat_map_all_animals_ax is None:
            self.heat_map_all_animals_ax = self.figure.add_subplot(223)
            self.heat_map_all_animals_img_ax = None
        # The colorbar
        if self.colorbar_ax is None:
            self.colorbar_ax = self.figure.add_subplot(244)
        # The animals over time graph
        if self.animals_over_time_ax is None:
            self.animals_over_time_ax = self.figure.add_subplot(224)

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

    def draw_animals_over_time(self):
        self.herbivores_over_time = []
        self.carnivores_over_time = []
        self.years = []
        self.animals_over_time_ax.plot(self.years, self.carnivores_over_time)
        self.animals_over_time_ax.plot(self.years, self.herbivores_over_time)

    def update_animals_over_time(self, island):
        # Island has property or attribute year
        self.herbivores_over_time.append(
            island.num_animals_per_species['Herbivore'])
        self.carnivores_over_time.append(
            island.num_animals_per_species['Carnivore'])
        self.years.append(island.year)
        self.animals_over_time_ax.plot(self.years, self.carnivores_over_time)
        self.animals_over_time_ax.plot(self.years, self.herbivores_over_time)

    def get_data_heat_map(self, island, data_type):
        """

        Parameters
        ----------
        island : class instance of Island
        data_type: str
            num_animals, num_herbivores or num_carnivores

        Returns
        -------

        """
        heat_map = self.empty_nested_list()
        for pos, cell in island.map.items():
            y, x = pos
            heat_map[y][x] = getattr(cell, data_type)
        self.heat_map = heat_map
        return heat_map

    def draw_heat_map(self, heat_map):
        self.heat_map_all_animals_ax.axis('off')
        self.heat_map_all_animals_ax.set_title('Heat map all animals')
        self.heat_map_all_animals_img_ax = self.heat_map_all_animals_ax.imshow(
            heat_map, cmap='inferno')
        plt.colorbar(self.heat_map_all_animals_img_ax, cax=self.colorbar_ax)

    def update_heat_map(self, island):
        self.get_data_heat_map(island, 'num_animals')
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
    for _ in range(150):
        island_instance.simulate_one_year()
        visual.update_heat_map(island_instance)
        visual.update_animals_over_time(island_instance)
        plt.pause(0.05)

    plt.show()
