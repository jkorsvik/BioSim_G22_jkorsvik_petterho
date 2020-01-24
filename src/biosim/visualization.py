# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from .island import Island


class Visuals:
    """
    Class handling the visual presentation, as well as storing of images

    Parameters
    ----------
    island : object
       Instance of Island
    num_years_sim : int
       Number of years to simulate, used for line graph
    ymax_animals : int or float
       Y-limit for line graph
    cmax_animals : dict
       Density for heat maps with 'Herbivore' or 'Carnivore' as key
    img_base : path
       Where to store pictures and make movie from
    img_fmt : filetype
       Default: 'png'

    Attributes
    ----------
    cell_colors : dict
        cell type to color name
    density_heatmap : dict
        animal type to int value
    """
    cell_colors = {
        "Ocean": 'cyan',
        "Savanna": 'yellowgreen',
        "Mountain": 'silver',
        "Desert": 'darkkhaki',
        "Jungle": 'darkgreen'
    }
    density_heatmap = {'Herbivore': 275,
                       'Carnivore': 150}

    def __init__(
            self,
            island,
            num_years_sim,
            ymax_animals=None,
            cmax_animals=None,
            img_base=None,
            img_fmt='png'
    ):
        self.img_num = 0
        self.x_len = island.len_map_x  # Double code
        self.y_len = island.len_map_y  # Double code
        self.num_years_sim = num_years_sim

        self.num_years_fig = island.year + num_years_sim

        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt
        if ymax_animals is None:
            self.ymax_animals = 20000
        if cmax_animals is None:
            self.cmax_animals = self.density_heatmap

        # For setup in setup_graphics
        # Possibly dont need img_ax for those who are not pictures
        self.figure = None
        self.grid = None

        self.island_map_ax = None
        self.island_map_img_ax = None
        self.island_map_exp_ax = None
        self.island_map_exp_img_ax = None

        self.heat_map_herbivores_ax = None
        self.heat_map_herb_img_ax = None
        self.colorbar_herb_ax = None

        self.heat_map_carnivores_ax = None
        self.heat_map_carn_img_ax = None
        self.colorbar_carn_ax = None

        self.animals_over_time_ax = None
        self.herbivores_over_time_data = None
        self.carnivores_over_time_data = None
        self.years = None

        self.line_carnivore = None
        self.line_herbivore = None

        self.setup_graphics(island)
        self.pixel_colors = self.make_color_pixels(island)

        self.draw_geography()
        self.draw_geography_exp()
        self.draw_heat_map_herbivore(self.get_data_heat_map(
            island, 'num_herbivores')
        )
        self.draw_heat_map_carnivore(self.get_data_heat_map(
            island, 'num_carnivores')
        )
        self.draw_animals_over_time(island)

        """
        self.tot_num_ani_by_species = self.line_graph(island_map)
        self.population_map_herb = self.heatmap_herb(island_map)
        self.population_map_carn = self.heatmap_carn(island_map)
        """

    def empty_nested_list(self):
        """
        Creates an empty list indexed by y and x (row, columns)
        Returns
        -------
        empty_nested_list : list
            Nested list

        """
        empty_nested_list = []
        for y in range(self.y_len):
            empty_nested_list.append([])
            for x in range(self.x_len):
                empty_nested_list[y].append(None)
        return empty_nested_list

    def setup_graphics(self, island):
        """
        Sets up graphics and places figures in the right place.

        Parameters
        ----------
        island : object
            Instance of Island

        Returns
        -------

        """
        if self.figure is None:
            self.figure = plt.figure(constrained_layout=True, figsize=(16, 9))
            self.grid = self.figure.add_gridspec(2, 24)

        # The map
        if self.island_map_ax is None:
            self.island_map_ax = self.figure.add_subplot(
                self.grid[0, :10]
            )
            self.island_map_ax.set_title(f' Year: {island.year}')
            self.island_map_img_ax = None

        # The color explanation
        if self.island_map_exp_ax is None:
            self.island_map_exp_ax = self.figure.add_subplot(
                self.grid[0, 10]
            )
            self.island_map_exp_img_ax = None

        # The animals over time graph
        if self.animals_over_time_ax is None:
            self.animals_over_time_ax = self.figure.add_subplot(
                self.grid[0, 12:]
            )
            self.animals_over_time_ax.set_ylim(self.ymax_animals)
            self.animals_over_time_ax.invert_yaxis()

            self.animals_over_time_ax.set_xlim(self.num_years_fig)
            self.animals_over_time_ax.invert_xaxis()

        # The heat maps
        if self.heat_map_herbivores_ax is None:
            self.heat_map_herbivores_ax = self.figure.add_subplot(
                self.grid[1, :11]
            )
            self.heat_map_herb_img_ax = None

        if self.heat_map_carnivores_ax is None:
            self.heat_map_carnivores_ax = self.figure.add_subplot(
                self.grid[1, 12:-1]
            )
            self.heat_map_carn_img_ax = None

        # The colorbars
        if self.colorbar_herb_ax is None:
            self.colorbar_herb_ax = self.figure.add_subplot(
                self.grid[1, 11]
            )
        if self.colorbar_carn_ax is None:
            self.colorbar_carn_ax = self.figure.add_subplot(
                self.grid[1, -1]
            )

    def make_color_pixels(self, island):
        """
        Creates a list indexed by [y][x] that represents an color by type of
        cell. The color is collected from a class variable called color_params

        For example: pixel_colors[0][0] = the color code for cyan in rgba
                    (since all cell at the edges shall be ocean)

        Parameters
        ----------
        island : instance of a map

        Returns
        -------
        pixel_colors : list
            Nested with triplets of rgb-values

        """
        pixel_colors = self.empty_nested_list()

        for pos, cell in island.map.items():
            y, x = pos
            name_of_class = cell.__class__.__name__
            color_name = self.cell_colors[name_of_class]
            color_code_rgb = mcolors.to_rgb(color_name)
            pixel_colors[y][x] = color_code_rgb
        return pixel_colors

    def draw_geography(self):
        """
        Draws pixels for geography with right colors
        Returns
        -------

        """
        self.island_map_ax.axis('off')
        self.island_map_img_ax = self.island_map_ax.imshow(
            self.pixel_colors)
        """
        self.island_map_ax.set_xticks(range(len(self.pixel_colors[0])))
        self.island_map_ax.set_xticklabels(range(1, 
        1 + len(self.pixel_colors[0])))
        self.island_map_ax.set_yticks(range(len(self.pixel_colors)))
        self.island_map_ax.set_yticklabels(range(1, 
        1 + len(self.pixel_colors)))
        """

    def draw_geography_exp(self):
        """
        Creates legend for geography map

        Returns
        -------

        """
        self.island_map_exp_ax.axis('off')
        for ix, name in enumerate(self.cell_colors.keys()):
            self.island_map_exp_ax.add_patch(
                plt.Rectangle((0., 0.05 + ix * 0.2), 0.3, 0.1,
                              edgecolor=(0, 0, 0),
                              facecolor=self.cell_colors[name]))
            self.island_map_exp_ax.text(
                0.35, 0.05 + ix * 0.2, name,
                transform=self.island_map_exp_ax.transAxes
            )

    def update_year(self, island):
        """Updates title of map to current year"""
        self.island_map_ax.set_title(f' Year: {island.year}')

    def draw_animals_over_time(self, island):
        """
        Draw line graph for herbivores and carnivores over time.

        Parameters
        ----------
        island : object
            Instance of Island

        Returns
        -------

        """
        self.herbivores_over_time_data = island.herbivore_tot_data.copy()
        self.carnivores_over_time_data = island.carnivore_tot_data.copy()
        self.years = [year for year in range(island.year + 1)]
        for n in range(self.num_years_sim):
            self.herbivores_over_time_data.append(None)
            self.carnivores_over_time_data.append(None)
            self.years.append(island.year + n + 1)

        self.herbivores_over_time_data = np.array(
            self.herbivores_over_time_data)
        self.carnivores_over_time_data = np.array(
            self.carnivores_over_time_data)
        self.years = np.array(self.years)
        self.line_carnivore, = self.animals_over_time_ax.plot(
            self.years, self.carnivores_over_time_data,
            color='r', label='Carnivore'
        )

        self.line_herbivore, = self.animals_over_time_ax.plot(
            self.years, self.herbivores_over_time_data, color='b', label='Herbivore'
        )
        self.animals_over_time_ax.set(
            xlabel='Years', ylabel='Number of Animals'
        )
        self.animals_over_time_ax.legend(loc='upper left')

    def update_animals_over_time(self, island):
        """
        Collect data from island instance to plot graph

        Parameters
        ----------
        island : object
            Instance of Island

        Returns
        -------

        """
        # Island has property or attribute year
        self.herbivores_over_time_data[island.year] = island.herbivore_tot_data[-1]
        self.carnivores_over_time_data[island.year] = island.carnivore_tot_data[-1]

        self.line_herbivore.set_ydata(self.herbivores_over_time_data)

        self.line_carnivore.set_ydata(self.carnivores_over_time_data)



    def get_data_heat_map(self, island, data_type):
        """
        Could have also used pandas DF to get data.

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
        return heat_map

    def draw_heat_map_herbivore(self, heat_map):
        """
        Draws heat map

        Parameters
        ----------
        heat_map : list
            Nested list with int

        Returns
        -------

        """
        self.heat_map_herbivores_ax.axis('off')
        self.heat_map_herbivores_ax.set_title('Distribution of Herbivores')
        self.heat_map_herb_img_ax = self.heat_map_herbivores_ax.imshow(
            heat_map, cmap='inferno', vmax=self.cmax_animals['Herbivore'])
        plt.colorbar(
            self.heat_map_herb_img_ax, cax=self.colorbar_herb_ax
        )

    def draw_heat_map_carnivore(self, heat_map):
        """
        Draws heat map

        Parameters
        ----------
        heat_map : list
           Nested list with int

        Returns
        -------

        """
        self.heat_map_carnivores_ax.axis('off')
        self.heat_map_carnivores_ax.set_title('Distribution of Carnivores')
        self.heat_map_carn_img_ax = self.heat_map_carnivores_ax.imshow(
            heat_map, cmap='inferno', vmax=self.cmax_animals['Carnivore'])
        plt.colorbar(
            self.heat_map_carn_img_ax, cax=self.colorbar_carn_ax
        )

    def update_heat_maps(self, island):
        """
        Gets new data for heat map from island

        Parameters
        ----------
        island : object
            Instance of Island

        Returns
        -------

        """
        heat_map_herb = self.get_data_heat_map(island, 'num_herbivores')
        self.heat_map_herb_img_ax.set_data(heat_map_herb)

        heat_map_carn = self.get_data_heat_map(island, 'num_carnivores')
        self.heat_map_carn_img_ax.set_data(heat_map_carn)

    def update_fig(self, island):
        """Updates the figure"""
        self.update_animals_over_time(island)
        self.update_heat_maps(island)
        self.update_year(island)
        plt.pause(1e-10)

    def save_fig(self):
        """Saves the figure at desired destination"""

        self.figure.savefig(
            f'{self.img_base}_{self.img_num:05d}.{self.img_fmt}',
            orientation='landscape')
        self.img_num += 1


if __name__ == '__main__':
    ini_herbs = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]

    island = Island(island_map_string='OOO\nOJO\nOOO', ini_pop=ini_herbs)
    visuals = Visuals(island, 50)
    for _ in range(50):
        island.simulate_one_year()
        visuals.update_animals_over_time(island)
    plt.show()