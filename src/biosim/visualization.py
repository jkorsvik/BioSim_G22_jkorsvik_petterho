# -*- coding: utf-8 -*-

"""
"""

__author__ = "Jon-Mikkel Korsvik & Petter Bøe Hørtvedt"
__email__ = "jonkors@nmbu.no & petterho@nmbu.no"

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class Visuals:
    cell_colors = {
        "Ocean": 'cyan',
        "Savanna": 'yellowgreen',
        "Mountain": 'silver',
        "Desert": 'darkkhaki',
        "Jungle": 'darkgreen'
    }

    def __init__(
            self,
            island,
            map_string,
            num_years_sim,
            ymax_animals=None,
            cmax_animals=None,
            img_base=None,
            img_fmt='png'
    ):
        self.img_num = -1
        self.x_len = island.len_map_x  # Double code
        self.y_len = island.len_map_y  # Double code
        self.num_years_sim = num_years_sim
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt

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
        self.herbivores_over_time = None
        self.carnivores_over_time = None
        self.years = None

        self.setup_graphics()
        self.pixel_colors = self.make_color_pixels(island)

        self.draw_geography()
        self.draw_geography_exp()
        self.draw_heat_map_herbivore(self.get_data_heat_map(
            island, 'num_herbivores')
        )
        self.draw_heat_map_carnivore(self.get_data_heat_map(
            island, 'num_carnivores')
        )
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
            self.figure = plt.figure(constrained_layout=True)
            self.grid = self.figure.add_gridspec(2, 24)

        # The map
        if self.island_map_ax is None:
            self.island_map_ax = self.figure.add_subplot(
                self.grid[0, :10]
            )
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
        self.animals_over_time_ax.plot(
            self.years, self.carnivores_over_time, color='r', label='Carnivore'
        )

        self.animals_over_time_ax.plot(
            self.years, self.herbivores_over_time, color='b', label='Herbivore'
        )
        self.animals_over_time_ax.set(
            xlabel='Year', ylabel='Number of Animals'
        )
        self.animals_over_time_ax.legend(loc='upper left')

    def update_animals_over_time(self, island):
        # Island has property or attribute year
        self.herbivores_over_time.append(
            island.num_animals_per_species['Herbivore'])
        self.carnivores_over_time.append(
            island.num_animals_per_species['Carnivore'])
        self.years.append(island.year)
        self.animals_over_time_ax.plot(
            self.years, self.carnivores_over_time, color='r'
        )
        self.animals_over_time_ax.plot(
            self.years, self.herbivores_over_time, color='b'
        )

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
        return heat_map

    def draw_heat_map_herbivore(self, heat_map):
        self.heat_map_herbivores_ax.axis('off')
        self.heat_map_herbivores_ax.set_title('Heat Map of Herbivores')
        self.heat_map_herb_img_ax = self.heat_map_herbivores_ax.imshow(
            heat_map, cmap='inferno', vmax=300)
        plt.colorbar(
            self.heat_map_herb_img_ax, cax=self.colorbar_herb_ax
        )

    def draw_heat_map_carnivore(self, heat_map):
        self.heat_map_carnivores_ax.axis('off')
        self.heat_map_carnivores_ax.set_title('Heat Map of Carnivores')
        self.heat_map_carn_img_ax = self.heat_map_carnivores_ax.imshow(
            heat_map, cmap='inferno', vmax=150)
        plt.colorbar(
            self.heat_map_carn_img_ax, cax=self.colorbar_carn_ax
        )

    def update_heat_maps(self, island):
        heat_map_herb = self.get_data_heat_map(island, 'num_herbivores')
        self.heat_map_herb_img_ax.set_data(heat_map_herb)

        heat_map_carn = self.get_data_heat_map(island, 'num_carnivores')
        self.heat_map_carn_img_ax.set_data(heat_map_carn)

    def draw_geography(self):
        self.island_map_ax.axis('off')
        self.island_map_ax.set_title('Map')
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
        self.island_map_exp_ax.axis('off')
        for ix, name in enumerate(self.cell_colors.keys()):
            self.island_map_exp_ax.add_patch(
                plt.Rectangle((0., 0.05 + ix * 0.2), 0.3, 0.1,
                              edgecolor=(0, 0, 0),
                              facecolor=self.cell_colors[name]))
            self.island_map_exp_ax.text(
                0.35, 0.05 + ix * 0.2, name,
                transform=self.island_map_exp_ax.transAxes)

    def update_fig(self, island):
        self.update_animals_over_time(island)
        self.update_heat_maps(island)
        plt.pause(1e-6)

    def save_fig(self):
        self.img_num += 1
        print(f'{self.img_base}{self.img_num:03d}')
        self.figure.savefig(f'{self.img_base}{self.img_num:03d}')


if __name__ == '__main__':
    pass
